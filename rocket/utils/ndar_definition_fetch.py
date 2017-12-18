from typing import *
from urllib import request, error
from collections import namedtuple
from pathlib import Path

InstruInfo = namedtuple("InstruInfo", ["name", "version"])


class NdarDefinitionFetch():
    def __init__(self, output_path, need_save_definition: bool = True):
        self.output_path = output_path
        self.need_save_definition = need_save_definition

    def save_definition_to_output_path(self, lines: List[str], instruInfo: InstruInfo) -> None:
        f_name = "{name}{version}_definition.csv".format(name=instruInfo.name, version=instruInfo.version)
        f_path = Path(self.output_path, f_name)  # type: Path
        try:
            with f_path.open("w+") as f:
                f.writelines(lines)
        except IOError as e:
            print(str(e))
            # error handling
            print("It's possible that you forget to close the definition.")
            i = input("Close the definition, and then press enter")
            try:
                with f_path.open("w+") as f:
                    f.writelines(lines)
            except IOError as e:
                print("File not created or updated")


    def fetch_definition(self, struct_name: str, version: str) -> Optional[List[List[str]]]:
        """
            This function returns a list that contains csv line. Each csv line is already split
            by comma, as a List[str]
        :param struct_name:
        :param version:
        :return:
        """
        short_name = struct_name + version
        url = "https://ndar.nih.gov/api/datadictionary/v2/datastructure/" \
              "{shortname}/csv".format(shortname=short_name)

        try:
            response = request.urlopen(url)

            # the respone will get str in binary, with double quote in it
            b_lines = response.readlines()  # type: List[str]
            lines = [s.decode('ascii').replace('"', "") for s in b_lines]

            if self.need_save_definition:
                self.save_definition_to_output_path(lines, InstruInfo(struct_name, version))
            return [l.split(",") for l in lines]

        except error.URLError as e:
            print(e.reason)
            return None


if __name__ == "__main__":
    f = NdarDefinitionFetch(".", True)
    f.fetch_definition("yadisc", "01")
