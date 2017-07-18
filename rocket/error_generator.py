"""
    This file should include the functions and classes that can be used to update the error
    log in the csv file.
    It also needs to store error message, so that it can dump the data
"""
from template_kit.components_behavior_protocols import ComponentWriteProtocol
import datetime


class MappingErrorMessage:
    def __init__(self, column_name, column_id, message):
        self.column_name = column_name
        self.column_id = column_id
        self.message = message
        self.type = "Error"


class MappingWarningMessage:
    def __init__(self, column_name, column_id, message):
        self.column_name = column_name
        self.column_id = column_id
        self.message = message
        self.type = "Warning"


class StructureErrorMessage:
    def __init__(self, component_name, message):
        self.component_name = component_name
        self.message = message
        self.type = "Error"


class RunTimeWarningMessage:
    def __init__(self, column_name, column_id, message):
        self.column_name = column_name
        self.column_id = column_id
        self.message = message
        self.type = "Warning"

class ErrorLogger(ComponentWriteProtocol):
    """
        Implementing some of the protocol to handle the update of the Error Section
    """
    mapping_error_messages = []
    mapping_warning_message = []
    structure_error_message = []
    runtime_warning_message = []

    def log_mapping_error(self, column_name, column_id, message):

        # If there has already been an error with the same message, it will ignore it
        for error_message in self.mapping_error_messages:
            if error_message.column_name == column_name and \
               error_message.column_id == column_id and error_message.message == error_message.message:
                return

        self.mapping_error_messages.append(MappingErrorMessage(column_name, column_id, message))

    def log_mapping_warning(self, column_name, column_id, message):
        self.mapping_error_messages.append(MappingWarningMessage(column_name, column_id, message))

    def log_structure_error(self, component_name, message):
        self.structure_error_message.append(StructureErrorMessage(component_name, message))

    def log_runtime_warning(self, column_name, column_id, message):
        self.runtime_warning_message.append(RunTimeWarningMessage(column_name, column_id, message))

    def append_error_with_indention(self, indention_num, data, error):
        """
            This is a wrapper for adding indention for appending the data
        :param indention_num: number of indention cell
        :param data: the line content
        :param error: the error template component
        """
        indention_block = ["" for x in range(0, indention_num)]
        error.content.append(indention_block + data)

    def add_one_line(self, indention, error):
        self.append_error_with_indention(indention, [], error)

    def add_extra_content_to_error(self, error):
        super().add_extra_content_to_error(error)

        error.content = []
        indention = 1

        # Write the line to show when this template has been run last time
        # Next time, I can add which data file it has been run with.
        self.append_error_with_indention(indention, ["Last Run:", str(datetime.datetime.now())], error)
        self.add_one_line(indention,error)

        self.append_mapping_error_messages(indention, error)
        self.append_runtime_error_message(indention, error)

    def append_mapping_error_messages(self, indention, error):
        if len(self.mapping_error_messages) != 0:

            # append header
            self.append_error_with_indention(indention, ["Mapping Error"], error)

            indention += 1
            self.append_error_with_indention(indention, ["Column name", "Column id", "Message", "Type"], error)

            # append each message
            for message in self.mapping_error_messages:
                self.append_error_with_indention(indention,
                                                 [message.column_name, message.column_id, message.message, message.type],
                                                 error)
            self.add_one_line(indention, error)

    def append_runtime_error_message(self, indention, error):
        if len(self.runtime_warning_message) != 0:
            self.append_error_with_indention(indention, ["Runtime Warning"], error)
            indention += 1
            self.append_error_with_indention(indention, ["Column name", "Column id", "Message", "Type"], error)

            # append each message
            for message in self.runtime_warning_message:
                self.append_error_with_indention(indention,
                                                 [message.column_name, message.column_id, message.message, message.type],
                                                 error)

            self.add_one_line(indention, error)

    # Should I store the column? or just the column name and its id?

user_error_log = ErrorLogger()
