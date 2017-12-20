import csv
import io


class InstruInfo(object):
    '''This package serves a place to store the instrument name and version. It will be used by
    others to get those information'''

    def __init__(self):
        self.instru_name = ""
        self.version = ""
        self.respondent = ""

    def get_instru_name(self):
        return self.instru_name

    def get_version(self):
        return self.version

    def get_respondent(self):
        return self.respondent


class TemplateStructureError(Exception): pass


class TemplateComponenet(object):
    '''
        This component represents the section in the template file
        This class controls the logic of how to write the section
        Each template component has its name, has its content. The start tag is set as "<name" and the end
    tag is "name>"
        Each subclass of the template will come with a function that reads the line between these tags. The
    template parser will run the read_in_line method and the _process_after_reading_ method to get the information
        It has two methods that provide delegates the flexibility to make decision about what to do. One is for
    the action of processing after the template action has been processed. The other one is for the action of
    writing customized section for a specific component
        You can add those two delegate methods to components_behavior_protocals.py, which is also in
    template_kit module

    @property:
        start_token: the tag that indicates the start of the component (Override it)
        end_token: the tag that indicates the end of the component (Override it)
        content: the lines between start tag and end tag, it reads with a csv reader, so expect it to be
                 each line is an array of elements
        line_num: the line number between start tag and end tag
    '''
    def __init__(self):
        self.start_token = "<"
        self.end_token = ">"
        self.content = []
        self.line_num = 0
        self.reader = None

    def read_in_line(self, file):
        self.reader = csv.reader(file)
        self.content, self.line_num = self.find_section_start_in_file(self.reader)._read_until_end_token_(self.reader)
        return self._process_after_reading_(self.content)

    def find_section_start_in_file(self, reader):
        for row in reader:
            if self.start_token in row: return self
        raise TemplateStructureError("Missing Template Component {0}".format(type(self).__name__))

    def _read_until_end_token_(self, reader):
        """
            A helper function to read the content of a component until reaching the end token
            If the end token is missing, then it will raise exception
        :param reader:
        :return:
        """
        content_lines = []
        for row in reader:
            if self.end_token not in row:
                content_lines.append(row)
            else:
                return content_lines, len(content_lines)
        raise TemplateStructureError("No ending token for component {0}".format(type(self).__name__))

    def _process_after_reading_(self, content=[]):
        '''
            Override this method to parse the information read from the template component
        Store this information in the component class. Content will be a list of lines, in which each
        line is a list of string.
        :param content: the lines information in the component
        :return: anything you want parser to catch
        '''

        return content

    def send_message_to_delegate(self, delegate):
        """This method will be called by template_parser to delegate to process the information
         after this component get parsed"""
        pass

    def written_to_file(self, file, delegate= None, delimiter= ","):
        """
            This function writes the start token, end token and customized information to the
        section.

        :param file:
        :param delegate:
        :param delimiter:
        :return:
        """
        file.write(self.start_token + "\n")

        self._extra_write_content_(file, delegate, delimiter)

        # Write the component content to the file
        writer = csv.writer(file)
        writer.writerows(self.content)
        file.write(self.end_token + "\n")

    def _extra_write_content_(self, file, delegate, delimiter):
        """
            This method is used to configure what happened after the
        start token is written. It can be implemented just in the component.
        Or a protocol can be provided for this method to help auto
        generate the template based on the information from Mapping
        Manager or other delegate
        :param file: the file object which represents the output file. Use this to write content to the section
        :param delegate: the delegate can be used to configure the output of the content from the outside
        :param delimiter: delimiter for the file. e.g for csv, the delimiter is ","
        :return: nothing.
        """

        pass


class RocketIgnoredComponent(TemplateComponenet):
    """
        This component won't get scanned in the rocket, thus no need to be present in the template
    """
    def read_in_line(self, file):
        try:
            super().read_in_line(file)
        except Exception as e:
            return None


class Header(TemplateComponenet):
    def __init__(self):
        super(Header, self).__init__()
        self.start_token = "<Header"
        self.end_token = "Header>"

    def get_headers(self):
        return self.content

    def send_message_to_delegate(self, delegate):
        #print("Header sending message")
        delegate.respond_to_header(self.get_headers())

    def _extra_write_content_(self, file, delegate, delimiter):
       # delegate.write_init_header(file, delimiter)
        delegate.add_extra_content_to_header(self)


class InstruInfoComponent(TemplateComponenet):
    '''
        The instru info componenet is responsible for writing the version format line to the template
        and parse the version format line to get the information

        @Overrided:
            start_token, end_token, line_num,
        @New property:
            INSTRU_NAME_KEY
            VERSION_KEY
            instru_info
    '''
    def __init__(self):
        super(InstruInfoComponent, self).__init__()
        self.start_token = "<InstruInfo"
        self.end_token = "InstruInfo>"

        self.line_num = 0
        self.INSTRU_NAME_KEY = "Instrument Name:"
        self.VERSION_KEY = "Version:"
        self.RESPONDENT_KEY = "Respondent:"

        # The object holding the data information
        self.instru_info = InstruInfo()

    def _process_after_reading_(self, content=[]):

        def find_info_line(list_line):
            for line in list_line:
                # RESPONDENT_KEY will be optional for backward version compatiable
                if self.INSTRU_NAME_KEY in line and self.VERSION_KEY in line:
                    return line
            raise Exception("The template is wrong for instrument name")

        def parse_line_to_instru(instru_line):
            '''Get the instrument name and table'''
            i = iter(instru_line)
            instru_info = InstruInfo()
            try:
                while True:
                    item = i.__next__()
                    if item == self.INSTRU_NAME_KEY:
                        instru_info.instru_name = i.__next__()
                    elif item == self.VERSION_KEY:
                        instru_info.version = i.__next__()
                    elif item == self.RESPONDENT_KEY:
                        instru_info.respondent = i.__next__()
            except StopIteration as e:
                return instru_info

        line = find_info_line(content)
        self.instru_info = parse_line_to_instru(line)
        return self.instru_info

    def get_instru_info(self):
        return self.instru_info

    def send_message_to_delegate(self, delegate):
        delegate.respond_to_instru_info(self.get_instru_info())

    def _extra_write_content_(self, file, delegate, delimiter):
        delegate.before_write_instru_info(instru_info=self)
        delegate.add_extra_content_to_instru_info(instru_info=self)


class MappingInfo(TemplateComponenet):
    def __init__(self):
        super(MappingInfo, self).__init__()
        self.start_token = "<Mapping Template"
        self.end_token = "Mapping Template>"
        self.mapping_info = None # string buffer that behaves like a file

    def _process_after_reading_(self, content=[]):
        """
            This turns the content of the mapper (original as line of string) into the
            a string buffer to mimic the behavior of file. The reason is that the converter
            needs to accept a file as its argument
        :param content:
        :return:
        """
        if len(content) == 0:
            raise Exception("Template file")
        if len(content) == 1:
            raise Exception("There is no actual mapping data in the file")

        mapping_rest_buffer = io.StringIO()
        map_writer = csv.writer(mapping_rest_buffer)
        map_writer.writerows(content)
        # get the seeker back to the head 
        mapping_rest_buffer.seek(0)

        self.mapping_info = mapping_rest_buffer
        return mapping_rest_buffer

    def get_mapping_info(self):
        if self.mapping_info == None:
            raise Exception("No mapping info has been read, please run the read_in_line first")
        # make sure the point will always go back
        self.mapping_info.seek(0)
        return self.mapping_info

    def send_message_to_delegate(self, delegate):
        #print("mapping info sending message")
        delegate.respond_to_mapping_info( self.get_mapping_info())

    def _extra_write_content_(self, file, delegate, delimiter):
        delegate.add_extra_content_to_mapping_info(self)


class NoticeComponent(TemplateComponenet):
    def __init__(self):
        super(NoticeComponent, self).__init__()
        self.start_token = "<User Notice"
        self.end_token = "User Notice>"
        self.notice = ""

    def _process_after_reading_(self, content=[]):
        '''Find the cell that is not empty, and store it. Recall that content is an list for lists'''
        for cell_row in content:
            for single_cell in cell_row:
                if single_cell == "":
                    continue
                else:
                    self.notice += "\n %s" % single_cell

        return self.notice

    def get_user_notice(self):
        return self.notice

    def send_message_to_delegate(self, delegate):
        #print("notice sending message")
        delegate.respond_to_user_notice(self.get_user_notice())


class DataTableComponent(TemplateComponenet):
    def __init__(self):
        super(DataTableComponent, self).__init__()
        self.start_token = "<Data Table"
        self.end_token = "Data Table>"
        self.DATA_TABLE_KEY = "Data table:"
        self.data_table = [] # data_table will be nothing if there is no data table. data_table is a list

    def _process_after_reading_(self, content=[]):
        #data table content should look like this: [,,Data table:,data_3_ ]'


        # An Template Structure Error can be thrown
        line = self.find_data_table_line(content)

        # If no data table name has been found, it will just return an empty string
        # TODO: Allow multiple table
        self.data_table = self.extract_data_table(line)

        return self.data_table

    def find_data_table_line(self,list_line):
        for line in list_line:
            if self.DATA_TABLE_KEY in line:
                return line
        raise TemplateStructureError("The template has wrong format for data table section")

    def extract_data_table(self, line):
        ind = line.index(self.DATA_TABLE_KEY)

        for index in range(ind+1, len(line)):
            if line[index].strip() != "":
                self.data_table.append(line[index].strip())

     #   for index, data in enumerate(line):
     #         if data == self.DATA_TABLE_KEY:
     #           self.data_table = line[index + 1].strip()
     #          return self.data_table
        return self.data_table

    def send_message_to_delegate(self, delegate):
        delegate.respond_to_data_table(self.data_table)

    def _extra_write_content_(self, file, delegate, delimiter):
        'data table content should look like this: [,,Data table:,data_3_ ]'
        delegate.add_extra_content_to_data_table(self)


class ErrorComponent(RocketIgnoredComponent):
    """
        This componenet should have no effect in running. Just for the log
    """
    def __init__(self):
        super(ErrorComponent, self).__init__()
        self.start_token = "<Error"
        self.end_token = "Error>"

    def _process_after_reading_(self, content=[]):
        pass

    def send_message_to_delegate(self, delegate):
        delegate.respond_to_error(self)

    def _extra_write_content_(self, file, delegate, delimiter):
        delegate.add_extra_content_to_error(self)

def open_test_file():
    #file = open("templateComponentTest.csv", "r")
    file = open("data_table_test.csv", "r")
    return file


def test_header(file=""):
    header = Header()
    header.read_in_line(file)
    print(header.get_headers())


def test_template(file=""):
    instru_compo = InstruInfoComponent()

    instru_compo.read_in_line(file)
    instru = instru_compo.get_instru_info()
    print("instrument name is %s, and the version name is %s" % (instru.get_instru_name(), instru.get_version()))


def test_mapper(file=""):
    mapping_info = MappingInfo()
    mapping = mapping_info.read_in_line(file)
    reader = csv.DictReader(mapping)

    for row in reader:
        print(row)

def test_user_notice(file = ""):
    user_notice_cop = NoticeComponent()
    user_notice = user_notice_cop.read_in_line(file)
    print(user_notice)

def test_data_table (file = ""):
    data_table_cop = DataTableComponent()
    data_table = data_table_cop.read_in_line(file)
    print(data_table)

def test():
    file = open_test_file()
    test_data_table(file)
    test_header(file)
    test_template(file)
    test_user_notice(file)
    test_mapper(file)