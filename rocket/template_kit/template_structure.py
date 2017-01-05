from template_kit.components_behavior_protocols import ComponentWriteProtocol
from template_kit.TemplateComponents import TemplateComponenet, Header, InstruInfoComponent, NoticeComponent,MappingInfo
from template_kit.TemplateComponents import DataTableComponent
from template_kit.template_parser import TemplateParser
from template_kit.template_writer import TemplateWriter

class TemplateStructure:

    def __init__(self):
        self.components = []

    def insert_component(self, component, index=None):
        '''The component should be a subclass of TemplateComponent
        The component works like a queue, so the user needs to be responsible 
        for maintaining the order
        '''

        if isinstance(component, TemplateComponenet):
            if index is None:
                self.components.append(component)
            else:
                self.components.insert(index, component)

    def component_count(self):
        return len(self.components)

    def display_components(self):
        for c in self.components:
            print(c)
            
    def set_to_default_structure(self):
        self.components = [Header(),InstruInfoComponent(), NoticeComponent(), MappingInfo()]
        return self.components

    def get_template_writer(self, delegate=ComponentWriteProtocol(), delimiter=","):
        return TemplateWriter(self.components, delegate=delegate, delimiter=delimiter)
        pass

    def get_template_parser(self, delegate=ComponentWriteProtocol()):
        return TemplateParser(self.components, delegate)


def test():
    template_structure = TemplateStructure()
    template_structure.set_to_default_structure()
    template_structure.insert_component(DataTableComponent(), 0)
    writer = template_structure.get_template_writer()
    writer.write_template("data_table_test.csv")

