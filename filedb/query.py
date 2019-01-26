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
    def __init__(self, select_args={}, group_by_arg=None, filter_args=[], order_by_args=[], db_file="filedb/db.json"):
        self.select_args = select_args
        self.group_by_arg = group_by_arg
        self.filter_args = filter_args
        self.order_by_args = order_by_args

        self.db = FileDB(db_file=db_file)

        self._init_field_properties()

        self.db_keys = [key for key in self.field_properties]

    def _init_field_properties(self):
        with open("filedb/properties.json") as properties:
            self.field_properties = json.load(properties, object_pairs_hook=OrderedDict)

    def query(self):
        result = self.db.query(self.filter_args)

        if self.group_by_arg:
            result = self._group_result(result)
        if self.order_by_args:
            result = self._order_result(result)
        if self.select_args:
            result = self._select_results(result)
        logger.info(repr(result))

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
        return [{key: self._apply_func(key, value) for key, value in record.items() if key in self.select_args.keys()}
                for record in result]

    def _apply_func(self, key, value):
        try:
            func_mapping = { 'sum': sum,
                             'min': min,
                             'max': max,
                             'collect': collect,
                             'count': count}
            if self.select_args[key]:
                return func_mapping[self.select_args[key]](value)
            else:
                return value
        except KeyError:
            raise ValueError("Invalid function defined for the item")
        except ValueError:
            raise ValueError("Invalid datatype for the function")


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

