import csv
import logging
import Functions 
from ssManagers import sinkManager
from ssManagers import sourceManager
import ipdb

# Is it possible to subclass SinkCol like this. Should be 
class SinkCol:
	"""SinkCol is the class representation for the col from the sink 
	@property col_name: column name
	@property corresponding_id : which columns the function for
								 this sink col should get data from
	@property value_range: which value range the data should end up be in
	@property function: the function name used for calculating the data
	@property fun_args: extra function argument should be passed to the function
	@property default_value: 



	"""

	def __init__(self, name = '', corresponding_id = '',
		datatype = None,element_des = '', value_range = '', 
		missing_value = '', function = '', sink_missing_value = '', 
		default_val = '', extra_args = ''
		):
		assert  name != '', 'There is no name'
		#assert (corresponding_id != None and corresponding_id != '') or\
		#		(default_value != None and default_value != '') , 'There is no corresponding id'
		#assert value_range !='', 'Here is a problem with value_range'
		
		#assert missing_value != None or missing_value != '','Here is no missing value defined'

		self.col_name = name.strip()
		self.corresponding_id = corresponding_id.strip().split(',')
		self.col_datatype = datatype
		self.value_range = value_range.strip()
		self.function = function
		self.sink_missing_value = missing_value
		self.extra_args = extra_args
		self.default_value = default_val


	# Given a list of sourceCol object, find the corresponding columns and process the data
	def process_data_from_corres_source(self, sourceCol_list):
		'''This method will do three things: 
		1: find all of the corresponding column for the sink column based on the corresponding id. 
		2: Check the value range of the source data and then convert it into the sink value range
		3: Calculate all of the data based on the function user given'''

		print('Start processing the data for column %s' %self.col_name)
		self.data_list = []

		source_missing_val = ''
		#if self.col_name =='quest_instruct':
		#	ipdb.set_trace()
		if self.corresponding_id[0] == '':

			#ipdb.set_trace()
			if self.default_value == '':
				self.data = self.sink_missing_value
			else:	
				self.data = self.default_value

		else:
			for source_col in sourceCol_list:
				if source_col.col_id in self.corresponding_id:
				# Check value range here.
				# Also change missing value here. 
				# The range string would look like this: 
				# TODO:
				# data should get strip before they got into the file
					self.data_list.append(source_col.data.strip())
					source_missing_val = source_col.col_missing_value

			#use try catch to catch illegal argument
			try:
				print ('start calculating data')
				self.calculate_data(self.data_list,source_missing_val)
				print ('calculating data end')

			except ValueError:

				self.data = self.default_value
				print('Argument for the function of this column %s is illegal'%self.col_name)

		print('Data process ends')

	def calculate_data(self, data_list, source_missing_val):
		'''This method help pass in the data argument for the function. If the intended function does not
		support the data type in the argument, a valueError should be thrown'''
		functions = Functions( data_list = data_list, sink_missing_val =  self.sink_missing_value,
								source_missing_val = source_missing_val)	
		self.data = functions.run_function(function_name = self.function, 
											extra_args = self.extra_args)
		#foo = getattr(Functions,  self.function, Functions.default_func)
		#self.data = foo(data_list, *self.extra_args.split(' '))


	def __repr__(self):
		self.data = str(self.data)

		return self.data

	# probably need a better value parser so that.
	def sync_value_range(self,source_value_range,source_data):
		# I can assume that the range is integer continuous
		# 1::9;999;998;
		return 


class SourceCol:
	def __init__(self, name = '', missing_value='', value_range='', col_id='',
		col_question = None):
		""" """
		assert name != None and name != '', 'Source col does not have a name'
		#assert missing_value != None and missing_value !='',\
		#	'Source col does not have the missing value'
		#assert value_range != None and value_range != '', \
		#	'Source col does not have the value range'

		assert col_id != None and col_id != '', \
			'Source col does not have the column id, necessary for cooresponding'

		self.data = ''
		self.col_name = name
		self.col_id = col_id
		self.col_question = col_question
		self.col_missing_value = missing_value
		self.value_range = value_range


	def __repr__(self):
		return self.data

class MappingManager:
	'''Mapping Manager is responsible for mapping the source data to the sink data 
	based on the template file

	@property source_manager: should be the subclass of SourceManager in ssManagers, 
			it knows which column in the template is properties for source column
	@property sink_manager: should be the subclass of SinkManager in ssManagers,
	 		it knows which column in the template is properties for sink column
	@property source_col_table: SourceCol Object presentation for the source data table

	@property sink_table: SinkCol Object presentation for the sink data table
			  map from source_col_table to sink_table

	 '''

	def __init__(self, source_manager, sink_manager):
		self.sink_table = []
		self.source_col_table = []
		self.source_manager = source_manager
		self.sink_manager = sink_manager


	def load_template(self,template_path, source_data_path):
		'''Read the template file and source data file
		@param template_path: The file for template
		@param source_data_path: the file for source data file
		'''

		template_file = ''
		data_file = ''
		

		csvfile = open(template_path, errors='replace')
		
		template_file = csv.DictReader(csvfile)
		data_file = self.source_manager.parse_datasource(source_data_path)		
	
		for i,row in enumerate(data_file):			
			#	print('the row is ',row)
			sink_col_list = []
			source_col_list = []
			for template_row in template_file:
				try:
					sink_col = self.create_sink_col(template_row)
					sink_col_list.append(sink_col)
				except AssertionError:
					print('Unable to read create the sink column on line %d'
						%i)
					pass
				
				try:
					source_col = self.create_source_col(template_row)
					source_col_list.append(source_col)
				except AssertionError:
					print('Unable to read create the source column on line %d'
						%i)
					pass

			self.sink_table.append(sink_col_list)
			
			for source_col in source_col_list:
				
				source_col.data = row[source_col.col_name]
				if source_col.data == None:
					source_col.data = ''

			self.source_col_table.append(source_col_list)
			
			csvfile.seek(0)
			template_file = csv.DictReader(csvfile)

		csvfile.close()
		return self.sink_table

	# Not allow override
	# Mapping will start the process of mapping based on the template file loaded before
	def mapping(self):


		for i,row_source in enumerate(self.source_col_table):
			sink_row=[]
			sink_col_list = self.sink_table[i]

			for sink_col in sink_col_list:
				sink_col.process_data_from_corres_source(sourceCol_list = row_source)
				sink_row.append(sink_col)

		return self.sink_table
	

	#Allow for override
	# I'm thinking how to extend in the future. Someone can subclass and 
	# override create_source_col
	def create_sink_col(self, template_row):
		name_col = self.sink_manager.fieldnames['name_col']
		range_col = self.sink_manager.fieldnames['range_col']
		missing_value = self.sink_manager.fieldnames['missing_val_col']
		mapping_id = self.sink_manager.fieldnames['mapping_id_col']
		function_col = self.sink_manager.fieldnames['function']
		fun_args_col = self.sink_manager.fieldnames['args']
		default_val = self.sink_manager.fieldnames['default_val']


		sink_col = SinkCol(name = template_row[name_col]
						   ,corresponding_id = template_row[mapping_id]
						   ,value_range = template_row[range_col]
						   ,function = template_row[function_col]
						   ,extra_args = template_row[fun_args_col]
						   ,missing_value = template_row[missing_value]
						  ,default_val = template_row[default_val])


		return sink_col 

	def create_source_col(self, template_row):
		name_col = self.source_manager.fieldnames['name_col']
		range_col = self.source_manager.fieldnames['range_col']	
		id_source = self.source_manager.fieldnames['id_col']
		missing_val_col = self.source_manager.fieldnames['missing_val_col']
		#question = self.source_manager.fieldnames['question'];
		source_col = SourceCol(name = template_row[name_col]
							   ,missing_value = template_row[missing_val_col]
							   ,col_id = template_row[id_source]
							   ,value_range = template_row[range_col]
							   )

		return source_col

def UnitTest():
	source_manager = sourceManager()
	sink_manager = sinkManager()
	mapping_manager = MappingManager(source_manager,sink_manager)
	mapping_manager.load_template('../mapping_files/GenericExample.csv','../source_datafiles/coinsExport2015_12_18-09_50_55_0.tsv')
	mapping_manager.mapping()
	table = mapping_manager.sink_table

	with open('UNITTEST','w') as file:
		for row in table:
			for column in row:
				file.write(column.data)

