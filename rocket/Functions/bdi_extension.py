from Functions.function_api import Function
from Managers import ssManager

class GetBDIScore(Function):

    def get_name(self):
        return "GetBDIScore"

    def _func_(self, data_list, args=None):

        # This function is meant to get the score from a data_list of four, 0-3 or NoDataError
        # In the data_list of four, it's possible to have 2 or 3 or 4 data. Under this
        # scenario, choose the highest score.
        # However, it's also possible to have 11 or 1 as the input. For these two, we all think it as
        # 1
        bdi_score = -1 #-1 as the missing value
        for data in data_list:

            if isinstance(data, ssManager.NoDataError):
                pass
            else:
                data = str(data)
                bdi_score = data[0]
                try:
                    if int(bdi_score) >= bdi_score:
                        bdi_score = int(bdi_score)
                except KeyError as e:
                    raise Exception("The data contains Non-number")

        return bdi_score

    def get_documentation(self):
        return "According BDI datafile rule, this will process several items to get the appropriate score. " \
               "If there are multiple data, it will return the highest score. " \
               "Note: put couple data columns into the mapping id"
