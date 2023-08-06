"""
Task Object Storage module.

Note that this module has no Robot Framework
dependencies, i.e. can be used with pure
Python applications.
"""
import os
import platform
import warnings
from datetime import datetime

import pymongo
from bson.binary import Binary

from .settings import (
    DEFAULT_DB_ADDRESS,
    VALID_STATUSES,
    VALIDATOR
)
from .utils import (
    accept_string_object_ids,
    get_temporary_file,
)


class TaskObjectStorage:

    def __init__(self, **options):
        """
        :param options: A dictionary of MongoDB options for the
         database server URL and port, and the process database
         name, username and password.

        The following is a list of accepted options as keyword arguments:

        :param db_server: Mongodb server uri and optional port, e.g. 'localhost:27017'
        :type db_server: str
        :param db_name: Database name.
        :type db_name: str
        :param db_user: Database username.
        :type db_user: str
        :param db_passw: Database password.
        :type db_passw: str
        :param db_auth_source: Authentication database.
        :type db_auth_source: str

        Example usage:

        .. code-block:: python

            tos = TaskObjectStorage(
                    db_server="localhost:27017",
                    db_name="testing",
                    db_auth_source="admin",
                    db_user="robo-user",
                    db_passw="secret-word",
            )

        where ``db_auth_source`` is the same as ``db_name`` by default.

        """
        self.options = options
        self.client = self.connect()
        self._check_connection_established(self.client)
        self.tos = None  # TOS collection

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        """Connect to MongoDB.

        :returns: MongoDB client object.
        :rtype: pymongo.MongoClient
        """
        server = self.options.get("db_server") or DEFAULT_DB_ADDRESS
        if self.options.get("db_passw"):
            client = pymongo.MongoClient(
                host=server,
                authSource=self.options.get("db_auth_source") or self.options["db_name"],
                authMechanism="SCRAM-SHA-1",
                username=self.options["db_user"],
                password=self.options["db_passw"],
                serverSelectionTimeoutMS=self.options.get("timeout", 10000),
            )
        else:
            client = pymongo.MongoClient(
                host=server,
                serverSelectionTimeoutMS=self.options.get("timeout", 10000),
            )

        return client

    def disconnect(self):
        self.client.close()

    def _check_connection_established(self, client):
        """Get active nodes (DB servers).

        :raises: ServerSelectionTimeoutError if no
                 connections active.
        """
        try:
            return client.server_info()
        except pymongo.errors.ServerSelectionTimeoutError as err:
            raise Exception("Is MongoDB running?") from err

    def initialize_tos(self, validate=False):
        """Initialize Mongo database and collection objects."""
        database = self.client[self.options["db_name"]]
        if validate:
            # TODO: validation seems not to work
            self.tos = database.create_collection("task_objects", validator=VALIDATOR)
        else:
            self.tos = database["task_objects"]

    def create_new_task_object(self, payload, process_name="", priority=0):
        """
        Create a new task object and insert into database.

        :param payload: The contents of the actual task object
        :type payload: dict
        :param priority: Priority of the task object, default=0.
        :type priority: int
        :param process_name: Name of the process.
        :type process_name: str
        :returns: The created task object.
        :rtype: dict

        Usage:

        >>> payload = {"customer_number": 583459089}
        >>> create_new_task_object(payload)
        {
            "_id": ObjectId("5c519c08cd9c9f140f95b427"),
            "status": "new",
            "stage": 0,
            "priority": 0,
            "executor": ""
            "payload": {
                "customer_number": 583459089
            }
            "analytics": {},
        }

        """
        initial_status = "new"
        initial_stage = 0  # the producer stage
        initial_error = None
        initial_retry_count = 0
        initial_executor = ""
        task_object = {
            "status": initial_status,
            "stage": initial_stage,
            "priority": priority,
            "payload": payload,
            "analytics": {},
            "last_error": initial_error,
            "retry_count": initial_retry_count,
            "executor": initial_executor,
        }
        if process_name:
            warnings.warn("process_name should not be used anymore", DeprecationWarning)
            task_object["process_name"] = process_name  # deprecate this

        inserted = self._insert_task_object(task_object)
        task_object["_id"] = inserted.inserted_id

        return task_object

    def _insert_task_object(self, task_object):
        return self.tos.insert_one(task_object)

    @accept_string_object_ids
    def find_task_object_by_id(self, object_id):
        """
        Get a single task object.

        This doesn't change the status of the task object.

        :param object_id: the object id
        :type object_id: ObjectId or str
        :returns: task object
        :rtype: dict
        """
        return self.tos.find_one({"_id": object_id})

    def find_one_task_object_by_status(self, statuses):
        """Convenience method."""
        return self.find_one_task_object_by_status_and_stage(statuses=statuses)

    def find_one_task_object_by_stage(self, stages):
        """Convenience method."""
        return self.find_one_task_object_by_status_and_stage(stages=stages)

    def find_one_task_object_by_status_and_stage(self, statuses=None, stages=None):
        """
        Get one of the task objects by status and (optionally) by stage.

        The status of the task object is **always** set to processing when
        using this keyword.

        The filtered results are sorted by priority in descending order so an
        item with the hightest priority will be returned.

        :param statuses: status(es)
        :type statuses: str or list of strs
        :param stages: stage number(s)
        :type stages: int or list of ints
        :raises TypeError: when invalid keyword arguments passed

        :returns: task object with the hightest priority.
        :rtype: dict
        """
        if statuses is stages is None:
            raise TypeError("Pass statuses or stages or both.")

        query = self._create_query(statuses, stages)
        task_object = self.tos.find_one_and_update(
            query,
            {"$set": {"status": "processing"}},
            sort=[("priority", pymongo.DESCENDING)]
        )

        if task_object:
            self.set_task_object_executor(task_object["_id"])

        return task_object

    def find_all_failed_task_objects(self):
        """Convenience method."""
        return self.find_all_task_objects_by_status("fail")

    def find_all_task_objects_by_status(self, statuses):
        """Convenience method."""
        return self.find_all_task_objects_by_status_and_stage(statuses=statuses)

    def find_all_task_objects_by_stage(self, stages):
        """Convenience method."""
        return self.find_all_task_objects_by_status_and_stage(stages=stages)

    def find_all_task_objects_by_status_and_stage(self, statuses=None, stages=None):
        """Get all task objects by status and stage.

        The returned list is sorted by priority in descending order so the
        hightest priority item is always the first.

        :param statuses: status(es)
        :type statuses: str or list of strs
        :param stages: stage number(s)
        :type stages: int or list of ints
        :raises TypeError: when invalid keyword arguments passed
        :returns: list of task objects
        :rtype: list

        Usage:

        >>> find_all_task_objects_by_status_and_stage("pass", 1)
        """
        if statuses is stages is None:
            raise TypeError("Pass statuses or stages or both.")

        query = self._create_query(statuses, stages)
        task_objects = self.tos.find(query).sort([("priority", -1), ])

        return list(task_objects)

    def _create_query(self, statuses=None, stages=None):
        """Dynamically create a MongoDB query with given search parameters.

        :param statuses: status(es)
        :type statuses: str or list of strs
        :param stages: stage number(s)
        :type stages: int or list of ints
        :returns: MongoDB query
        :rtype: str
        """
        if statuses and stages is None:  # 0 is a valid stage
            query = self._create_status_query(statuses)
        elif not statuses and stages is not None:
            query = self._create_stage_query(stages)
        else:
            query = {
                "$and": [
                    self._create_status_query(statuses),
                    self._create_stage_query(stages)
                ]
            }

        return query

    def _create_status_query(self, statuses):
        if isinstance(statuses, str):
            return {"status": {"$eq": statuses}}
        elif isinstance(statuses, (list, tuple)):
            return {"$or": [{"status": {"$eq": status}} for status in statuses]}
        else:
            raise TypeError("Pass status as a string or a sequence of strings.")

    def _create_stage_query(self, stages):
        if isinstance(stages, int):
            return {"stage": {"$eq": stages}}
        elif isinstance(stages, (list, tuple)):
            return {"$or": [{"stage": {"$eq": stage}} for stage in stages]}
        else:
            raise TypeError("Pass stages as an int or a sequence of ints.")

    def find_one_task_object_marked_as_manual_and_not_passed(self):
        """
        Get one of the task objects marked as manual.

        The list returned by `find_all_task_objects_marked_as_manual_and_not_passed`
        is sorted by priority so the hightest priority item is
        always the first.

        :returns: manual task object with the hightest priority.
        :rtype: dict
        """
        # TODO: Deprecate this method
        warnings.warn("Use status instead of manual field", DeprecationWarning)
        task_objects = self.find_all_task_objects_marked_as_manual_and_not_passed()
        if not task_objects:
            return None
        one_object = task_objects[0]

        return one_object

    def find_all_task_objects_marked_as_manual_and_not_passed(self):
        """
        Get all task objects marked to manual handling.

        :returns: list of task objects
        :rtype: list
        """
        # TODO: Deprecate this method
        warnings.warn("Use status instead of manual field", DeprecationWarning)
        task_objects = self.tos.find(
            {"manual": {"$eq": True},
             "status": {"$ne": "pass"}}
        ).sort([("priority", -1), ])

        return list(task_objects)

    @accept_string_object_ids
    def set_task_object_status(self, object_id, status):
        """
        Set the task object status to one of the accepted values.

        Accepted values are in :attr:`settings.VALID_STATUSES`

        :param object_id: Object id.
        :type object_id: str or ObjectId
        :param status: status text
        :type status: str
        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`
        """
        self._validate_status_text(status)
        return self._set_task_object_item(object_id, "status", status)

    def _validate_status_text(self, status):
        # TODO: use MongoDB schema validation instead of this
        if status not in VALID_STATUSES:
            raise ValueError("Trying to set invalid status")

    @accept_string_object_ids
    def set_task_object_stage(self, object_id, stage: int):
        """
        :param object_id: Object id
        :type object_id: str or ObjectId
        :param stage: target stage
        :type stage: int

        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`
        """
        return self._set_task_object_item(object_id, "stage", stage)

    @accept_string_object_ids
    def set_task_object_payload(self, object_id, new_payload):
        """
        Replace the current payload object with an updated one.

        :param object_id: Object id
        :type object_id: str or ObjectId
        :param new_payload: new payload object
        :type new_payload: dict

        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`
        """
        return self._set_task_object_item(object_id, "payload", new_payload)

    @accept_string_object_ids
    def set_task_object_analytics(self, object_id, new_analytics):
        """
        Replace the current analytics object with an updated one.

        :param object_id: Object id
        :type object_id: str or ObjectId
        :param new_analytics: new analytics object
        :type new_analytics: dict

        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`
        """
        return self._set_task_object_item(object_id, "analytics", new_analytics)

    @accept_string_object_ids
    def set_task_object_last_error(self, object_id, error_text):
        """
        :param object_id: Object id
        :type object_id: str or ObjectId
        :param error_text: Exception stacktrace or error text
        :type error_text: str

        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`
        """
        return self._set_task_object_item(object_id, "last_error", error_text)

    @accept_string_object_ids
    def set_task_object_analytics_item(self, object_id, key, value):
        """Update one item in the analytics dict.

        :param object_id: Object id
        :type object_id: str or ObjectId
        :param key: analytics item key
        :type key: str
        :param value: analytics item value
        :type value: str
        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`
        """
        item_name = f"analytics.{key}"
        return self.tos.update_one(
            {"_id": object_id},
            {"$set": {item_name: value, "updatedAt": datetime.now()}}
        )

    @accept_string_object_ids
    def set_task_object_priority(self, object_id, new_priority):
        """Set the priority of a task object.

        :param object_id: Object id
        :type object_id: str or ObjectId
        :param new_priority: New desired priority
        :type new_priority: int
        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`
        """
        return self.tos.update_one(
            {"_id": object_id},
            {"$set": {"priority": new_priority, "updatedAt": datetime.now()}}
        )

    @accept_string_object_ids
    def _set_task_object_item(self, object_id, field_name, new_item):
        """
        :param object_id: Object id
        :type object_id: str or ObjectId
        :param field_name: name of the field to set
        :type field_name: str
        :param new_item: new value of the field
        :type new_item: str

        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`
        """
        return self.tos.update_one(
            {"_id": object_id},
            {"$set": {field_name: new_item, "updatedAt": datetime.now()}}
        )

    @accept_string_object_ids
    def set_task_object_to_manual_handling(self, object_id):
        # TODO: Deprecate this method
        warnings.warn("Use status instead of manual field", DeprecationWarning)
        return self.tos.update_one(
            {"_id": object_id},
            {"$set": {"manual": True, "updatedAt": datetime.now()}}
        )

    @accept_string_object_ids
    def increment_retry_count(self, object_id):
        """
        :param object_id: Object id
        :type object_id: str or ObjectId
        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`
        """
        return self.tos.update_one(
            {"_id": object_id},
            {"$inc": {"retry_count": 1},
             "$set": {"updatedAt": datetime.now()}}
        )

    @accept_string_object_ids
    def increment_task_object_stage(self, object_id):
        """
        :param object_id: Object id
        :type object_id: str or ObjectId
        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`
        """
        return self.tos.update_one(
            {"_id": object_id},
            {"$inc": {"stage": 1},
             "$set": {"updatedAt": datetime.now()}}
        )

    @accept_string_object_ids
    def decrement_task_object_stage(self, object_id):
        """
        :param object_id: Object id
        :type object_id: str or ObjectId
        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`
        """
        return self.tos.update_one(
            {"_id": object_id},
            {"$inc": {"stage": -1},
             "$set": {"updatedAt": datetime.now()}}
        )

    @accept_string_object_ids
    def set_task_object_for_rerun(self, object_id):
        """
        Decrement stage and set status to pass for rerunning the
        previous stage. Note that a whole task object is passed,
        not only object id.

        :param object_id: Object id
        :type object_id: str or ObjectId

        :raises ValueError: if current task object stage is 0 or less
        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`
        """

        task_object = self.find_task_object_by_id(object_id)
        if task_object["stage"] < 0:
            raise ValueError("Cannot decrement stage to negative number")

        self.increment_retry_count(object_id)
        self.decrement_task_object_stage(object_id)
        return self.set_task_object_status(object_id, "pass")

    def set_task_object_executor(self, object_id):
        node_name = os.environ.get("NODE_NAME", platform.node())
        executor_number = os.environ.get("EXECUTOR_NUMBER", 1)
        text = f"Executor {executor_number} on node {node_name}"

        return self._set_task_object_item(object_id, "executor", text)

    def encode_binary_data(self, filepath):
        """
        Encode a file to a binary string presentation.

        :param filepath: file path to the file to encode
        :type filepath: str

        :returns: encoded file
        :rtype: bson.Binary
        """
        with open(filepath, "rb") as f:
            encoded = Binary(f.read())
        return encoded

    @accept_string_object_ids
    def add_binary_data_to_payload(self, object_id, filepath, data_title):
        """
        Put an encoded binary string to database.

        :param object_id: Object id
        :type object_id: str or ObjectId
        :param filepath: file path to the file to encode
        :type filepath: str
        :param data_title: name of the binary data to store.
        :type data_title: str

        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`

        :ivar bin_data: bson.Binary encoded binary data
        """
        bin_data = self.encode_binary_data(filepath)
        return self.add_key_value_pair_to_payload(object_id, data_title, bin_data)

    @accept_string_object_ids
    def update_payload(self, object_id, update):
        """
        Update task object payload with new data.

        :param object_id: Object id
        :type object_id: str or ObjectId
        :param update: key value pair(s) to add to payload
        :type update: dict

        :raises TypeError: when ``update`` is not a dict.
        :returns: List of results of the update action
        :rtype: List of :class: `pymongo.results.UpdateResult`
        """
        if not isinstance(update, dict):
            raise TypeError("Argument update should be a dict")

        results = []
        for key, value in update.items():
            results.append(
                self.add_key_value_pair_to_payload(object_id, key, value)
            )
        return results

    @accept_string_object_ids
    def add_key_value_pair_to_payload(self, object_id, key, value):
        """
        Add single key value pair to payload.

        :param object_id: Object id
        :type object_id: str or ObjectId
        :param key: name of the field to insert
        :type key: str
        :param value: value of the field to insert
        :type value: str

        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`
        """
        return self._add_key_value_pair_to_field(object_id, key, value, "payload")

    @accept_string_object_ids
    def _add_key_value_pair_to_field(self, object_id, key, value, field_name):
        """
        Add single key value pair to payload.

        :param object_id: Object id
        :type object_id: str or ObjectId
        :param key: name of the field to insert
        :type key: str
        :param value: value of the field to insert
        :type value: str
        :param field_name: name of the field where the key-value pair is inserted
        :type field_name: str

        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`
        """
        item_name = f"{field_name}.{key}"
        return self.tos.update_one(
            {"_id": object_id},
            {"$set": {item_name: value, "updatedAt": datetime.now()}}
        )

    @accept_string_object_ids
    def push_value_to_array_field(self, object_id, value, field_name):
        """
        Push an arbitrary value to an array type field.

        Push is an upsert operation; if the array doesn't exist,
        it will be created.

        :param object_id: Object id
        :type object_id: str or ObjectId
        :param value: value of the field to insert
        :type value: str, int or dict
        :param field_name: Name of the array field, e.g. 'analytics' or
            'payload.alerts'
        :type field_name: str

        :returns: results of the update action
        :rtype: :class: `pymongo.results.UpdateResult`
        """
        return self.tos.update_one(
            {"_id": object_id},
            {"$push": {field_name: value},
             "$set": {"updatedAt": datetime.now()}}
        )

    @accept_string_object_ids
    def delete_task_object(self, object_id):
        # TODO: when would one want to remove a record?
        return self.tos.delete_one({"_id": object_id})

    def save_binary_payload_to_tmp(self, task_object, payload_item_name, prefix="", suffix=""):
        tmp_file = get_temporary_file(prefix, suffix)
        with open(tmp_file, "wb") as f:
            f.write(task_object["payload"][payload_item_name])

        return tmp_file
