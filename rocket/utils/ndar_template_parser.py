from typing import *
import csv
from collections import namedtuple

class NdarElement:

    def __init__(self, col_name, required):
        self.col_name = col_name
        self.required = required


class NdarTemplateError(Exception):
    pass

class CoinsDataError(Exception):
    pass

class NdarTemplateParser:

    def get_columns(filepath: str) -> List[NdarElement]:
        with open(filepath, 'r', newline='') as f:
            dict_reader = csv.DictReader(f)
            if "ElementName" not in dict_reader.fieldnames:
                raise NdarTemplateError("No ElementName")


            cols = [NdarElement(row['ElementName'], row['Required']) for row in dict_reader]
            return cols


class CoinsDataParser:

    def get_columns(filepath: str):
        with open(filepath, 'r', newline='') as f:
            dict_reader = csv.DictReader(f, delimiter='\t')
            cols = dict_reader.fieldnames
            return cols


if __name__ == '__main__':
    print(NdarTemplateParser.get_columns('sd_definitions.csv'))
    print(CoinsDataParser.get_columns('coinsExport_FEQ_041617.csv.tsv'))
