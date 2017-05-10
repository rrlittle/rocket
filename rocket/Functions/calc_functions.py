''' This file implements several useful functions that can be used for the
    template. Each function should take the argument of a list, and another extra
    argument called args (which can be empty). Look like this (srcdat, args = None)
    Every data passed will be in the form of a list of string. If you want to do
    numerical calculation, change that into the number.
'''
from Managers import ssManager
from Functions.function_api import Function

def sum(*data, args = [0.8,'int']):
 #   import ipdb; ipdb.set_trace()

    # Set the default value for the args if the passed in args is ""
    if args == [""] or args == None or type(args) != list:
        args = [0.8, 'int']

    threshold = args[0]
    strtypearg = args[1]
    strtypes = {'float':float,'int':int}
    strtype = strtypes[strtypearg]

    numMiss = 0
    data_sum = 0
    for num in data:
        if isinstance(num, ssManager.NoDataError ):
            numMiss +=1
        else:
            #import ipdb; ipdb.set_trace()
            try:
                data_sum += strtype(num)
            except ValueError:
                numMiss += 1

    valid_num = len(data)- numMiss

    if numMiss/len(data) < 1 -threshold:
        return data_sum
    else:
        return ssManager.NoDataError()


class Subtract(Function):

    argument_number = 1

    def get_documentation(self):
        return "The data will be subtracted by the first argument."

    def get_name(self):
        return "subtractBy"

    def _func_(self, data_list, args=None):
        if args is None or len(args) == 0:
            raise Exception("No argument for subtract")

        offset = int(args[0])
        try:
            return int(data_list[0]) - offset
        except ValueError as e:
            raise e


class Sum(Function):

    def get_documentation(self):
        return "Calculate the sum. Put the coins ids for all" \
        " the columns into the mapping id"

    def get_name(self):
        return "sum"

    def _func_(self, data_list, args=None):
        if args == [""] or args == None or type(args) != list:
            args = [0.8, 'int']

        threshold = args[0]
        strtypearg = args[1]
        strtypes = {'float': float, 'int': int}
        strtype = strtypes[strtypearg]

        numMiss = 0
        data_sum = 0
        for num in data_list:
            if isinstance(num, ssManager.NoDataError):
                numMiss += 1
            else:
                # import ipdb; ipdb.set_trace()
                try:
                    data_sum += strtype(num)
                except ValueError:
                    numMiss += 1

        valid_num = len(data_list) - numMiss

        if numMiss / len(data_list) < 1 - threshold:
            return data_sum
        else:
            return ssManager.NoDataError()


def sum_mean(data_list, args = [""]):
 #   import ipdb; ipdb.set_trace()

    # Set the default value for the args if the passed in args is ""
    if args == [""] or args == None or type(args) != list:
        args = [0.7, 'int']

    threshold = args[0]
    strtypearg = args[1]
    strtypes = {'float':float,'int':int}
    strtype = strtypes[strtypearg]

    numMiss = 0
    data_sum = 0
    for num in data_list:
        if isinstance(num, ssManager.NoDataError ):
            numMiss +=1
        else:
            #import ipdb; ipdb.set_trace()
            try:
                data_sum += strtype(num)
            except ValueError:
                numMiss += 1

    valid_num = len(data_list)- numMiss

    if numMiss/len(data_list) <= 1 -threshold:
        return data_sum, valid_num
    else:
        return ssManager.NoDataError()


class Mean(Function):
    def __init__(self,*args, **kwargs):
        super(Mean, self).__init__(*args, **kwargs)

    def get_documentation(self):
        return "Calculate the mean. Put the coins ids "\
        "for all the columns into the mapping id"

    def get_name(self):
        return "mean"

    def _func_(self, data_list, args=None):
        mean_sum, valid_num = sum_mean(data_list, args)

        if mean_sum == ssManager.NoDataError:
            return ssManager.NoDataError

        if valid_num == 0:
            print('There is no data for calculating the mean')
            return ssManager.NoDataError

        mean = mean_sum / valid_num
        return mean


class FindFirstValid(Function):

    def get_name(self):
        return "findFirstValid"

    def get_documentation(self):
        return "Gets the first Non-missing value in the data list."

    def _func_(self, data_list, args=None):

        # return the first element that has data.
        for data in data_list:
            if not isinstance(data, ssManager.NoDataError):
                return data

        return ssManager.NoDataError("No data for this field")


class ReverseBySubtractingFrom(Function):

    def get_documentation(self):
        return "Given the cell score, it will reverse the score by subtracting it from a number given in the arg"

    def get_name(self):
        return "reverseBySubtractingFrom"

    def _func_(self, data_list, args=None):
        try:
            upper_bound = float(args[0])

            # Data validation
            if isinstance(data_list[0], ssManager.NoDataError):
                raise Exception("No data exists")

            #
            try:
                data = float(data_list[0])

                # the most essential part
                return int(upper_bound - data)
            except ValueError as e:
                raise ValueError("The data should be in number.")

        except ValueError as e:
            raise ValueError("The args entered is not a number. Please check the args")


class TestNoData(Function):
    def get_name(self):
        return "noDataTest"

    def _func_(self, data_list, args=None):

        return ssManager.NoDataError("NO DATA")


class MaxLength(Function):

    def get_name(self):
        return "maxLength"

    def get_documentation(self):
        return "The data will be limited to this number of characters. The argument will accept an integer as" \
               " the number of characters allowed in a max string"

    def _func_(self, data_list, args=None):
        if args is None or len(args) == 0:
            raise ValueError("There should be one argument for this function")

        max_length = int(args[0])
        if max_length < 0:
            raise ValueError("The argument should be bigger than or equal 0")

        return data_list[0][0: max_length]


def mean(*srcdat, args=None):
    # data will be coerced in the sum
    #import ipdb; ipdb.set_trace()
    mean_sum, valid_num= sum_mean(srcdat, args)

    if mean_sum == ssManager.NoDataError:
        return ssManager.NoDataError

    if valid_num == 0:
        print('There is no data for calculating the mean')
        return ssManager.NoDataError

    mean = mean_sum / valid_num
    return mean


def data_sum(srcdat, args = None):

    if args == 'coerce':
        srcdat = coerce(data)
    data_sum = 0
    for data in srcdat:
        try:
            data = int(data)
            data_sum = data_sum + data
        except ValueError:
            print (('In the calculation of the sum, one of the data: %s is not'
                               'a number') % data)
    return data_sum

def coerce(data):
    try:
        data = int(srcdat[0])
        if data >= 5 and data <= 7:
            data = data - 1
        return data
    except ValueError:
        print ('The data for recoding is not a number')
    return
