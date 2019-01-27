from filedb.loader import Loader
from filedb.query import Query
from collections import OrderedDict
from tempfile import NamedTemporaryFile
import pytest
import os
import logging


logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def remove_file(request):
    print("its a dummy fixture")

    def finalizer():
        os.remove("tests/db.json")
    request.addfinalizer(finalizer)
    return


@pytest.fixture(scope="function")
def tempfile():
    file = NamedTemporaryFile('w')
    return file


@pytest.fixture(scope="function")
def input1(tempfile, request):
    input_list = ["PROJECT|SHOT|VERSION|STATUS|FINISH_DATE|INTERNAL_BID|CREATED_DATE",
                  "the hobbit|45|64|scheduled|2010-05-20|45.00|2010-04-01 13:35",
                  "the hobbit|52|64|scheduled|2010-05-20|45.00|2010-04-01 13:35"]
    input_str = os.linesep.join(input_list)
    tempfile.write(input_str)
    tempfile.flush()

    def finalizer():
        tempfile.close()
    request.addfinalizer(finalizer)
    return tempfile

@pytest.fixture(scope="function")
def input2(tempfile, request):
    input_list = ["PROJECT|SHOT|VERSION|STATUS|FINISH_DATE|INTERNAL_BID|CREATED_DATE",
                  "the hobbit|50|64|scheduled|2010-05-20|45.00|2010-04-01 13:35",
                  "the hobbit|50|64|scheduled|2010-05-20|45.00|2010-04-01 13:35"]
    input_str = os.linesep.join(input_list)
    tempfile.write(input_str)
    tempfile.flush()

    def finalizer():
        tempfile.close()
    request.addfinalizer(finalizer)
    return tempfile

@pytest.fixture(scope="function")
def input3(tempfile, request):
    input_list = ["PROJECT|SHOT|VERSION|STATUS|FINISH_DATE|INTERNAL_BID|CREATED_DATE",
                  "the avengers|50|64|scheduled|2010-05-20|45.00|2010-04-01 13:35"]
    input_str = os.linesep.join(input_list)
    tempfile.write(input_str)
    tempfile.flush()

    def finalizer():
        tempfile.close()
    request.addfinalizer(finalizer)
    return tempfile

@pytest.fixture(scope="function")
def input4(tempfile, request):
    input_list = ["PROJECT|SHOT|VERSION|STATUS|FINISH_DATE|INTERNAL_BID|CREATED_DATE",
                  "the hobbit|50|64|scheduled|2010-05-20|45.00|2010-04-01 13:35",
                  "avengers|45|64|scheduled|2010-05-20|45.00|2010-04-01 13:35",
                  "spiderman|03|16|finished|2001-10-15|45.00|2001-04-01 06:47",
                  "superman|42|128|scheduled|2006-07-22|25|2006-08-04 07:22",
                  "king kong|42|128|notrequired|2006-07-22|35.00|2006-10-15 09:14",
                  "king kong|65|128|notrequired|2006-07-22|30.00|2008-10-15 09:14"]

    input_str = os.linesep.join(input_list)
    tempfile.write(input_str)
    tempfile.flush()

    def finalizer():
        tempfile.close()
    request.addfinalizer(finalizer)
    return tempfile

@pytest.fixture(scope="function")
def query1():
    query = Query(db_file="tests/db.json")
    return query

@pytest.fixture(scope="function")
def query2():
    query = Query(db_file="tests/db.json", select_args=OrderedDict([("project", None), ("internal_bid", "count")]),
                  group_by_arg="project", order_by_args=['finish_date'],
                  filter_args="PROJECT='the hobbit' OR PROJECT='king kong'")
    return query


@pytest.fixture(scope="function")
def loader(input1):
    db_file = "tests/db.json"
    unprocessed_file = NamedTemporaryFile().name
    input_file = input1.name
    loader = Loader(db_file=db_file, input_file=input_file, unprocessed_file=unprocessed_file)
    return loader


@pytest.fixture(scope="function")
def loader_init(input3):
    db_file = "tests/db.json"
    unprocessed_file = NamedTemporaryFile().name
    input_file = input3.name
    loader = Loader(db_file=db_file, input_file=input_file, unprocessed_file=unprocessed_file, init=True)
    return loader


@pytest.fixture(scope="function")
def query_loader(input4):
    db_file = "tests/db.json"
    unprocessed_file = NamedTemporaryFile().name
    input_file = input4.name
    loader = Loader(db_file=db_file, input_file=input_file, unprocessed_file=unprocessed_file, init=True)
    loader.load()
    loader.db.close()
    return loader


def test_db_normal_load(loader, remove_file):
    loader.load()
    expected_result = {"the hobbit-45-64": {
                                            "created_date": "2010-04-01 13:35",
                                            "finish_date": "2010-05-20",
                                            "internal_bid": 45.0,
                                            "project": "the hobbit",
                                            "shot": "45",
                                            "status": "scheduled",
                                            "version": 64},
        "the hobbit-52-64": {
            "created_date": "2010-04-01 13:35",
            "finish_date": "2010-05-20",
            "internal_bid": 45.0,
            "project": "the hobbit",
            "shot": "52",
            "status": "scheduled",
            "version": 64}
    }

    actual_result = loader.db._read()
    assert expected_result == actual_result


def test_db_overwrite_load(loader, input2, remove_file):
    loader.input_file = input2.name
    loader.load()
    expected_result = {"the hobbit-45-64": {
                                            "created_date": "2010-04-01 13:35",
                                            "finish_date": "2010-05-20",
                                            "internal_bid": 45.0,
                                            "project": "the hobbit",
                                            "shot": "45",
                                            "status": "scheduled",
                                            "version": 64},
        "the hobbit-52-64": {
            "created_date": "2010-04-01 13:35",
            "finish_date": "2010-05-20",
            "internal_bid": 45.0,
            "project": "the hobbit",
            "shot": "52",
            "status": "scheduled",
            "version": 64},
        "the hobbit-50-64": {
                                            "created_date": "2010-04-01 13:35",
                                            "finish_date": "2010-05-20",
                                            "internal_bid": 45.0,
                                            "project": "the hobbit",
                                            "shot": "50",
                                            "status": "scheduled",
                                            "version": 64}
                    }

    actual_result = loader.db._read()
    assert expected_result == actual_result


def test_db_loader_init(loader_init, remove_file):
    loader_init.load()
    expected_result = {"the avengers-50-64": {
                                            "created_date": "2010-04-01 13:35",
                                            "finish_date": "2010-05-20",
                                            "internal_bid": 45.0,
                                            "project": "the avengers",
                                            "shot": "50",
                                            "status": "scheduled",
                                            "version": 64}
                    }
    actual_result = loader_init.db._read()
    assert expected_result == actual_result


def test_db_query1(query_loader, query1, remove_file):
    actual_result = query1.query()
    expected_result = ["notrequired    2006-07-22     128            42             2006-10-15 09:1435.0           king kong",
                       "notrequired    2006-07-22     128            42             2006-10-15 09:1435.0           king kong",
                        "scheduled      2010-05-20     64             45             2010-04-01 13:3545.0           Avengers",
                        "scheduled      2006-07-22     128            42             2006-08-04 07:2225.0           superman",
                        "finished       2001-10-15     16             03             2001-04-01 06:4745.0           spiderman",
                        "scheduled      2010-05-20     64             50             2010-04-01 13:3545.0           the hobbit"]
    actual_result_list = actual_result.split('\n')
    assert len(actual_result_list) == len(expected_result) + 2

def test_db_query2(query_loader, query2, remove_file):
    actual_result = query2.query()
    expected_result = ["PROJECT        INTERNAL_BID   ","king kong      2              ", "the hobbit     1              ",
                       '']
    actual_result_list = actual_result.split('\n')
    logger.info(actual_result)
    assert actual_result_list == expected_result

