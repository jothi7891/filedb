import argparse
from filedb.query import Filter, Query
from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--select', required=False, help="Columns to be selected in the displayed",
                        type=str)
    parser.add_argument('-o', '--order_by', required=False, type=str,
                        help="Order by columns")
    parser.add_argument('-g', '--group_by', required=False, type=str,
                        help="group by column", default=None)
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
    if args.select:
        for item in args.select.lower().split(","):
            if len(item.split(':')) >= 2:
                temp_list.append((item.split(':')[0], item.split(':')[1]))
            else:
                temp_list.append((item, None))
    select_args = OrderedDict(temp_list)

    order_by = []
    if args.order_by:
        order_by = args.order_by.lower().split(',')

    group_by = None
    if args.group_by:
        group_by = args.group_by.lower()

    query = Query(select_args=select_args, order_by_args=order_by, filter_args=args.filter,
                  group_by_arg=group_by)

    result = query.query()
    print(result)

