import json
from collections import OrderedDict
import logging
from operator import and_
from datetime import datetime
from filedb.db import FileDB

logger = logging.getLogger(__name__)


class Loader:
    def __init__(self, db_file="filedb/db.json", input_file="data/input.txt",
                 unprocessed_file= "data/unprocessed.txt", init=False):

        self._init_field_properties()
        # could be easily made as a class on its own - but just keeping it as a config dict for now
        self.db_keys = [key for key in self.field_properties]

        self.header_validated = False

        self.db = FileDB(db_file=db_file)
        self.input_file = input_file
        self.unprocessed_file = unprocessed_file

    def load(self):
        with open(self.input_file) as input_file:
            self.new_records = {}
            for line in input_file:
                parsed_line = self._parse(line)
                if parsed_line is not None:
                    self.add_record_to_db(parsed_line)
            self.db.insert_many(self.new_records)

    def add_record_to_db(self, parsed_line):

        db_record = {key: value for key, value in zip(self.db_keys, parsed_line)}

        record_id = self._create_id(parsed_line)

        self._update(record_id, db_record)

    def _add_to_unprocessed_record(self, line):
        with open(self.unprocessed_file, 'a+') as fp:
            fp.write(line + '\n')
        logger.info("Line {0} was added to the unprocessed file".format(line))

    def _parse(self, line):
        parsed_line = None

        # strip off the newline at the end
        line = line.rstrip()
        if self.header_validated is False:
            self.header_validated = self._validate_header(line)
            logger.info("validating the header line")
        else:
            try:
                logger.info("validated and transform the fields line")
                parsed_line = self._create_record(line)

            except ValueError as e:
                logger.error("Error processing the record" + repr(e) + line)
                # Adding it to the different file so it could be processed later
                self._add_to_unprocessed_record(line)
        return parsed_line

    def _validate_header(self, line):
        logger.info("validating the header info")
        header_details = "|".join(self.db_keys).upper()
        if line == header_details:
            return True
        else:
            return False

    def _create_record(self, line):
        try:
            # Find the right field property from the field properties file and validate it
            fields = line.split('|')
            trans_field_list = []
            valid = True
            # could use map and lambda or a func here , but going with the list comprehension
            # actually avoiding the list comprehension here to avoid multiple loops and going with the convention for
            # loop
            for field, key in zip(fields, self.db_keys):
                field_valid, trans_field = self._validate_and_transform(field, self.field_properties[key])
                valid = valid and field_valid
                trans_field_list.append(trans_field)

                # use logical and on the values  and if it returns True , then something is wrong on the field type
                if valid is False:
                    raise ValueError
        except ValueError as e:
            logger.error("The line {0} did not match the properties defined - {1}".format(line, repr(e)))
            raise ValueError
        else:
            logger.info("The line {0} is validated successfully against the property".format(line))
            return trans_field_list

    def _validate_and_transform(self, field, field_property):
        valid = True
        trans_field = None
        logger.info("validating field {0} against its defined properties".format(field))
        for key, value in field_property.items():
            if key == 'field_type':
                field_valid, trans_field = self._validate_type(field, value)
                valid = and_(field_valid, valid)
            elif key == 'max_len':
                valid = and_(True if len(field) <= value else False, valid)
            elif key == 'max_value':
                valid = and_(True if field <= value else False, valid)
            elif key == 'min_value':
                valid = and_(True if field >= value else False, valid)
            elif key == 'required' and value is True:
                valid = and_(True if field != '' else False, valid)
            elif key in ['name', 'description']:
                continue
            else:
                logger.error('undefined property {0} in the properties.json'.format(field_property))
            if valid is False:
                break
        logger.info("The field {0} validity against its property is {1}".format(field, valid))
        return valid, trans_field

    @staticmethod
    def _validate_type(field, field_type):
        return_value = (False, None)
        try:
            if field_type == 'text' and type(field) is str:
                return_value = (True, field)
            elif field_type == 'int':
                return_value = (True, int(field))
            elif field_type == 'date' and datetime.strptime(field, "%Y-%m-%d"):
                return_value = (True, field)
            elif field_type == 'datetime' and datetime.strptime(field, "%Y-%m-%d %H:%M"):
                return_value = (True, field)
            elif field_type == 'float':
                return_value = (True, float(field))
        except ValueError:
            logger.error("Encountered exception in validating the type{0} for field {1}".format(field_type, field))
        finally:
            return return_value

    def _init_field_properties(self):
        with open("filedb/properties.json") as properties:
            self.field_properties = json.load(properties, object_pairs_hook=OrderedDict)

    # reduce is not present in 3.5 hence defining a custom defined one
    @staticmethod
    def _reduce(function, iterable, initializer=None):
        it = iter(iterable)
        if initializer is None:
            value = next(it)
        else:
            value = initializer
        for element in it:
            value = function(value, element)
        return value

    @staticmethod
    def _create_id(parsed_line):
        return '-'.join(map(str, parsed_line[:3]))

    def _update(self, record_id, db_record):
        self.new_records[record_id] = db_record



