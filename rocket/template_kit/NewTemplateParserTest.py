import unittest
from template_parser import TemplateParser
from template_structure import TemplateStructure
from TemplateComponents import InstruInfo
from components_behavior_protocols import ComponentResponseProtocol

class TemplateParser(unittest.TestCase, ComponentResponseProtocol):
    def setUp(self):

        self.ts = TemplateStructure()
        self.ts.set_to_default_structure()
        self.tp = self.ts.get_template_parser(delegate=self)
        file_path = "templateComponentTest.csv"
        self.tp.parse_template(file_path)

    def respond_to_instru_info(self, instru_info):
        self.instru_info = instru_info

    def test_parser(self):
        # get the instrument name and its version

        print(self.instru_info.get_version())
        print(self.instru_info.get_instru_name())

        self.assertEqual(self.instru_info.get_instru_name(), "rpq" )


if __name__ == '__main__':
    unittest.main()
