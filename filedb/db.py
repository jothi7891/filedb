import logging
from filedb.datastore import JsonStore

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class FileDB:
    """
    class for handling all the DB operations
    """
    def __init__(self, db_file, init=False):
        self._data_store = JsonStore(file_name=db_file, indent=4, init=init)

    def insert(self, record: dict):
        data = self._read()
        data.update(record)
        self._write(data)
        return list(record.keys())[-1]

    def insert_many(self, records: dict):
        rec_id = self.insert(records)
        return rec_id

    def query(self, filter_args=None):
        records = self._read()
        filtered_records = {}
        if filter_args:
            for each_filter in filter_args:
                filtered_records.update({rid: record for rid, record in records.items() if each_filter.items() <= record.items()})
        else:
            filtered_records = records
        return list(filtered_records.values())

    def _read(self):
        return self._data_store.read()

    def _write(self, values):
        self._data_store.write(values)

    def close(self):
        self._data_store.close()

    def flush(self):
        self._data_store.flush()


