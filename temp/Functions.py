# import utils

# class Functions(object):
# 	'''This class include many functions that will be used in the template. Feel free to add more functions 
# 	After you add the call to the new function in run_function.

# 	@property sink_missing_val: the missing value that the source_missing_value should be mapped to
# 	@property data_list 
# 	'''
# 	def __init__ (self, sink_missing_val = None, 
# 		source_missing_val = None,
# 		data_list = [''],
# 		):
# 		'''Be careful, every value is in string which got stripped, instead of double. Cast if you need'''
# 		self.data_list = data_list
# 		self.sink_missing_val = sink_missing_val
# 		self.source_missing_val = source_missing_val.split(',')
# 		for i,value in enumerate(self.source_missing_val):
# 			self.source_missing_val[i] =  str.strip(value)

# 	def run_function(self, function_name = None,extra_args = None):
# 		'''Place to run the function from the outside. This method is used 
# 			in case people want to customize their function name; '''
# 		if function_name == "":
# 			return self.default_func(extra_args = extra_args)

# 		if function_name == "sum":
# 			return self.sum(extra_args = extra_args)

# 	def checkMissingValue(self):
# 		''' For some number calculation, it's necessary to have missing value, but for some 
# 			string calculation not'''
# 		if(self.sink_missing_val == None or self.source_missing_val == None or self.sink_missing_val == ''
# 			or self.source_missing_val == ''):
# 			raise ValueError('No missing value')

# 	def sum(self, extra_args = None):
# 		'''If one of the data cannot be converted to int, then an exception will be raised'''
# 		print('Calculating the sum')
# 		#self.checkMissingValue()

# 		if self.data_list == 0:
# 			raise ValueError()

# 		sum_data = 0
# 		increase_time = 0

# 		for x in self.data_list:
# 			if x not in self.source_missing_val:
# 				sum_data += float(x)
# 				increase_time += 1
# 		if(increase_time == 0):
# 			return self.source_missing_val
# 		#print('the sum is',sum_data)
# 		return sum_data

# 	def default_func(self,extra_args = None):
# 		data = ''
# 		if len(self.data_list) > 0:
# 			data = self.data_list[0]
	
# 		if data == '':
# 			return self.sink_missing_val

# 		if data in self.source_missing_val:
# 			return self.sink_missing_val

# 		return data

# 	def calc_age(self, **extra_args):
# 		''' calcs age using NDAR formula. which is pretty good.
# 			we can use it for all the things probably and it will be fine. 
# 			requires dob and assessment time. 
			
# 			Age is rounded to chronological month. If the research 
#         	participant is 15-days-old at time of interview, 
#         	the appropriate value would be 0 months. If the participant
#         	is 16-days-old, the value would be 1 month.
# 		'''
# 		assessmentTime = extra_args['assement']
# 		if has
#         assessmentDays = assessmentTime.strftime("%d").to_i
#         assessmentMonths = assessmentTime.strftime("%m").to_i
#         assessmentYears = assessmentTime.strftime("%Y").to_i
#         dobDays = thisDOB.strftime("%d").to_i
#         dobMonths = thisDOB.strftime("%m").to_i
#         dobYears = thisDOB.strftime("%Y").to_i
#         ageAtAssessmentInMonths = (assessmentYears - dobYears) * 12 +
#             (assessmentMonths - dobMonths)
#         if (assessmentDays - dobDays) > 15
#             ageAtAssessmentInMonths += 1
#         end
        

# 	# if data in self.source_missing_val:
# 	# 	return sink_missing_val




