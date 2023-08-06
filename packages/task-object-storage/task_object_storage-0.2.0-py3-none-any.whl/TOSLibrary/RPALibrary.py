"""Base libary for RPA using TOS."""
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

from .deco import log_number_of_task_objects, handle_errors
from .exceptions import CannotCreateTaskObject, DataAlreadyProcessed


class RPALibrary:
    """
    RPA Library base class to be used for writing Robot Framework
    libraries using TOSLibrary.

    This class contains error handling, logging, and TOS interaction,
    so users don't have to write them manually every time they write
    new keyword libraries.

    Every library inheriting RPALibrary must have a method
    ``main_action`` which defines the steps to be done for every
    task object in the current stage. To run the actions,
    call ``main_loop`` defined here (override only when necessary).

    Usage example:

    .. code-block:: python

        from TOSLibrary.RPALibrary import RPALibrary

        class PDFMergerLibrary(RPALibrary):

            def __init__(self):
                '''
                Remember to call ``super`` in the constructor.
                '''
                super(PDFMergerLibrary, self).__init__()
                self.merger = PdfFileMerger()

            @keyword
            def merge_all_pdfs(self, filename):
                '''
                Get every valid task object from the DB
                and do the action defined in ``main_action``.
                Exceptions are handled and logged appropriately.
                '''
                count = self.main_loop(current_stage=4)
                if count:
                    write_merged_pdf_object(filename)

            def main_action(self, to):
                '''Append pdf as bytes to the pdf merger object.'''
                pdf_bytes = io.BytesIO(to["payload"]["pdf_letter"])
                self.merger.append(pdf_bytes)

    And the corresponding Robot Framework script:

    .. code-block:: python

        *** Settings ***
        Library                 PDFMergerLibrary

        *** Tasks ***
        Manipulate PDF files
            Merge All PDFs      combined.pdf
    """

    def __init__(self):
        """Remember to call this constructor when inheriting.

        See the example in the :class:`~TOSLibrary.RPALibrary.RPALibrary`
        class docstring above.

        :ivar self.tags: Tags of the current Robot Framework task.
        :ivar self.tos: TOSLibrary instance of the current RF suite.
        """
        super(RPALibrary, self).__init__()
        self.tags = BuiltIn().get_variable_value("@{TEST TAGS}")
        self.tos = BuiltIn().get_library_instance("TOSLibrary")
        self.error_msg = ""
        self.processed_items = []

    def _get_stage_from_tags(self):
        """Get the stage number from the stage tag.

        It is required that the current task tags include one tag
        of the form 'stage_0'.

        Example:
        >>> self.tags = ["stage_0", "producer"]
        >>> self._get_stage_from_tags()
        0

        """
        try:
            stage_tag = next(filter(lambda x: "stage" in x, self.tags))
            return int(stage_tag[-1])
        except (StopIteration, ValueError):
            raise

    @keyword
    @log_number_of_task_objects
    def main_loop(self, *args, **kwargs):
        """
        The main loop for processing task objects on a given stage.

        Get task objects ready for processing and do the actions
        as defined in method ``main_action``. Continue doing this as
        long as valid task objects are returned from the DB. The counter
        value must be returned for logger decorator consumption.

        Using this method/keyword gives you automatic logging and looping
        over valid task objects. You can override this method to suit
        your specific needs.

        Remember to explicitly call this from Robot Framework.

        :param kwargs:

            - **stage** (`int` or `str`) - the current stage where this is called from.
              If this is not given, the stage is inferred from the Robot Framework
              task level tag.

            - **status** (`str`) - the status of the task objects to process
              (default is 'pass')

            - **change_status** (`bool`) - decide if the status should be changed after
              main_action or kept as the original (default is `True`).

            - **error_msg** (`str`) - Custom error message if the action here fails
              (optional).

            - **getter** (`callable`) - the method which is used to get the data to process.
               This might be a custom input data fetcher. By default it is
               ``find_one_task_object_by_status_and_stage``.
               Note that using a custom getter is still experimental.

            - **getter_args** (`tuple`)- arguments that should be passed to the custom
              getter. By default they are ``(status, previous_stage)``.

        :returns: number of task objects processed
        :rtype: int
        :ivar new_status: the new status returned from the ``handle_errors``
                          decorator.
        :type new_status: str
        """
        current_stage = kwargs.get("current_stage")
        if current_stage is None:
            current_stage = self._get_stage_from_tags()
        else:  # 0 is a valid case
            current_stage = int(current_stage)
        previous_stage = current_stage - 1
        self.error_msg = kwargs.get("error_msg", "")  # used inside the decorator
        if current_stage == 0:
            return self.main_loop_when_creating()

        status = kwargs.get("status", "pass")
        getter_args = (status, previous_stage)
        if kwargs.get("getter"):
            # TODO: Not tested and experimental! Is this ever needed?
            getter = kwargs.get("getter")
            getter_args = kwargs.get("getter_args", getter_args)
        else:
            getter = self.tos.find_one_task_object_by_status_and_stage  # this will change status to processing

        counter = 0
        while True:
            to = getter(*getter_args)
            if not to:
                break
            counter += 1

            self.tos.set_task_object_stage(to["_id"], current_stage)
            self.pre_action(to)
            value, new_status = self._error_handled_main_action(to=to, *args, **kwargs)
            if kwargs.get("change_status", True):
                self.tos.set_task_object_status(to["_id"], new_status)
            else:
                # change back to the old status from 'processing'
                self.tos.set_task_object_status(to["_id"], status)
            if new_status == "fail":
                self.tos.set_task_object_last_error(to["_id"], value)
                to["last_error"] = value  # FIXME: handle this in better way
                self.action_on_fail(to)  # the process might be killed here
            self.post_action(to, status)

        return counter

    @keyword
    @log_number_of_task_objects
    def main_loop_when_creating(self):
        """
        The main loop for creating new task objects.

        Call this as a Robot Framework keyword.

        When using this, define also a keyword method ``get_input_data``
        which must return ``None`` when no more data are available.
        """
        counter = 0
        self._reset_processed_list()
        while True:
            data, status = self._error_handled_get_input_data()
            to = {}  # TODO: is it a good idea to use empty dict as default to?
            if status == "pass" and not data:
                # no more input data to process
                break
            elif status == "pass":
                self._check_if_input_data_already_processed(data)
                to = self.tos.create_new_task_object(data)
                self.tos.set_task_object_status(to["_id"], "pass")
            elif status == "fail":
                self.action_on_fail(to)
            self.post_action(to, status)
            counter += 1

        return counter

    @handle_errors()
    def _error_handled_main_action(self, to=None, **kwargs):
        """Wrap the user defined main action with error handling.

        It is important that the task object ``to`` is passed
        as a keyword argument to this method. It allows the decorator
        to consume the task object data.

        :param to: task object
        :type to: dict
        :param kwargs:
            - **main_keyword** (`str`) -  Name of the keyword that should be
              used as the ``main_action``

        :returns: return value of ``main_action`` and status ("pass" or "fail")
         as returned from the decorator ``handle_errors``.
        :rtype: `tuple`
        """
        main_keyword = kwargs.get("main_keyword")
        if main_keyword:
            return BuiltIn().run_keyword(main_keyword, to)
        return self.main_action(to)

    @handle_errors()
    def _error_handled_get_input_data(self):
        return self.get_input_data()

    def get_input_data(self, *args):  # pragma: no cover
        """
        Get the raw data here.

        Should return ``None`` if no more input data is available.
        """
        # TODO: consider writing the functionality as a generator.
        pass

    def main_action(self, to):
        """
        The main action to do.

        You should make the implementation yourself.
        This will be called in the ``main_loop`` and should
        contain all the steps that should be done with the
        data stored in one task object.

        Don't call this from Robot Framework, call ``main_loop`` instead.

        :param to: task object
        :type to: dict
        """
        raise NotImplementedError("Make your own implementation of this method")

    def post_action(self, to, status, *args, **kwargs):
        """Teardown steps.

        Action to do for every task object after
        the main action has completed succesfully or failed.

        You should make the implementation yourself, if needed.

        :param to: task object
        :type to: dict
        :param status: status returned from running ``handle_errors`` decorated
                       ``main_action``.
        :type status: str
        """
        pass

    def pre_action(self, to):
        """Setup steps.

        Action to do for every task object before the error
        handled main action.

        You should make the implementation yourself, if needed.

        :param to: task object
        :type to: dict
        """
        pass

    def action_on_fail(self, to):
        """Action to do when an error is encountered.

        E.g. fail the robot immediately with keyword "Fail".

        Note that these actions are not error handled, all exceptions
        will be propagated until Robot Framework stops execution with failure.
        """
        pass

    def _reset_processed_list(self):
        self.processed_items = []

    def _check_if_input_data_already_processed(self, data):
        """Failsafe preventing infinite loops."""
        # TODO: is this a good idea at all?
        data_hash = hash(frozenset(data.items()))
        if data_hash in self.processed_items:
            raise DataAlreadyProcessed("Input data was just processed")
        else:
            self.processed_items.append(data_hash)
