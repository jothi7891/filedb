from filedb.db import FileDB
import logging
from collections import OrderedDict, MutableMapping, defaultdict
import json
from operator import itemgetter
from itertools import groupby

logger = logging.getLogger(__name__)


def collect(t):
    return list(OrderedDict.fromkeys(t))


def count(t):
    return len(collect(t))


class Query:
    def __init__(self, select_args={}, group_by_arg=None, filter_args=None, order_by_args=[], db_file="filedb/db.json"):
        self.select_args = select_args
        self.group_by_arg = group_by_arg

        self.order_by_args = order_by_args

        self.db = FileDB(db_file=db_file)

        self._init_field_properties()

        self.db_keys = [key for key in self.field_properties]

        self.filter_args = self._transform_filter(filter_args)._store if filter_args else None

    def query(self):
        try:
            result = self.db.query(self.filter_args)

            if self.group_by_arg:
                result = self._group_result(result)
            if self.order_by_args:
                result = self._order_result(result)
            if self.select_args:
                result = self._select_results(result)
            self._beautify_result(result)

        except KeyError as e:
            logger.info("Unexpected key in the arguments" + repr(e))
        except TypeError as e:
            logger.info("Invalid operation on the operand" + repr(e))


    def _init_field_properties(self):
        with open("filedb/properties.json") as properties:
            self.field_properties = json.load(properties, object_pairs_hook=OrderedDict)

    def _transform_filter(self, filter_args):

        filter_args = filter_args.replace(" OR ", " | ")
        filter_args = filter_args.replace(" AND ", " & ")

        for key in self.db_keys:
            start_index = 0
            while start_index <= len(filter_args) and start_index != -1:
                start_index = filter_args.find(key.upper(), start_index)
                if start_index == -1:
                    break
                end_index = min(filter_args.find(')', start_index), filter_args.find(' &', start_index) ,
                                filter_args.find(' |', start_index), key=lambda x: len(filter_args) if x == -1 else x)
                if end_index == -1:
                    filter_args = filter_args[:start_index] + 'Filter(' + filter_args[start_index:] + ')'
                else:
                    filter_args = filter_args[:start_index] + 'Filter(' + filter_args[start_index:end_index] + ')' + \
                                    filter_args[end_index:]
                start_index = end_index
            filter_args = filter_args.replace(key.upper(), key)

        return eval(filter_args)

    def _order_result(self, result):
        result = sorted(result, key=itemgetter(*self.order_by_args))
        return result

    def _group_result(self, result):
        new_result = []

        for key, group in groupby(sorted(result, key=itemgetter(self.group_by_arg)), key=itemgetter(self.group_by_arg)):
            new_dict = defaultdict(list)
            for item in list(group):
                new_dict[self.group_by_arg] = key
                for item_key, item_value in item.items():
                    if item_value != key:
                        new_dict[item_key].append(item_value)
            new_result.append(new_dict)
        return new_result

    def _select_results(self, result):
        # return [OrderedDict((key, self._apply_func(key, value)) for key, value in record.items()
        #                     if key in self.select_args.keys()) for record in result]

        return [OrderedDict((key, self._apply_func(key, record[key])) for key in self.select_args.keys())
                for record in result]

    def _apply_func(self, key, value):
        try:
            func_mapping = { 'sum': sum,
                             'min': min,
                             'max': max,
                             'collect': collect,
                             'count': count}
            if self.select_args[key]:
                if self.group_by_arg:
                    return func_mapping[self.select_args[key]](value)
                else:
                    logger.error("cannot perform sorting aggregate function without groupby")
            else:
                return value
        except KeyError:
            raise ValueError("Invalid function defined for the item")
        except ValueError:
            raise ValueError("Invalid datatype for the function")

    def _beautify_result(self, result):
        # construct the format
        print(''.join(map(self._apply_formatting, list(self.select_args.keys()))).upper())
        for item in result:
            print(''.join(map(self._apply_formatting, list(item.values()))))

    @staticmethod
    def _apply_formatting(item):
        return '{:15}'.format(str(item))


class Filter:
    def __init__(self, **kwargs):
        self._store = [UniqueKeyValueDict(**kwargs)]

    def __or__(self, other):
        if isinstance(other, Filter):
            self._store = self._store + other._store
            return self
        else:
            return NotImplemented

    def __and__(self, other):
            if isinstance(other, Filter):
                if len(other._store) == 0:
                    self._store =[]
                else:
                    del_list = []
                    for item1 in self._store:
                        for item2 in other._store:
                            try:
                                item1.update(item2)
                            except AttributeError:
                                del_list.append(item1)
                    self._store = [item for item in self._store if item not in del_list]
                return self

            else:
                return NotImplemented


class UniqueKeyValueDict(MutableMapping, dict):
    def __init__(self, *args, **kwargs):
        self._dict = dict(*args, **kwargs)

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        if key in self and self._dict[key] != value:
            raise AttributeError("Key '{}' already exists with value '{}'.".format(key, self[key]))
        self._dict[key] = value

    def __delitem__(self, key):
        del self._dict[key]

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

