from typing import *


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

    def respond_to_data_table(self, data_table):
        """Data table will be passed as a string.
        An empty string means nothing has been returned"""
        pass

    def respond_to_error(self, error_componenet):
        pass

class ComponentWriteProtocol(object):

    def add_extra_content_to_header(self, header):
        pass

    def add_extra_content_to_mapping_info(self, mapping_info):
        pass

    def before_write_instru_info(self, instru_info):
        pass

    def add_extra_content_to_instru_info(self, instru_info):
        pass

    def add_extra_content_to_data_table(self, data_table):
        pass

    def add_extra_content_to_error(self, error):
        pass