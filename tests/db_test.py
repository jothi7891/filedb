from filedb.loader import Loader
import json
from tempfile import NamedTemporaryFile
import pytest
import os


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
                  "the hobbit|45|64|scheduled|2010-05-20|45.00|2010-04-01 13:35",
                  "the hobbit|45|64|scheduled|2010-05-20|45.00|2010-04-01 13:35"]
    input_str = os.linesep.join(input_list)
    tempfile.write(input_str)
    tempfile.flush()

    def finalizer():
        tempfile.close()
    request.addfinalizer(finalizer)
    return tempfile


@pytest.fixture(scope="function")
def loader(input1):
    db_file = NamedTemporaryFile().name
    unprocessed_file = NamedTemporaryFile().name
    input_file = input1.name
    loader = Loader(db_file=db_file, input_file=input_file, unprocessed_file=unprocessed_file)
    return loader


def test_db_normal_load(loader):
    loader.load()
    expected_dict = {"the hobbit-45-64": {
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

    actual_dict = loader.db._read()
    assert expected_dict == actual_dict


def test_db_overwrite_load(loader, input2):
    loader.input_file = input2.name
    loader.load()
    expected_dict = {"the hobbit-45-64": {
                                            "created_date": "2010-04-01 13:35",
                                            "finish_date": "2010-05-20",
                                            "internal_bid": 45.0,
                                            "project": "the hobbit",
                                            "shot": "45",
                                            "status": "scheduled",
                                            "version": 64}
                    }

    actual_dict = loader.db._read()
    assert expected_dict == actual_dict
