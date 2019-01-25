import logging
from collections import OrderedDict
from filedb.datastore import JsonStore

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class FileDB:
    def __init__(self, db_file):
        self._data_store = JsonStore(file_name=db_file, indent=4)

    def insert(self, record: dict):
        data = self._read()
        data.update(record)
        self._write(data)
        return list(record.keys())[-1]

    def insert_many(self, records: dict):
        rec_id = self.insert(records)
        return rec_id

    def query(self):
        return None

    def _read(self):
        return self._data_store.read()

    def _write(self, values):
        self._data_store.write(values)

