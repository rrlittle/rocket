#from Managers import Manager
from __init__ import templatedir
from TemplateComponents import Header, InstruInfoComponent, MappingInfo, InstruInfo

import csv

class TemplateParser(object):
	"""docstring for TemplateParser
		the template structure now is Header, InstruInfo, MappingInfo
	"""
	def __init__(self, path):
		super(TemplateParser, self).__init__()
		self.path = path
		self.header = Header()
		self.instru_info = InstruInfoComponent()
		self.mapping_info = MappingInfo()

	def _open_file_(self):
		self.templ_file = open(self.path,"r", errors = "ignore")
		return self.templ_file

	def parse_template(self):

		try: 
			file = self._open_file_()
			self.header.read_in_line(file)
			self.instru_info.read_in_line(file)
			self.mapping = self.mapping_info.read_in_line(file)
		except Exception as e:
			raise TemplateParseError("%s"%e)
		pass

	def get_instrument_info(self):
		return self.instru_info.get_instru_info()

	def get_mapping(self):
		if (self.mapping == None):
			raise ValueError("Please parse the template first")
		return self.mapping

	def close_file(self):
		'''This should be called at the end of the parse template, because if you close, you cant use the 
		mapping part anymore.
		'''
		self.templ_file.close()
		pass


	# this template manager needs to tell sinkManager that I 
	# have Mapping Version
class TemplateParseError(Exception): pass

def test():
	file_path = "test_template.csv"
	tp = TemplateParser(file_path)
	tp.parse_template()

	# get the instrument name and its version
	instru_info = tp.get_instrument_info()
	mapping_part = tp.get_mapping()
	print(instru_info.get_version())
	print(instru_info.get_instru_name())
