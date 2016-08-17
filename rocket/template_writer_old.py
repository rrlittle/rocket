from TemplateComponents import Header, InstruInfoComponent, MappingInfo, NoticeComponent
import csv
import os


class TemplateWriter(object):
    """Is it possible to put those write template into the component?"""
    def __init__(self, output_file_path, delimiter =","):
        self.output_file_path = output_file_path
        self.file = open(self.output_file_path, "w", errors="replace", newline="")
        self.header = Header()
        self.instru_info = InstruInfoComponent()
        self.mapping_info = MappingInfo()
        self.user_notice = NoticeComponent()

        self.delimiter = delimiter

    def write_header(self, header_list = [[]]):
        """This header list should be a two dimension array. One array inside is one line"""
        def write_headerlist_as_csv(header_list):

            csv_writer = csv.writer(self.file, delimiter=self.delimiter)
            for header in header_list:
                csv_writer.writerow( [""] + header)

        self.file.write(self.header.start_token + "\n")
        write_headerlist_as_csv(header_list)
        self.file.write(self.header.end_token + "\n")

    def write_instru_info(self):
        def write_instru_info_with_blank():
            instru_key = self.instru_info.INSTRU_NAME_KEY
            version_key = self.instru_info.VERSION_KEY
            instru_info_line = ["",instru_key,"",version_key,""]
            csv_writer = csv.writer(self.file, delimiter = self.delimiter)
            csv_writer.writerow(instru_info_line)

        self.file.write(self.instru_info.start_token + "\n")
        write_instru_info_with_blank()
        self.file.write(self.instru_info.end_token + "\n")
    
    def write_mapping_info(self, mapping_info={}, mapping_header=[]):
        """This one can be a little difficult. Basically, it will get a dict """
        self.file.write (self.mapping_info.start_token + "\n")

        # write the header line
        csv_writer = csv.writer(self.file,delimiter = self.delimiter)
        csv_writer.writerow(mapping_header)

        # write the mapping_info dict 
        # TODO:

        self.file.write("\n" + self.mapping_info.end_token + "\n")

    def write_user_notice(self):

        self.file.write(self.user_notice.start_token + "\n")
        self.file.write("\n" + self.user_notice.end_token + "\n")

    def close_and_save_file(self):
        self.file.close()

    def close_delete_file(self):
        self.file.close()
        os.remove(self.output_file_path)


def test():
    output_file_path = "test_template"
    header = "This is a test template"
    mapping_header = [["Name", "Gender", "height"]]

    tw = TemplateWriter(output_file_path)
    tw.write_header(mapping_header)
    tw.write_instru_info()
    tw.write_mapping_info(mapping_header=mapping_header)
    tw.close_and_save_file()

