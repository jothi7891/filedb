import logging
import json
from operator import and_
from collections import OrderedDict
from datetime import datetime


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class FileDB:
    def __init__(self):
        with open("properties.json") as properties:
            self.field_properties = json.load(properties, object_pairs_hook=OrderedDict)
            # could be easily made as a class on its own - but just keeping it as a config dict for now
        self.db_keys = [key for key in self.field_properties]
        self.db_file = "db.json"
        # Initialize the db json if not present
        self._init_db_json()
        self.unprocessed_file = "unprocessed.txt"
        self.new_records = {}

    def load(self):
        with open("input.txt") as input_file:
            self._parse_and_update(input_file)

    def _init_db_json(self):
        try:
            open(self.db_file, 'r')
        except FileNotFoundError:
            logger.info('Db file does not exist, hence creating one')
            with open(self.db_file, 'w') as db_fp:
                record_list = {}
                json.dump(record_list, db_fp)
        # doesn't exist
        else:
            logger.info("Db file already exists")

    def _parse_and_update(self, input_file):
        header_validated = False

        for line in input_file:
            # strip off the newline at the end
            line = line.rstrip('\n')
            if header_validated is False:
                header_validated = self._validate_header(line)
                logger.info("validating the header line")
            else:
                try:
                    logger.info("validated the fields line")
                    parsed_line = self._validate_fields(line)
                    self._add_record_to_db(parsed_line)
                except ValueError as e:
                    logger.error("Error processing the record"+ repr(e) + line)
                    # Adding it to the different file so it could be processed later
                    self._add_to_unprocessed_record(line)

    def _validate_header(self, line):
        logger.info("validating the header info")
        header_details = "|".join(self.db_keys).upper()
        if line == header_details:
            return True
        else:
            return False

    def _validate_fields(self, line):
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

    def _add_record_to_db(self, parsed_line):

        db_record = {key: value for key, value in zip(self.db_keys,parsed_line)}

        record_id = self._create_id(parsed_line)

        self._update(record_id, db_record)

    def _add_to_unprocessed_record(self, line):
        with open(self.unprocessed_file , 'a+') as fp:
            fp.write(line + '\n')
        logger.info("Line {0} was added to the unprocessed file".format(line))

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

        # Used Json for simplicity and given no constraints on the datastore, for sure this will be not
        # efficient for processing greater number of records.
        self.new_records[record_id] = db_record
        logger.info("Successfully inserted/updated record{0} with {1}".format(repr(db_record), id))

    def commit(self):
        # Just not lazily loading just incase if we need to rollback we still have 2 dicts , one new and one
        # existing .. an easy way for now
        try:
            with open(self.db_file, 'r') as db_fp:
                record_list = json.load(db_fp)

                record_list.update(self.new_records)

            with open(self.db_file, 'w') as db_fp:
                json.dump(record_list, db_fp, sort_keys=True, indent=4)

        except IOError as e:
            logger.error("Error commiting the records {0} to the database ".format(repr(e)))
        except ValueError as e:
            logger.error("Error commiting the record {0} to the database".format(repr(e)))

