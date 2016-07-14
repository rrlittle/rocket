''' This file implements several useful functions that can be used for the 
    template. Each function should take the argument of a list, and another extra  
    argument called args (which can be empty). Look like this (srcdat, args = None)
    Every data passed will be in the form of a list of string. If you want to do 
    numerical calculation, change that into the number. 
'''
def data_sum(srcdat, args=None):
    data_sum = 0
    for data in srcdat:
        try:
            data = float(data)
            data_sum = data_sum + data
        except ValueError:
            print ('In the calculation of the sum, one of the data: %s is not'
                   , 'a number' % data)
    return data_sum


def mean(srcdat, args=None):

    mean_sum = data_sum(srcdat, args)
    mean_num = len(srcdat)
    if mean_num == 0:
        print 'There is no data for calculating the mean'
        return

    mean = mean_sum / mean_num

    return mean


def recodeHBQ(srcdat, args=None):
    try:
        data = int(srcdat[0])
        if data > 4:
            data = data - 1
        return data
    except ValueError:
        print 'The data for recoding is not a number'

    return
