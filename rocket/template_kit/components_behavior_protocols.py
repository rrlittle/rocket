class ComponentResponseProtocol(object):
    def respond_to_mapping_info(self, mapping_info):
        """Mapping info will be passed as a string IO"""
        pass

    def respond_to_instru_info(self, instru_info):
        """instru_info will be passed as a instru info object"""
        pass

    def respond_to_header(self, header):
        """header will be a list of list"""
        pass

    def respond_to_user_notice(self, user_notice):
        """User notice will be passed as a string"""
        pass

    def repond_to_data_table(self, data_table):
        """Data table will be passed as a string.
        An empty string means nothing has been returned"""
        pass

class ComponentWriteProtocol(object):

    def write_init_header(self, file, delimiter):
        pass

    def write_init_mapping_info(self, file, delimiter):
        pass
