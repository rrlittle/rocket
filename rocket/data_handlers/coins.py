from Managers import sourceManager

class coins_src(sourceManager):
    ''' coins source
    '''
    def __init__(self):
    	sourceManager.__init__(self)
    	self.template_fields['id'] = 'coins id'
    	self.template_fields['col_name'] = 'coins name'
    	self.template_fields['col_range'] = 'coins range'
    	print(self.template_fields)