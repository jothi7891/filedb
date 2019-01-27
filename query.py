import argparse
from filedb.query import Filter, Query
from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--select', required=True, help="Columns to be selected in the displayed",
                        type=str, default=False)
    parser.add_argument('-o', '--order_by', required=False, type=str,
                        help="Order by columns")
    parser.add_argument('-g', '--group_by', required=False, type=str,
                        help="group by column")
    parser.add_argument('-f', '--filter', required=False, type=str,
                        help="filter columns")
    return parser.parse_args()


if __name__ == '__main__':
    try:
        parse_arguments()
    except ValueError as e:
        print(repr(e))
    args = parse_arguments()

    temp_list = []

    for item in args.select.lower().split(","):
        if len(item.split(':')) >= 2:
            temp_list.append((item.split(':')[0], item.split(':')[1]))
        else:
            temp_list.append((item, None))
    select_args = OrderedDict(temp_list)

    args.select.split(',')
    order_by = args.order_by.lower().split(',')
    query = Query(select_args=select_args, order_by_args=order_by, filter_args=args.filter,
                  group_by_arg=args.group_by.lower())

    result = query.query()
    print(result)

