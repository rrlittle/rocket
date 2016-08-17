import unittest
from template_parser import TemplateParser
from template_structure import TemplateStructure
from TemplateComponents import InstruInfo
from components_response_protocal import ComponentResponseProtocal

class MyTestCase(unittest.TestCase, ComponentResponseProtocal):
    def setUp(self):
        super()

        self.ts = TemplateStructure()
        self.ts.set_to_default_structure()
        self.tp = self.ts.get_template_parser()
        file_path = "templateComponentTest.csv"
        self.tp.parse_template(file_path)

    def respond_to_instru_info(self, instru_info):

    def test_something(self):
        # get the instrument name and its version
        instru_info = self.tp.get_instrument_info()
        mapping_part = self.tp.get_mapping()
        user_notice = self.tp.get_user_notice()

        print(instru_info.get_version())
        print(instru_info.get_instru_name())
        print(user_notice)


        self.assertEqual(instru_info.get_version(), "rpq" )


if __name__ == '__main__':
    unittest.main()
