import csv
import io


class TemplateComponenet(object):
    def __init__(self):
        self.start_token = "<"
        self.end_token = ">"
        self.content = []
        self.line_num = 0

    def read_in_line(self, file):
        def start_read_until_end_token(reader):
            content_lines = []
            line_num = 0
            for row in reader:
                if not self.end_token in row:
                    content_lines.append(row)
                    line_num += 1
                else:
                    break
            return content_lines, line_num

        reader = csv.reader(file)

        # find the first token to start the processing
        for row in reader:
            if self.start_token in row:
                self.content, self.line_num = start_read_until_end_token(reader)
                break;

        return self._process_after_reading_(self.content)

    def _process_after_reading_(self, content=[]):
        return content

    def send_message_to_delegate(self, delegate):
        """This method will be called to delegate to process the information
         after this component get parsed"""
        pass

    def _extra_write_requirement_(self, file, delegate, delimiter):
        """This method is used to configure what happened after the
        start token is written. A protocal will also be provided
        for this method to help auto generate the template based on the
        information from Mapping Manager or other delegate
        """

        pass

    def written_to_file(self, file, delegate= None, delimiter= ","):
        file.write(self.start_token + "\n")

        self._extra_write_requirement_(file, delegate, delimiter)

        file.write("\n" + self.end_token + "\n")

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

    def _extra_write_requirement_(self, file, delegate, delimiter):
        delegate.write_init_header(file, delimiter)


class InstruInfoComponent(TemplateComponenet):
    def __init__(self):
        super(InstruInfoComponent, self).__init__()
        self.start_token = "<InstruInfo"
        self.end_token = "InstruInfo>"

        self.line_num = 0;
        self.INSTRU_NAME_KEY = "Instrument Name:"
        self.VERSION_KEY = "Version:"

        # The object holding the data information
        self.instru_info = InstruInfo()

    def _process_after_reading_(self, content=[]):

        def find_info_line(list_line):
            for line in list_line:
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
            except StopIteration as e:
                return instru_info

        line = find_info_line(content)
        self.instru_info = parse_line_to_instru(line)
        return self.instru_info

    def get_instru_info(self, ):
        return self.instru_info

    def send_message_to_delegate(self, delegate):
        #print("Instru Info sending message")
        delegate.respond_to_instru_info(self.get_instru_info())

    def _extra_write_requirement_(self, file, delegate, delimiter):
        instru_key = self.INSTRU_NAME_KEY
        version_key = self.VERSION_KEY
        instru_info_line = ["", instru_key, "", version_key, ""]
        csv_writer = csv.writer(file, delimiter=delimiter)
        csv_writer.writerow(instru_info_line)


class InstruInfo(object):
    '''This package serves a place to store the instrument name and version. It will be used by others to get those information'''

    def __init__(self):
        self.instru_name = ""
        self.version = ""

    def get_instru_name(self):
        return self.instru_name

    def get_version(self):
        return self.version


class MappingInfo(TemplateComponenet):
    def __init__(self):
        super(MappingInfo, self).__init__()
        self.start_token = "<Mapping Template"
        self.end_token = "Mapping Template>"
        self.mapping_info = None

    def _process_after_reading_(self, content=[]):
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

    def _extra_write_requirement_(self, file, delegate, delimiter):
        delegate.write_init_mapping_info(file, delimiter)


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


def open_test_file():
    file = open("templateComponentTest.csv", "r")
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

def test():
    file = open_test_file()
    test_header(file)
    test_template(file)
    test_user_notice(file)
    test_mapper(file)