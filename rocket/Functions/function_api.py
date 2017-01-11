import logging
logger = logging.getLogger("main_log.function")
class Function():
    '''This class should be memoryless about the data because this instance will be used for many
    times throughtout the whole program.
    Initialize support two keyword arguemnt:
        documentation: for the external change of the funciton documentation
        name: for the external change of the function name
    '''

    def __init__(self, *args, **kwargs):
        super(Function, self).__init__()
        self.documentation = kwargs.get("documentation", self.get_documentation())
        self.func_name = kwargs.get("name", self.get_name())

    def get_documentation(self):
        return "NO DOCUMENTATION IMPLEMENTED"

    def get_name(self):
        return NotImplementedError

    def execute(self, *data, args=None):
        '''
        This is the API for running the function. it receives *data from the
        outside as the tuple. Here the tuple will be casted to list.
        It also is used to provide debugger information, and error handling. No need to override this function
        :param data:
        :param args:
        :return:
        '''
        data_list = list(data)

        logger.debug("The function:%s is getting executed" %self.get_name())
        logger.debug("The data is %s" %data_list)
        logger.debug("The args is %s" %args)

        # execute the function.
        result = self._func_(data_list=data_list, args=args)

        logger.debug("The function:%s finishes correctly" %self.get_name())
        return result

    def _func_(self, data_list, args=None):
        '''
        This is the overrided part for execution. Put the logic of function here. It's best to return one thing
        Either raising exception or returning NoDataError will fill this cell with default value, except for raising
        DroppingRowException, which will stop the execution for this row and drop the finished part.

        :param data_list: the data in a list
        :param args: args used by user to configure the behavior of a Function. It should also be a list.
        :return:
        '''

        raise NotImplementedError


class PlainCopy(Function):

    def get_name(self):
        return "PlainCopy"

    def _func_(self, data_list, args=None):
        return data_list[0]
