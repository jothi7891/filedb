import argparse
from filedb.loader import Loader
import logging

logger = logging.getLogger(__name__)


def parse_arguments():
    """

    :return: args
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=False, help="start the database from scratch",
                        type=str,default="data/input.txt")
    parser.add_argument('-f', '--db_file', required=False, type=str,
                        help="Location of the database file", default="filedb/db.json")
    parser.add_argument('-r', '--remove', required=False, type=bool,
                        help="Location of the database file", default=False)
    return parser.parse_args()


if __name__ == '__main__':

    logger.info(" Inside the load ")
    try:
        parse_arguments()
    except ValueError as e:
        print(repr(e))
    args = parse_arguments()

    loader = Loader(db_file=args.db_file, init=args.remove, input_file=args.input)
    loader.load()



