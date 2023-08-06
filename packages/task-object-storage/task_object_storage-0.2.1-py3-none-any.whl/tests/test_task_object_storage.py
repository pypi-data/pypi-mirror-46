"""
Test task object storage module.
"""
import os

import pytest
import mongomock
from bson.binary import Binary

from tos.task_object_storage import TaskObjectStorage

DIRNAME = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(DIRNAME, "test_data")

MOCK_SERVER = "127.0.0.1"
MOCK_PORT = 16


@pytest.fixture
def tos(mocker):
    def mocked_connect(*args):
        """Mock the mongo connect method."""
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


def test__insert_task_object_and_find_task_object(tos):
    """Test that the object status does not change."""
    object_to_insert = {
        "status": "new",
        "priority": 0,
        "payload": {"data": 213213}
    }
    tos._insert_task_object(object_to_insert)
    object_id = object_to_insert["_id"]

    inserted_object = tos.find_task_object_by_id(object_id)

    assert inserted_object["_id"] == object_id
    assert inserted_object["status"] == object_to_insert["status"]
    assert inserted_object["priority"] == object_to_insert["priority"]
    assert inserted_object["payload"] == object_to_insert["payload"]


def test_create_new_task_object(tos):
    payload = {"data": 213213}
    priority = 0
    tos.create_new_task_object(
        payload,
        priority=priority
    )

    inserted_object = tos.find_one_task_object_by_status_and_stage("new", 0)

    assert inserted_object["status"] == "new"
    assert inserted_object["priority"] == priority
    assert inserted_object["payload"] == payload


def test_create_new_task_object_with_deprecated_process_name(tos, capsys):
    """Using process_name in task_object creation prints out a DeprecationWarning."""
    with pytest.warns(DeprecationWarning) as warn:
        tos.create_new_task_object(
            {"data": 213213},
            "process_name_not_needed",
            priority=0
        )

    assert "process_name should not be used anymore" in str(warn.list[0].message)

def test_find_one_task_object_by_status_and_stage_with_different_priorities(tos):
    """
    Test that the method returns the object
    with the highest priority when multiple objects
    are inserted.

    Note that the highest priority object is not
    created first or last.
    """
    payload = {"data": 213213}
    priority = 10

    tos.create_new_task_object(
        {"data": 65646},
        priority=0
    )
    tos.create_new_task_object(
        {"data": 7657},
        priority=2
    )
    tos.create_new_task_object(
        payload,
        priority=priority
    )
    tos.create_new_task_object(
        {"data": 7657},
        priority=0
    )

    obj = tos.find_one_task_object_by_status_and_stage("new", 0)

    assert obj["payload"] == payload
    assert obj["priority"] == 10
    assert obj["status"] == "new"


def test_find_one_task_object_by_status(tos):
    """
    Create two items with different stages but same status "new".
    Then create a third item with a different status "fail".

    Test getting both "new" items one at a time and only them.
    """

    item1 = tos.create_new_task_object(
        {"data": 65646},
    )
    item2 = tos.create_new_task_object(
        {"data": 7657},
    )
    item3 = tos.create_new_task_object(
        {"data": 7657},
    )
    tos.set_task_object_stage(item2["_id"], 1)
    tos.set_task_object_status(item2["_id"], "fail")

    to1 = tos.find_one_task_object_by_status("new")
    tos.set_task_object_status(to1["_id"], "pass")
    to2 = tos.find_one_task_object_by_status("new")
    tos.set_task_object_status(to2["_id"], "pass")

    assert not tos.find_one_task_object_by_status("new")


def test_set_task_object_priority(tos):
    initial_priority = 0
    changed_priority = 10
    object_to_insert = {
        "status": "new",
        "priority": initial_priority,
        "payload": {"data": 213213}
    }
    tos._insert_task_object(object_to_insert)
    object_id = object_to_insert["_id"]

    inserted_object = tos.find_task_object_by_id(object_id)
    tos.set_task_object_priority(object_id, changed_priority)
    inserted_object_again = tos.find_task_object_by_id(object_id)

    assert inserted_object["priority"] == initial_priority
    assert inserted_object_again["priority"] == changed_priority


def test_set_task_object_payload(tos):
    initial_payload = {"data": 213213}
    changed_payload = {"data": 213213, "additional_data": 124}
    object_to_insert = {
        "status": "new",
        "priority": 0,
        "payload": initial_payload
    }
    tos._insert_task_object(object_to_insert)
    object_id = object_to_insert["_id"]

    inserted_object = tos.find_task_object_by_id(object_id)
    tos.set_task_object_payload(object_id, changed_payload)
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


def test_find_one_task_object_by_status_and_stage_no_matches(tos):
    items = tos.find_one_task_object_by_status_and_stage("pass", 0)

    assert items is None


@pytest.fixture
def tos_with_inserted_object(tos):
    payload = {"data": 213213}

    item = tos.create_new_task_object(
        payload,
    )

    return tos, item


def test_set_task_object_status(tos_with_inserted_object):
    tos, item = tos_with_inserted_object
    inserted_item = tos.find_task_object_by_id(item["_id"])
    old_status = "new"
    new_status = "processing"

    assert inserted_item["status"] == old_status

    tos.set_task_object_status(item["_id"], new_status)
    updated_item = tos.find_task_object_by_id(item["_id"])

    assert updated_item["status"] == new_status


def test_find_all_failed_task_objects(tos_with_inserted_object):
    tos, item = tos_with_inserted_object
    inserted_item = tos.find_task_object_by_id(item["_id"])

    assert inserted_item["status"] == "new"

    tos.set_task_object_status(item["_id"], "fail")
    failed_objects = tos.find_all_failed_task_objects()

    assert failed_objects[0]["status"] == "fail"

    failed_objects[0].pop("status")
    failed_objects[0].pop("updatedAt")
    item.pop("status")

    assert failed_objects[0] == item


def test_set_task_object_stage(tos_with_inserted_object):
    tos, item = tos_with_inserted_object
    inserted_item = tos.find_task_object_by_id(item["_id"])
    new_stage = 1

    assert inserted_item["stage"] == 0

    tos.set_task_object_stage(item["_id"], new_stage)
    updated_item = tos.find_task_object_by_id(item["_id"])

    assert updated_item["stage"] == new_stage


@pytest.fixture
def test_set_task_object_analytics(tos_with_inserted_object):
    tos, item = tos_with_inserted_object
    inserted_item = tos.find_task_object_by_id(item["_id"])
    new_analytics = {
        "marked_for_manual": True,
        "customer_type": 2
    }

    assert inserted_item["analytics"] == {}

    tos.set_task_object_analytics(item["_id"], new_analytics)
    updated_item = tos.find_task_object_by_id(item["_id"])

    assert updated_item["analytics"] == new_analytics

    return tos, item


def test_set_task_object_analytics_item(test_set_task_object_analytics):
    tos, item = test_set_task_object_analytics
    key = "marked_for_manual"
    new_value = False

    tos.set_task_object_analytics_item(item["_id"], key, new_value)
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


def test_set_task_object_last_error(tos_with_inserted_object):
    tos, item = tos_with_inserted_object
    with pytest.raises(ZeroDivisionError) as err:
        1/0
    tos.set_task_object_last_error(item["_id"], str(err))

    updated_item = tos.find_task_object_by_id(item["_id"])

    assert "ZeroDivisionError" in updated_item["last_error"]


def test_initializing_with_no_mongo_running():
    """Use real non-mocked TOS here to access the method.

    There should not be a running mongo server!
    """
    with pytest.raises(Exception) as err:
        tos_object = TaskObjectStorage(
            db_server=f"{MOCK_SERVER}:{MOCK_PORT}",
            db_name="test_tos_db",
            timeout=0.1  # low timeout because we know this should fail anyway
        )

    assert "Is MongoDB running?" in str(err)


def test_initializing_with_no_mongo_running_with_authentication():
    """Use real non-mocked TOS here to access the method.

    There should not be a running mongo server!
    """
    with pytest.raises(Exception) as err:
        tos_object = TaskObjectStorage(
            db_server=f"{MOCK_SERVER}:{MOCK_PORT}",
            db_name="test_tos_db",
            db_user="test_user",
            db_passw="test_passw",
            timeout=0.1  # low timeout because we know this should fail anyway
        )

    assert "Is MongoDB running?" in str(err)


def test_context_managed_task_object_storage(mocker):

    def mocked_connect(*args):
        """Mock the mongo connect method"""
        return mongomock.MongoClient()

    mocker.patch('tos.task_object_storage.TaskObjectStorage.connect',
                 mocked_connect)

    with TaskObjectStorage(
        db_server=f"{MOCK_SERVER}:{MOCK_PORT}",
        db_name="test_tos_db",
    ) as tos:
        assert tos._check_connection_established(tos.client)

    # NOTE: mongomock.MongoClient().close() doesn't do anything
    # so it's hard to test the disconnect method without real
    # mongodb instance.


def test_save_binary_payload_to_tmp(tos):
    test_pdf = os.path.join(TEST_DATA_DIR, "letter.pdf")
    to = {
        "status": "new",
        "priority": 0,
        "payload": {
            "data": 213213,
            "test-pdf": tos.encode_binary_data(test_pdf),
        }
    }

    tmp_file = tos.save_binary_payload_to_tmp(to, "test-pdf")

    assert isinstance(to["payload"]["test-pdf"], Binary)
    assert os.path.isfile(tmp_file)

    os.remove(tmp_file)


def test_update_payload(tos):
    initial_payload = {"data": 213213}
    new_data = {
        "new_data": "xxxx",
        "more_new_data": "yyy"
    }

    to = {
        "status": "new",
        "priority": 0,
        "payload": initial_payload
    }

    tos._insert_task_object(to)
    object_id = to["_id"]

    inserted_object = tos.find_task_object_by_id(object_id)
    _ = tos.update_payload(object_id, new_data)
    inserted_object_again = tos.find_task_object_by_id(object_id)

    assert inserted_object["payload"] == initial_payload
    assert inserted_object_again["payload"] == {**initial_payload, **new_data}


def test_update_payload_with_error(tos):
    initial_payload = {"data": 213213}
    new_data = ("new_data", "xxxx")

    to = {
        "status": "new",
        "priority": 0,
        "payload": initial_payload
    }

    tos._insert_task_object(to)
    object_id = to["_id"]

    # pytest.set_trace()

    with pytest.raises(TypeError) as err:
        _ = tos.update_payload(object_id, new_data)

    assert "Argument update should be a dict" in str(err)


def test_find_one_task_object_marked_as_manual_and_not_passed(tos):

    expected_payload = {"data": 65646}
    item1 = tos.create_new_task_object(
        expected_payload,
    )
    item2 = tos.create_new_task_object(
        {"data": 7657},
    )

    with pytest.warns(DeprecationWarning) as warn:
        tos.set_task_object_to_manual_handling(item1["_id"])
        to1 = tos.find_one_task_object_marked_as_manual_and_not_passed()
        tos.set_task_object_status(to1["_id"], "pass")

        to2 = tos.find_one_task_object_marked_as_manual_and_not_passed()

        assert to1["payload"] == expected_payload
        assert not to2

    assert "Use status instead of manual field" in str(warn.list[0].message)


def test_increment_and_decrement_task_object_stage(tos_with_inserted_object):
    tos, item = tos_with_inserted_object

    tos.increment_task_object_stage(item["_id"])
    item_after_increment = tos.find_task_object_by_id(item["_id"])
    tos.decrement_task_object_stage(item["_id"])
    item_after_decrement = tos.find_task_object_by_id(item["_id"])

    assert item["stage"] == 0
    assert item_after_increment["stage"] == 1
    assert item_after_decrement["stage"] == 0


def test_set_task_object_for_rerun(tos_with_inserted_object):
    tos, item = tos_with_inserted_object

    tos.set_task_object_stage(item["_id"], 2)
    tos.set_task_object_status(item["_id"], "fail")
    item_after_failure = tos.find_task_object_by_id(item["_id"])
    tos.set_task_object_for_rerun(item["_id"])

    item_after_reset = tos.find_task_object_by_id(item["_id"])

    assert item_after_failure["status"] == "fail"
    assert item_after_failure["stage"] == 2
    assert item_after_failure["retry_count"] == 0
    assert item_after_reset["status"] == "pass"
    assert item_after_reset["stage"] == 1
    assert item_after_reset["retry_count"] == 1


def test_find_all_task_objects_by_status_and_stage_multiple_stages(tos):
    item1 = tos.create_new_task_object(
        {"data": 65646},
    )
    item2 = tos.create_new_task_object(
        {"data": 7657},
    )
    item3 = tos.create_new_task_object(
        {},
    )

    tos.set_task_object_stage(item2["_id"], 2)
    tos.set_task_object_stage(item3["_id"], 3)

    objects = tos.find_all_task_objects_by_status_and_stage("new", [0, 2, 3])

    assert len(objects) == 3


def test_find_all_task_objects_by_status_and_stage_multiple_statuses(tos):
    item1 = tos.create_new_task_object(
        {"data": 65646},
    )
    item2 = tos.create_new_task_object(
        {"data": 7657},
    )
    item3 = tos.create_new_task_object(
        {},
    )

    tos.set_task_object_status(item2["_id"], "fail")
    tos.set_task_object_status(item3["_id"], "processing")

    objects = tos.find_all_task_objects_by_status_and_stage(["new", "fail", "processing"])

    assert len(objects) == 3


def test_find_all_task_objects_by_stage(tos):
    item1 = tos.create_new_task_object(
        {"data": 65646},
    )
    item2 = tos.create_new_task_object(
        {"data": 7657},
    )
    item3 = tos.create_new_task_object(
        {},
    )

    tos.set_task_object_stage(item2["_id"], 1)
    tos.set_task_object_stage(item3["_id"], 2)

    objects = tos.find_all_task_objects_by_stage([0, 1])

    assert len(objects) == 2


def test_find_all_task_objects_by_status_and_stage_invalid_arguments(tos):
    with pytest.raises(TypeError) as err:
        tos.find_all_task_objects_by_status_and_stage()

    assert "Pass statuses or stages or both." in str(err)


def test_find_one_task_object_by_status_and_stage_invalid_arguments(tos):
    with pytest.raises(TypeError) as err:
        tos.find_one_task_object_by_status_and_stage()

    assert "Pass statuses or stages or both." in str(err)


def test__create_status_query_invalid_arguments(tos):
    with pytest.raises(TypeError) as err:
        tos._create_status_query({})

    assert "Pass status as a string or a sequence of strings" in str(err)


def test__create_stage_query_invalid_arguments(tos):
    with pytest.raises(TypeError) as err:
        tos._create_stage_query({})

    assert "Pass stages as an int or a sequence of ints." in str(err)


def test_find_one_task_object_by_stage(tos):
    item1 = tos.create_new_task_object(
        {"data": 65646},
    )
    item2 = tos.create_new_task_object(
        {"data": 7657},
    )

    tos.set_task_object_stage(item2["_id"], 2)

    to = tos.find_one_task_object_by_stage(2)

    assert to


@pytest.mark.xfail
def test_validation(tos_with_inserted_object):
    """Mongomock does not support validation.

    It raises NotImplementedError when passing kwargs
    to db.create_collection
    """
    tos, item = tos_with_inserted_object
    raise NotImplementedError


def test_push_value_to_array_field(tos_with_inserted_object):
    tos, item = tos_with_inserted_object
    alert_text = "2 transactions confirmed"

    tos.push_value_to_array_field(item["_id"], alert_text, "payload.alerts")
    to = tos.find_task_object_by_id(item["_id"])

    assert to["payload"]["alerts"][0] == alert_text
