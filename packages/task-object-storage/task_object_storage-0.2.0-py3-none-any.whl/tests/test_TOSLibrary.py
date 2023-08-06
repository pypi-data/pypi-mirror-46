"""
Test TOSLibrary class
"""
import os
import sys

import pytest
import mongomock
# from bson.binary import Binary

from tos.task_object_storage import TaskObjectStorage
import TOSLibrary

DIRNAME = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(DIRNAME, "test_data")

MOCK_SERVER = "127.0.0.1"
MOCK_PORT = 16


@pytest.fixture
def mocked_collection():
    obj = {"stage": 0, "status": "pass"}
    collection = mongomock.MongoClient().db.collection
    obj['_id'] = collection.insert_one(obj)
    return collection


@pytest.fixture
def mocked_TOSLibrary(mocker, mocked_collection):
    """
    Simple test to initialize TOSLibrary.

    Everything here is mocked though.
    """
    def mocked_connect(*args):
        """Mock the mongo connect method"""
        return mongomock.MongoClient()

    def mocked_check_connection_established(*args):
        """Mock the mongo connect method"""
        return

    mocker.patch('TOSLibrary.TaskObjectStorage.connect',
                 mocked_connect)
    mocker.patch('TOSLibrary.TaskObjectStorage._check_connection_established',
                 mocked_check_connection_established)

    toslib = TOSLibrary.TOSLibrary(
        db_server=f"{MOCK_SERVER}:{MOCK_PORT}",
        db_name="test_tos_db",
        db_user="test_user",
        db_passw="test_passw",
    )

    # patch TaskObjectStorage.tos to be a mock collection
    mocker.patch.object(toslib.tos, "tos", mocked_collection)

    return toslib


def test_TOSLibrary(mocked_TOSLibrary):
    toslib = mocked_TOSLibrary
    keywords = set(toslib.keywords.keys())
    instance_attributes = set(dir(toslib))

    assert keywords.issubset(instance_attributes)
