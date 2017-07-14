#from Managers import Manager
from template_kit.TemplateComponents import Header, InstruInfoComponent, MappingInfo, InstruInfo, NoticeComponent
from template_kit.components_behavior_protocols import ComponentResponseProtocol

import csv


class TemplateParser(object):
    """ docstring for TemplateParser
        the template structure now is Header, InstruInfo, MappingInfo
    """
    # TODO: add comment
    def __init__(self, components, delegate=ComponentResponseProtocol()):
        super(TemplateParser, self).__init__()
        self.components = components
        self.mapping = None
        self.user_notice = None
        self.delegate = delegate

    def _open_file_(self, path):
        self.templ_file = open(path, "r", errors="ignore")
        return self.templ_file

    def parse_template(self, file_path):
        # Parse each component in the rocket template
        try:
            file = self._open_file_(file_path)
            for c in self.components:
                # read in content
                c.read_in_line(file)
                # the component will send message to the delegate
                c.send_message_to_delegate(self.delegate)

        except Exception as e:
            #import ipdb; ipdb.set_trace()
            raise TemplateParseError("%s"%e)
        pass

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
