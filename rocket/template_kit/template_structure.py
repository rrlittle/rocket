from template_kit.TemplateComponents import TemplateComponenet, Header, InstruInfoComponent, NoticeComponent,MappingInfo
from template_kit.template_parser import TemplateParser
from template_kit.template_writer import TemplateWriter

class TemplateStructure:

    def __init__(self):
        self.components = []

    def add_component(self, component):
        '''The component should be a subclass of TemplateComponent
        The component works like a queue, so the user needs to be responsible 
        for maintaining the order
        '''
        if issubclass(component, TemplateComponenet):
            self.components.append(component)
        pass

    def display_components(self):
        for c in self.components:
            print(c)
            
    def set_to_default_structure(self):
        self.components = [Header(),InstruInfoComponent(), NoticeComponent(), MappingInfo()]
        return self.components

    def get_template_writer(self, delegate, delimiter):
        return TemplateWriter(self.components, delegate=delegate, delimiter=delimiter)
        pass

    def get_template_parser(self, delegate):
        return TemplateParser(self.components, delegate)
