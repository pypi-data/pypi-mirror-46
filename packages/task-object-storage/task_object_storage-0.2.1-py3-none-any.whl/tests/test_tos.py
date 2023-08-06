"""
Test TOS.
"""
import os
import sys

import pytest
import mongomock
from bson.binary import Binary

from tos.task_object_storage import TaskObjectStorage

DIRNAME = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(DIRNAME, "test_data")

MOCK_SERVER = "127.0.0.1"
MOCK_PORT = 27017


@pytest.fixture
def tos(mocker):
    def mocked_connect(*args):
        """Mock the mongo connect method"""
        return mongomock.MongoClient()

    mocker.patch('tos.task_object_storage.TaskObjectStorage.connect',
                 mocked_connect)

    # NOTE: Other option would be to use a real Mongo server
    # and mongomock.patch, see
    # https://github.com/mongomock/mongomock

    tos_object = TaskObjectStorage(
        db_server=f"{MOCK_SERVER}:{MOCK_PORT}",
        db_name="test_tos_db",
    )
    tos_object.initialize_tos()
    return tos_object


def test__insert_task_objectand_find_task_object(tos):
    """Test that the object status does not change."""
    object_to_insert = {
        "status": "new",
        "process_name": "test process",
        "priority": 0,
        "payload": {"data": 213213}
    }
    tos._insert_task_object(object_to_insert)
    object_id = object_to_insert["_id"]

    inserted_object = tos.find_task_object_by_id(object_id)

    assert inserted_object["_id"] == object_id
    assert inserted_object["status"] == object_to_insert["status"]
    assert inserted_object["process_name"] == object_to_insert["process_name"]
    assert inserted_object["priority"] == object_to_insert["priority"]
    assert inserted_object["payload"] == object_to_insert["payload"]


def test_create_new_task_object(tos):
    payload = {"data": 213213}
    process_name = "test_process"
    priority = 0
    tos.create_new_task_object(
        payload,
        process_name,
        priority=priority
    )

    inserted_object = tos.find_task_object_by_status_and_stage("new", 0)

    assert inserted_object["status"] == "new"
    assert inserted_object["process_name"] == process_name
    assert inserted_object["priority"] == priority
    assert inserted_object["payload"] == payload


def test_find_task_object_by_status_with_different_priorities(tos):
    """
    Test that the method returns the object
    with the highest priority when multiple objects
    are inserted.

    Note that the highest priority object is not
    created first or last.
    """
    payload = {"data": 213213}
    process_name = "test_process"
    priority = 10

    tos.create_new_task_object(
        {"data": 65646},
        "test_process",
        priority=0
    )
    tos.create_new_task_object(
        {"data": 7657},
        "test_process",
        priority=2
    )
    tos.create_new_task_object(
        payload,
        process_name,
        priority=priority
    )
    tos.create_new_task_object(
        {"data": 7657},
        "test_process",
        priority=0
    )

    obj = tos.find_task_object_by_status_and_stage("new", 0)

    assert obj["payload"] == payload
    assert obj["process_name"] == process_name
    assert obj["priority"] == 10
    assert obj["status"] == "new"


def test_update_task_object_priority(tos):
    initial_priority = 0
    changed_priority = 10
    object_to_insert = {
        "status": "new",
        "process_name": "test process",
        "priority": initial_priority,
        "payload": {"data": 213213}
    }
    tos._insert_task_object(object_to_insert)
    object_id = object_to_insert["_id"]

    inserted_object = tos.find_task_object_by_id(object_id)
    tos.update_task_object_priority(object_id, changed_priority)
    inserted_object_again = tos.find_task_object_by_id(object_id)

    assert inserted_object["priority"] == initial_priority
    assert inserted_object_again["priority"] == changed_priority


def test_update_task_object_payload(tos):
    initial_payload = {"data": 213213}
    changed_payload = {"data": 213213, "additional_data": 124}
    object_to_insert = {
        "status": "new",
        "process_name": "test process",
        "priority": 0,
        "payload": initial_payload
    }
    tos._insert_task_object(object_to_insert)
    object_id = object_to_insert["_id"]

    inserted_object = tos.find_task_object_by_id(object_id)
    tos.update_task_object_payload(object_id, changed_payload)
    inserted_object_again = tos.find_task_object_by_id(object_id)

    assert inserted_object["payload"] == initial_payload
    assert inserted_object_again["payload"] == changed_payload


def test__validate_status_text_valid_status(tos):
    status = "pass"
    tos._validate_status_text(status)


def test__validate_status_text_invalid_status(tos):
    status = "AWEFDSC"
    with pytest.raises(ValueError):
        tos._validate_status_text(status)


def test_find_task_object_by_status_and_stage_no_matches(tos):
    items = tos.find_task_object_by_status_and_stage("pass", 0)

    assert items is None


@pytest.fixture
def tos_with_inserted_object(tos):
    payload = {"data": 213213}
    process_name = "test_process"

    item = tos.create_new_task_object(
        payload,
        process_name,
    )

    return tos, item


def test_update_task_object_status(tos_with_inserted_object):
    tos, item = tos_with_inserted_object
    inserted_item = tos.find_task_object_by_id(item["_id"])
    old_status = "new"
    new_status = "processing"

    assert inserted_item["status"] == old_status

    tos.update_task_object_status(item["_id"], new_status)
    updated_item = tos.find_task_object_by_id(item["_id"])

    assert updated_item["status"] == new_status


def test_find_all_failed_task_objects(tos_with_inserted_object):
    tos, item = tos_with_inserted_object
    inserted_item = tos.find_task_object_by_id(item["_id"])

    assert inserted_item["status"] == "new"

    tos.update_task_object_status(item["_id"], "fail")
    failed_objects = tos.find_all_failed_task_objects()

    assert failed_objects[0]["status"] == "fail"

    failed_objects[0].pop("status")
    failed_objects[0].pop("updatedAt")
    item.pop("status")

    assert failed_objects[0] == item


def test_update_task_object_stage(tos_with_inserted_object):
    tos, item = tos_with_inserted_object
    inserted_item = tos.find_task_object_by_id(item["_id"])
    new_stage = 1

    assert inserted_item["stage"] == 0

    tos.update_task_object_stage(item["_id"], new_stage)
    updated_item = tos.find_task_object_by_id(item["_id"])

    assert updated_item["stage"] == new_stage


@pytest.fixture
def test_update_task_object_analytics(tos_with_inserted_object):
    tos, item = tos_with_inserted_object
    inserted_item = tos.find_task_object_by_id(item["_id"])
    new_analytics = {
        "marked_for_manual": True,
        "customer_type": 2
    }

    assert inserted_item["analytics"] == {}

    tos.update_task_object_analytics(item["_id"], new_analytics)
    updated_item = tos.find_task_object_by_id(item["_id"])

    assert updated_item["analytics"] == new_analytics

    return tos, item


def test_update_task_object_analytics_item(test_update_task_object_analytics):
    tos, item = test_update_task_object_analytics
    key = "marked_for_manual"
    new_value = False

    tos.update_task_object_analytics_item(item["_id"], key, new_value)
    updated_item = tos.find_task_object_by_id(item["_id"])

    assert updated_item["analytics"][key] == new_value


def test_add_binary_data_to_payload(tos_with_inserted_object):
    tos, item = tos_with_inserted_object
    test_pdf = os.path.join(TEST_DATA_DIR, "letter.pdf")
    pdf_title = "testi-pdf"

    tos.add_binary_data_to_payload(item["_id"], test_pdf, pdf_title)

    updated_item = tos.find_task_object_by_id(item["_id"])

    assert updated_item["payload"].get(pdf_title)
    assert isinstance(updated_item["payload"][pdf_title], Binary)


def test_delete_task_object(tos_with_inserted_object):
    tos, item = tos_with_inserted_object
    tos.delete_task_object(item["_id"])
    updated_item = tos.find_task_object_by_id(item["_id"])

    assert updated_item is None


def test_update_task_object_last_error(tos_with_inserted_object):
    tos, item = tos_with_inserted_object
    with pytest.raises(ZeroDivisionError) as err:
        1/0
    tos.update_task_object_last_error(item["_id"], str(err))

    updated_item = tos.find_task_object_by_id(item["_id"])

    assert "ZeroDivisionError" in updated_item["last_error"]
