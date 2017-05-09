from data_handlers.wtp import WtpSource
from data_handlers.ndar import ndar_snk
from MappingManager import MappingManager
from Functions.calc_functions import Sum, Mean
from template_kit.template_structure import TemplateStructure
from template_kit.TemplateComponents import DataTableComponent
from Functions.interview_functions import FindGuidByWTPInt, FindGenderByWTPInt, FindAgeByWTPInt, FindAssessByWTPInt, \
                                          FindWbicByWTPInt
import pyodbc
from loggers import map_log

class wtp2ndar (MappingManager):

    def __init__(self):
        super(wtp2ndar, self).__init__(source=WtpSource,
                                        sink=ndar_snk)

    def load_functions(self):
        function_list = []
        function_list.append(Sum())
        function_list.append(Mean())
        function_list.append(FindGuidByWTPInt())
        function_list.append(FindGenderByWTPInt())
        function_list.append(FindAgeByWTPInt())
        function_list.append(FindAssessByWTPInt())
        function_list.append(FindWbicByWTPInt())
        return function_list

    def _set_template_structure_(self):
        template_structure = TemplateStructure()
        template_structure.set_to_default_structure()
        template_structure.insert_component(DataTableComponent(), 1)
        return template_structure

    ############################
    # Component behavior delegate method
    #########
    def respond_to_data_table(self, data_table):
        # pass the data_table to wtp_source
        self.source.data_table = data_table

    def add_extra_content_to_data_table(self, data_table):

        # Read in multiple data tables
        data_table_names = []
        while True:
            data_table_name = input("Which database tables are you going to pull data from (press Enter to end): ")
            if data_table_name == "":
                break
            data_table_names.append(data_table_name)

        content = ["", data_table.DATA_TABLE_KEY] + data_table_names
        data_table.content.append(content)
        self.source.data_table_names = data_table_names

    def add_extra_content_to_mapping_info(self, mapping):
        # this will append the field names
        super().add_extra_content_to_mapping_info(mapping)

        fields_for_tables = [self._get_table_fields_(f) for f in self.source.data_table_names]

        # This will insert each field information
        mapping_header = self._add_mapping_headers_from_src_sink()
        col_id_index = mapping_header.index(self.source.template_fields["id"])
        col_name_index = mapping_header.index(self.source.template_fields["col_name"])
        missing_value_index = mapping_header.index(self.source.template_fields["missing_vals"])
        col_id = 0
        for fields in fields_for_tables:
            if fields is None: continue
            for field in fields:
                new_row = ["" for x in mapping_header]
                new_row[col_id_index] = col_id
                new_row[col_name_index] = field
                new_row[missing_value_index] = "9998, 9999"
                mapping.content.append(new_row)
                col_id += 1

    def _get_table_fields_(self, tablename):

        con = None
        try:
            con = pyodbc.connect("DSN=wtp_data")
            if tablename is None or tablename == "":
                return None

            cur = con.cursor()
            sql = "SELECT * FROM {0} LIMIT 1;".format(tablename)
            print(sql)
            cur.execute(sql)

            desc = cur.description
            return [x[0] for x in desc]

        except pyodbc.Error as e:
            map_log.critical(str(e))
            return None
        finally:
            if con is not None:
                con.close()