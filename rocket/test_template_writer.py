import unittest
from template_kit.template_structure import  TemplateStructure
from template_kit.TemplateComponents import  DataTableComponent

class MyTestCase(unittest.TestCase):
    def test_something(self):

        template_structure = TemplateStructure()
        template_structure.set_to_default_structure()
        template_structure.insert_component(DataTableComponent(), 0)
        writer = template_structure.get_template_writer()
        writer.write_template("data_table_test.csv")

        self.assertEqual(True, False)




if __name__ == '__main__':
    unittest.main()
