"""
Robot Framework layer for TOS.
"""
from tos.task_object_storage import TaskObjectStorage

# TODO Add custom logging for keywords?


class TOSLibrary(TaskObjectStorage):

    def __init__(self, server, port, db_name):

        super(TOSLibrary, self).__init__(
            db_server=f"{server}:{port}",
            db_name=db_name,
        )

        self.connect()
        self.initialize_tos()

    # FIXME: use robot Dynamic API
    # def get_keyword_names(self):
    #     """Robot Framework dynamic API keyword collector."""
    #     return [name for name in dir(self)]
    #
    # def run_keyword(self, name, args, kwargs):
    #     print("Running keyword '%s' with positional arguments %s and named arguments %s."
    #           % (name, args, kwargs))
    # FIXME: should the return value be defined here?
