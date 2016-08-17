#from Managers import Manager
from __init__ import templatedir
from TemplateComponents import Header, InstruInfoComponent, MappingInfo, InstruInfo, NoticeComponent
from components_response_protocal import ComponentResponseProtocal

import csv


class TemplateParser(object):
    """docstring for TemplateParser
        the template structure now is Header, InstruInfo, MappingInfo
    """
    def __init__(self, components, delegate=ComponentResponseProtocal()):
        super(TemplateParser, self).__init__()
        self.components = components
        self.mapping = None
        self.user_notice = None
        self.delegate = delegate

    def _open_file_(self, path):
        self.templ_file = open(path, "r", errors = "ignore")
        return self.templ_file

    def parse_template(self, file_path):

        try:
            file = self._open_file_(file_path)
            for c in self.components:
                # read in content
                c.read_in_line(file)

                # the component will send message to the delegate
                c.send_message_to_delegate(self.delegate)

        except Exception as e:
            raise TemplateParseError("%s"%e)
        pass

    def get_instrument_info(self):
        return self.instru_info.get_instru_info()

    def get_mapping(self):
        if self.mapping == None:
            raise ValueError("Please parse the template first")
        return self.mapping

    def get_user_notice(self):
        return self.user_notice

    def close_file(self):
        '''This should be called at the end of the parse template, because if you close, you cant use the
        mapping part anymore.
        '''
        self.templ_file.close()
        pass

    # this template manager needs to tell sinkManager that I
    # have Mapping Version


class TemplateParseError(Exception):
    pass


def test():
    ts = TemplateStructure()
    ts.set_to_default_structure()
    tp = ts.get_template_parser()
    file_path = "templateComponentTest.csv"
    tp.parse_template(file_path)

    # get the instrument name and its version
    instru_info = tp.get_instrument_info()
    mapping_part = tp.get_mapping()
    user_notice = tp.get_user_notice()

    print(instru_info.get_version())
    print(instru_info.get_instru_name())
    print(user_notice)
