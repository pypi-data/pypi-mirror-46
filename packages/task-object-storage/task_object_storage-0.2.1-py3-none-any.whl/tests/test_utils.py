"""
Test TOS utility functions.
"""
import os
from bson.objectid import ObjectId
import pytest

from tos.utils import accept_string_object_ids, get_temporary_file


def test_accept_string_object_ids():
    object_id = ObjectId('5c502833cd9c9f7606120f14')

    class TestLibrary:
        @accept_string_object_ids
        def return_id(self, obj_id):
            return obj_id

    returned_id = TestLibrary().return_id(object_id)

    assert isinstance(returned_id, ObjectId)


def test_accept_string_object_ids_with_string():
    object_id = '5c502833cd9c9f7606120f14'

    class TestLibrary:
        @accept_string_object_ids
        def return_id(self, obj_id):
            return obj_id

    returned_id = TestLibrary().return_id(object_id)

    assert isinstance(returned_id, ObjectId)


def test_accept_string_object_ids_with_invalid_argument():
    object_id = callable

    class TestLibrary:
        @accept_string_object_ids
        def return_id(self, obj_id):
            return obj_id

    with pytest.raises(ValueError) as err:
        TestLibrary().return_id(object_id)

    assert "Second argument should be object id as string or ObjectId" in str(err)


def test_get_temporary_file():
    tmp_file = get_temporary_file()

    assert os.path.isfile(tmp_file)

    os.remove(tmp_file)
