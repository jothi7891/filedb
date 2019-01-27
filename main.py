from filedb.loader import Loader
from filedb.query import Filter, Query
import argparse

if __name__ == "__main__":

    loader = Loader()
    loader.load()

    result = (Filter(project='thehobbit') | Filter(shot='45')) & Filter(shot='45')

    print(result)
    query = Query(order_by_args=['internal_bid'], group_by_arg='', select_args={'project': None, 'version': 'collect',
                                                                                       'shot': 'count', 'internal_bid': None})
    query.query()

