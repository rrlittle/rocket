from ssManagers import sourceManager, sinkManager, ssManager, csv


class genericCoinsHandler(ssManager):
	def __init__(self):
		self.fieldnames['missing_val_col'] = 'coins missing value' 
									# required for both
		self.fieldnames['name_col'] = 'coins name' # required for both
		self.fieldnames['range_col'] = 'coins range' # required for both

		# coins specific
		self.fieldnames['description'] = 'description'

class coinssource(genericCoinsHandler, sourceManager):
	def __init__(self):
		sourceManager.__init__(self)
		genericCoinsHandler.__init__(self)
		self.handlername = 'coins source'
		self.fieldnames['id_col'] = 'coins id' # required for source
	
	def parse_datasource(self, path_to_source):
		with open (path_to_source, errors = 'replace') as csv_file:
			template_file = csv.DictReader(csv_file,  delimiter='\t')
			template_list = []
			for i, row in enumerate(template_file):
				if i == 0 :
					pass
				else:
					template_list.append(row)

		return template_list