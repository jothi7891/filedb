import logging
import json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class FileDB:
    def __init__(self):
        with open("input.txt") as input_file:
            self.db = self.load_db(input_file)
        with open("properties.json") as properties:


    def load_db(self, input_file):
        self._parse(input_file)

