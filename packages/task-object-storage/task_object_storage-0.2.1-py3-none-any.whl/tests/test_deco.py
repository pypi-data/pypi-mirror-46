"""
Test the decorators.
"""
import pytest
import robot

from bson.objectid import ObjectId
from testfixtures import LogCapture

from TOSLibrary.deco import (
    log_number_of_task_objects,
    handle_errors,
    _take_screenshot,
)
from TOSLibrary.exceptions import BusinessException, CannotCreateTaskObject

# DIRNAME = os.path.dirname(os.path.abspath(__file__))
# PACKAGE_ROOT = os.path.abspath(os.path.join(DIRNAME, os.pardir))
# sys.path.append(os.path.join(PACKAGE_ROOT, "TOSLibrary"))


def test_log_number_of_task_objects():
    @log_number_of_task_objects
    def test_func():
        return 10

    with LogCapture() as logs:
        value = test_func()

    assert value == 10
    assert str(logs) == "RobotFramework INFO\n  10 task object(s) processed"


def test_log_number_of_task_objects_no_objects():
    @log_number_of_task_objects
    def test_func():
        return 0

    with LogCapture() as logs:
        value = test_func()

    assert value == 0
    assert str(logs) == "RobotFramework WARNING\n  No task objects processed"


def test_handle_errors_when_pass():
    """
    Currently this test cannot be run.

    TODO: Investigate how to test
    TOSLibrary initialization in Robot Framework or refactor the
    decorator itself.
    """
    to = {
        "_id": ObjectId("5c4710b1ad68bf2aa4994350"),
        "status": "pass",
        "stage": 4,
        "process_name": "read_excels",
        "priority": 0,
        "payload": {}
    }

    class Test:
        @handle_errors("Test errors")
        def test_func(self, to):
            return to

    value, status = Test().test_func(to=to)
    assert status == "pass"


def test_handle_errors_when_fail():
    to = {
        "_id": ObjectId("5c4710b1ad68bf2aa4994350"),
        "status": "pass",
        "stage": 4,
        "process_name": "read_excels",
        "priority": 0,
        "payload": {}
    }
    expected_message = "Test errors"

    class Test:
        @handle_errors(expected_message)
        def test_func(self, to):
            raise RuntimeError

    with LogCapture() as logs:
        value, status = Test().test_func(to=to)
    assert status == "fail"
    assert expected_message in str(logs)


def test_handle_errors_when_not_implemented():
    to = {
        "_id": ObjectId("5c4710b1ad68bf2aa4994350"),
        "status": "pass",
        "stage": 4,
        "process_name": "read_excels",
        "priority": 0,
        "payload": {}
    }

    expected_message = "Test errors2"

    class Test:
        @handle_errors(expected_message)
        def test_func(self, to):
            raise NotImplementedError(expected_message)

    with pytest.raises(NotImplementedError) as err:
        Test().test_func(to=to)

    assert expected_message in str(err)


def test_handle_errors_when_business_exception():
    to = {
        "_id": ObjectId("5c4710b1ad68bf2aa4994350"),
        "status": "pass",
        "stage": 4,
        "process_name": "read_excels",
        "priority": 0,
        "payload": {}
    }

    expected_message = "Business error"

    class Test:
        @handle_errors(expected_message)
        def test_func(self, to):
            raise BusinessException(expected_message)

    with LogCapture() as logs:
        value, status = Test().test_func(to=to)

    assert status == "fail"
    assert expected_message in str(logs)


def test_handle_errors_message_as_instance_attribute():
    to = {
        "_id": ObjectId("5c4710b1ad68bf2aa4994350"),
        "status": "pass",
        "stage": 4,
        "process_name": "read_excels",
        "priority": 0,
        "payload": {}
    }
    expected_message = "Error message from instance"

    class Test:
        def __init__(self):
            self.error_msg = expected_message

        @handle_errors()
        def test_func(self, to):
            # self.error_msg = expected_message  # this doesn't work!
            raise RuntimeError

    with LogCapture() as logs:
        value, status = Test().test_func(to=to)

    assert status == "fail"
    assert expected_message in str(logs)


def test_handle_errors_when_no_input_data_available():
    expected_message = "Data could not be fetched"

    class Test:
        @handle_errors()
        def test_func(self):
            raise CannotCreateTaskObject(expected_message)

    with LogCapture() as logs:
        data, status = Test().test_func()

    assert status == "fail"
    assert expected_message in str(logs)


@pytest.mark.xfail
def test_handle_errors_no_task_object_passed():
    """
    This will fail because passing ``to`` inside the decorator
    is not enforced anymore.

    TODO: Consider if this test should be removed.
    """
    to = {
        "_id": ObjectId("5c4710b1ad68bf2aa4994350"),
        "status": "pass",
        "stage": 4,
        "process_name": "read_excels",
        "priority": 0,
        "payload": {}
    }
    expected_message = "Task object must be passed as a keyword argument"

    class Test:
        @handle_errors()
        def test_func(self, to):
            return None

    with pytest.raises(ValueError) as err:
        _ = Test().test_func([1, 2, 3])

    assert expected_message in str(err)


def test__take_screenshot_rf_not_running():
    with LogCapture() as logs:
        _take_screenshot()

    assert "Robot needs to be running for screenshotting to work" in str(logs)
