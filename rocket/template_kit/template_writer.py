from template_kit.TemplateComponents import Header, InstruInfoComponent, MappingInfo, NoticeComponent
import csv
from template_kit.components_behavior_protocols import ComponentWriteProtocol
import os


class TemplateWriter(object):
    """Is it possible to put those write template into the component?"""
    def __init__(self, components=[], delegate=ComponentWriteProtocol(), delimiter=","):
        self.delegate = delegate
        self.components = components
        self.delimiter = delimiter
        self.file = None
        self.output_file_path = ""

    def write_template(self, output_file_path):
        self.output_file_path = output_file_path
        self.file = open(output_file_path, "w", errors="replace", newline="")
        for c in self.components:
            c.written_to_file(file=self.file, delegate= self.delegate, delimiter= self.delimiter)

    def close_and_save_file(self):
        self.file.close()

    def close_delete_file(self):
        self.file.close()
        os.remove(self.output_file_path)


def test():
    output_file_path = "test_template"
    header = "This is a test template"
    mapping_header = [["Name", "Gender", "height"]]
