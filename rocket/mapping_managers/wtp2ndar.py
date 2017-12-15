from data_handlers.wtp import WtpSource
from data_handlers.ndar import ndar_snk
from MappingManager import MappingManager
from Functions.calc_functions import Sum, Mean, Subtract, MaxLength, ConcatString
from template_kit.template_structure import TemplateStructure
from template_kit.TemplateComponents import DataTableComponent
from Functions.interview_functions import FindGuidByWTPInt, FindGenderByWTPInt, FindAgeByWTPInt, FindAssessByWTPInt, \
                                          FindWbicByWTPInt, FindUrsiByWTPInt, GenderResponse
import pyodbc
from loggers import map_log
from tkinter import messagebox, Tk, simpledialog, filedialog
from template_kit.TemplateComponents import MappingInfo, InstruInfo
from typing import *
from __init__ import templatedir, sinkdatdir, srcdatdir, ndartempdir
from pathlib import Path
from utils.ndar_template_parser import NdarTemplateParser
from template_kit.TemplateComponents import MappingInfo, InstruInfo, InstruInfoComponent
from itertools import chain
from toolz.itertoolz import unique

class wtp2ndar (MappingManager):

    def __init__(self):
        super(wtp2ndar, self).__init__(source=WtpSource,
                                        sink=ndar_snk)

    def load_functions(self):
        function_list = []
        function_list.append(Sum())
        function_list.append(Mean())
        function_list.append(Subtract())
        function_list.append(MaxLength())
        function_list.append(ConcatString())
        function_list.append(GenderResponse())

        function_list.append(FindGuidByWTPInt())
        function_list.append(FindGenderByWTPInt())
        function_list.append(FindAgeByWTPInt())
        function_list.append(FindAssessByWTPInt())
        function_list.append(FindWbicByWTPInt())
        function_list.append(FindUrsiByWTPInt())
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
        # while True:
        #     data_table_name = input("Which database tables are you going to pull data from (press Enter to end): ")
        #     if data_table_name == "":
        #         break
        #     data_table_names.append(data_table_name)
        root = Tk()
        root.withdraw()

        data_table_name = simpledialog.askstring("Action",
                                                 "Add datatable name for this template. Press cancel to end inputting")

        while True:
            if data_table_name is None:
                break
            data_table_names.append(data_table_name)
            data_table_name = simpledialog.askstring("Action",
                                                     "Add another datatable name for this template. Press cancel to end inputting")

        root.destroy()
        content = ["", data_table.DATA_TABLE_KEY] + data_table_names
        data_table.content.append(content)
        self.source.data_table_names = data_table_names

    def before_write_instru_info(self, instru_info: InstruInfoComponent):
        super().before_write_instru_info(instru_info)
        root = Tk()
        root.withdraw()

        name = simpledialog.askstring("Action", "Enter NDAR instrument name")
        version = simpledialog.askstring("Action", "Enter NDAR instrument version")

        if name is not None:
            # No input check right now
            instru_info.instru_info.instru_name = name

        if version is not None:
            instru_info.instru_info.version = version

        root.destroy()

    def _get_ndar_template_(self)->Optional[str]:
        ndar_template = None
        messagebox.showinfo("Next step", "Then please choose a NDAR definition file. "
                                         "\nIf you don't want. you can press cancel on next page")
        while True:
            ndar_template = filedialog.askopenfilename(initialdir=ndartempdir, title="Choose a NDAR template")

            if ndar_template is None or ndar_template == "":
                ndar_template = None
                break

            p = Path(ndar_template)
            if p.suffix != '.csv':
                messagebox.showwarning("File error", "Please choose a csv file .")
                pass
            else:
                break

        return ndar_template

    def add_extra_content_to_mapping_info(self, mapping):
        # this will append the field names
        super().add_extra_content_to_mapping_info(mapping)

        ndar_template = self._get_ndar_template_()

        if ndar_template is not None:
            ndar_elements = NdarTemplateParser.get_columns(ndar_template)
            ndar_cols = [e.col_name for e in ndar_elements]
        else:
            ndar_cols= []

        fields_for_tables = [self._get_table_fields_(f) for f in self.source.data_table_names] # type: List[List[str]]
        all_fields_with_no_duplicate = list(unique(chain.from_iterable(fields_for_tables)))

        # This will insert each field information
        mapping_header = self._add_mapping_headers_from_src_sink()
        wtp_col_id_index = mapping_header.index(self.source.template_fields["id"])
        wtp_col_name_index = mapping_header.index(self.source.template_fields["col_name"])
        wtp_missing_value_index = mapping_header.index(self.source.template_fields["missing_vals"])

        ndar_col_id_index = mapping_header.index(self.sink.template_fields["id"])
        ndar_col_name_index = mapping_header.index(self.sink.template_fields["col_name"])
        ndar_default_index = mapping_header.index(self.sink.template_fields["default"])

        longest = max(len(all_fields_with_no_duplicate), len(ndar_cols))
        # the index starts from 1, for user convenience
        for index in range(1, longest + 1):
            # fill in each section
            row = [""] * len(mapping_header)  # type:List[str]
            if index <= len(all_fields_with_no_duplicate):
                row[wtp_col_id_index] = index
                row[wtp_col_name_index] = all_fields_with_no_duplicate[index - 1]
                row[wtp_missing_value_index] = "9998, 9999, "

            if index <= len(ndar_cols):
                row[ndar_col_id_index] = index
                row[ndar_col_name_index] = ndar_cols[index - 1]
                row[ndar_default_index] = ""

            mapping.content.append(row)

    def _get_table_fields_(self, tablename) -> List[str]:
        con = None
        try:
            con = pyodbc.connect("DSN=wtp_data")
            if tablename is None or tablename == "":
                return []

            cur = con.cursor()
            sql = "SELECT * FROM {0} LIMIT 1;".format(tablename)
            print(sql)
            cur.execute(sql)

            desc = cur.description
            return [x[0] for x in desc]

        except pyodbc.Error as e:
            map_log.critical(str(e))
            return []
        finally:
            if con is not None:
                con.close()