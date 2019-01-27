import argparse
from filedb.loader import Loader
import logging

logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--init', required=False, help="start the database from scratch",
                        type=bool, default=False)
    parser.add_argument('-f', '--db_file', required=False, type=str,
                        help="Location of the database file")
    return parser.parse_args()


if __name__ == '__main__':
    logger.info(" Inside the load ")
    try:
        parse_arguments()
    except ValueError as e:
        print(repr(e))
    args = parse_arguments()

    loader = Loader(db_file=args.db_file, init=args.init)
    loader.load()



