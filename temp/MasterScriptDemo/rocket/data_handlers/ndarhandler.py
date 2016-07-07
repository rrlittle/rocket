from ssManagers import sourceManager, sinkManager, ssManager, csv

#class genericNdarHandler:
class genericNdarHandler(ssManager):
	def __init__(self):
		self.tablename= "default table"
		self.version = 'default version'

		self.fieldnames['missing_val_col'] = 'ndar missing value' 
									# required for both
		self.fieldnames['name_col'] = 'ndar name' # required for both
		self.fieldnames['range_col'] = 'ndar range' # required for both

		# ndar specific
		self.fieldnames['size'] = 'size'
		self.fieldnames['required'] = 'required'
		self.fieldnames['type'] = 'data type'
		self.fieldnames['description'] = 'description'
	
	# this function will prompt the user for a schema file 
	def load_schema(self):
		pathtotemplate = ssManager.load_schema(self,title=('please select'
			' the Ndar template you would like to use for %s')%self.handlername, 
			initialdir=self.defaultschemedir, defaultextension= '.csv')
		pathtodefinitions = ssManager.load_schema(self,title=('please select'
			' the Ndar definition you would like to use for %s')%self.handlername, 
			initialdir=self.defaultschemedir, defaultextension= '.csv')

		with open(pathtotemplate, errors='replace') as ndartemplatefile:
			# we need to get the tablename and version number from the template
			templcsv = csv.reader(ndartemplatefile, delimiter=',')
			for row in templcsv: print(row)
			self.tablename = templcsv[0][0]
			self.version = templcsv[0][1]

		with open(pathtotemplate, errors='replace') as ndardefinitionsfile:
			defcsv = csv.DictReader(ndardefinitionsfile, delimiter=',')
			# ElementName,DataType,Size,Required,ElementDescription,ValueRange,Notes,Aliases
			for row in defcsv: print(','.join(row))

		



class ndarsink(genericNdarHandler, sinkManager):
	def __init__(self):
		sinkManager.__init__(self)
		genericNdarHandler.__init__(self)

		self.handlername = 'ndar sink'
		self.fieldnames['mapping_id_col'] = 'mapping' # required for sink
		self.fieldnames['function'] = 'function' # required for sink
		self.fieldnames['args'] = 'args' # required for sink

	# overwrites generic sink managers write_outfile
	# ndar requires the first line have tablename and version number.
	def write_outfile(self, data, sinkpath):

		with open(sinkpath,'w',newline='') as outfile:
			writer = csv.writer(outfile)
			writer.writerow([self.tablename,self.version])
		
			sinkManager.write_outfile(self, data, outfile=outfile)
		