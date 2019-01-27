import json
import logging

logger = logging.getLogger(__name__)


class JsonStore:
    """
    Decided to simply use json for storing the data.
    """

    def __init__(self, file_name, init=False, **kwargs):

        self._file_name = file_name

        self._init_db_json(init)
        self.kwargs = kwargs

        self._file_handle = open(self._file_name, 'r+')

    def close(self):
        self._file_handle.close()
        logger.info("Closing the file")

    def flush(self):
        self._file_handle.flush()
        logger.info("Closing the file")

    def read(self):
        self._file_handle.seek(0)
        record_list = json.load(self._file_handle)
        return record_list

    def write(self, data):
        self._file_handle.seek(0)
        json.dump(data, self._file_handle, **self.kwargs)

    def _init_db_json(self, init):
        try:
            open(self._file_name, 'r')
        except FileNotFoundError:
            logger.info('Db file does not exist, hence creating one')
            self._create_a_new_ds()
            # doesn't exist
        else:
            logger.info("Db file already exists")
            if init is True:
                self._create_a_new_ds()

    def _create_a_new_ds(self):
        with open(self._file_name, 'w') as db_fp:
            record_list = {}
            json.dump(record_list, db_fp)
