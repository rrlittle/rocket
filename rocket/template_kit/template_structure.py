from template_kit.components_behavior_protocols import ComponentWriteProtocol, ComponentResponseProtocol
from template_kit.TemplateComponents import TemplateComponenet, Header, InstruInfoComponent, NoticeComponent,MappingInfo, ErrorComponent
from template_kit.TemplateComponents import DataTableComponent
from template_kit.template_parser import TemplateParser
from template_kit.template_writer import TemplateWriter
from typing import *

class TemplateStructure:

    def __init__(self):
        self.components = [] # type: List[TemplateComponenet]

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

    def get_component(self, component_type: Type[TemplateComponenet]) -> Optional[TemplateComponenet]:
        for c in self.components:
            if isinstance(c, component_type):
                return c
        return None

    def component_count(self):
        return len(self.components)

    def display_components(self):
        for c in self.components:
            print(c)
            
    def set_to_default_structure(self):
        self.components = [Header(), InstruInfoComponent(), NoticeComponent(), MappingInfo(), ErrorComponent()]
        return self.components

    def get_template_writer(self, delegate=ComponentWriteProtocol(), delimiter=","):
        return TemplateWriter(self.components, delegate=delegate, delimiter=delimiter)
        pass

    def get_template_parser(self, delegate=ComponentResponseProtocol()):
        return TemplateParser(self.components, delegate)

    

def test():
    template_structure = TemplateStructure()
    template_structure.set_to_default_structure()
    template_structure.insert_component(DataTableComponent(), 0)
    writer = template_structure.get_template_writer()
    writer.write_template("data_table_test.csv")

