from data_handlers.wtp import WtpSource
from data_handlers.ndar import ndar_snk
from MappingManager import MappingManager
from Functions.calc_functions import Sum, Mean, Subtract, MaxLength, ConcatString, RecodeTwinToAB, MapFrequencyScaleToYesAndNo
from template_kit.template_structure import TemplateStructure
from template_kit.TemplateComponents import DataTableComponent
from Functions.interview_functions import FindGuidByWTPInt, FindGenderByWTPInt, FindAgeByWTPInt, FindAssessByWTPInt, \
                                          FindWbicByWTPInt, FindUrsiByWTPInt, GenderResponse
import pyodbc
from loggers import map_log
from tkinter import messagebox, Tk, simpledialog, filedialog
from template_kit.TemplateComponents import MappingInfo, InstruInfo
from typing import *
from __init__ import templatedir, sinkdatdir, srcdatdir, ndartempdir, ndardefdir
from pathlib import Path
from utils.ndar_template_parser import NdarTemplateParser
from template_kit.TemplateComponents import MappingInfo, InstruInfo, InstruInfoComponent
from itertools import chain
from toolz.itertoolz import unique
from utils.ndar_definition_fetch import NdarDefinitionFetch
from toolz.itertoolz import *

class wtp2ndar (MappingManager):

    def __init__(self):
        super(wtp2ndar, self).__init__(source=WtpSource,
                                        sink=ndar_snk)
        self.instru_name = ""
        self.version = ""


    def load_functions(self):
        function_list = []
        function_list.append(Sum())
        function_list.append(Mean())
        function_list.append(Subtract())
        function_list.append(MaxLength())
        function_list.append(ConcatString())
        function_list.append(GenderResponse())
        function_list.append(RecodeTwinToAB())
        function_list.append(MapFrequencyScaleToYesAndNo())

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

        name = simpledialog.askstring("Action", "Enter NDAR instrument name (without version and not case sensitive)")
        version = simpledialog.askstring("Action", "Enter NDAR instrument version")
        respondent = simpledialog.askstring("Action", "Enter the respondent for this instrument. (e.g, twin, cotwin)")

        if name is not None:
            # No input check right now
            name = name.lower()
            instru_info.instru_info.instru_name = name
            self.instru_info.instru_name = name

        if version is not None:
            # A '0' is added to the version string because NDAR requires
            # single digit versions numbers to have a leading '0'
            if len(version) == 1:
                version = "0" + version
            instru_info.instru_info.version = version
            self.instru_info.version = version

        if respondent is not None:
            instru_info.instru_info.respondent = respondent
            self.instru_info.respondent = respondent

        root.destroy()

    def _get_ndar_definition_(self)->Optional[str]:
        ndar_definition = None
        messagebox.showinfo("Next step", "Then please choose a NDAR definition file. "
                                         "\nIf you don't want. you can press cancel on next page")
        while True:
            ndar_definition = filedialog.askopenfilename(initialdir=ndartempdir, title="Choose a NDAR template")

            if ndar_definition is None or ndar_definition == "":
                ndar_definition = None
                break

            p = Path(ndar_definition)
            if p.suffix != '.csv':
                messagebox.showwarning("File error", "Please choose a csv file .")
                pass
            else:
                break

        return ndar_definition

    def _get_ndar_cols_with_def_(self) -> List[str]:
        """
            This function parses the ndar definition downloaded through NDAR API.
            It only returns the ndar col name now.
            If there is error with the fetch. Then it will return empty list
        :return:
        """
        fetch = NdarDefinitionFetch(ndardefdir)
        ndar_definition = None
        instru_info = self.instru_info
        if instru_info.instru_name != "" and instru_info.version != "":
            ndar_definition = fetch.fetch_definition(instru_info.instru_name, instru_info.version)

        if ndar_definition is None:
            print("Can't find the Instrument with the name and version")
            return []
        else:
            fields = first(ndar_definition) # type: List[str]
            elem_index = fields.index("ElementName")
            elem_list_names = [l[elem_index] for l in drop(1, ndar_definition)]

            return elem_list_names

    def add_extra_content_to_mapping_info(self, mapping):
        # this will append the field names
        super().add_extra_content_to_mapping_info(mapping)

        ndar_cols = self._get_ndar_cols_with_def_()

#        ndar_definition = self._get_ndar_definition_()

        # if ndar_definition is not None:
        #     ndar_elements = NdarTemplateParser.get_columns(ndar_definition)
        #     ndar_cols = [e.col_name for e in ndar_elements]
        # else:
        #     ndar_cols = []

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