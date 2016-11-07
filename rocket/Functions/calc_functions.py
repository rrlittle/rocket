''' This file implements several useful functions that can be used for the
    template. Each function should take the argument of a list, and another extra
    argument called args (which can be empty). Look like this (srcdat, args = None)
    Every data passed will be in the form of a list of string. If you want to do
    numerical calculation, change that into the number.
'''
from Managers import ssManager


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
        return ssManager.NoDataError();

def sum_mean(data, args = [0.7,'int']):
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

    if numMiss/len(data) <= 1 -threshold:
        return data_sum, valid_num
    else:
        return ssManager.NoDataError();


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

def coerce(data):
    try:
        data = int(srcdat[0])
        if data >= 5 and data <= 7:
            data = data - 1
        return data
    except ValueError:
        print ('The data for recoding is not a number')
    return