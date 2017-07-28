import Managers
from loggers import col_log
from Functions.function_api import PlainCopy, DropRowException, UserWarningNotificationException, UserErrorNotificationException
from error_generator import user_error_log
import re

class Col(object):
    ''' this represents one row from the template file.
        it defines the parameters for a column from either the source or
        the sink column.
        this will be extended by a sourceCol and sinkCol, which will each
        implent further src/sink dependant functions
    '''

    class BadColErr(Exception):
        pass  # column should not be created

    def __init__(self, sshandler, template_row):
        '''all columns need
            - a handler. this asserts its an sshandler instance
            - column definitions
                i.e. the row from the template. source coluns and sink columns
                    require different things. but they all need:
                    -  name
            '''

        # all columsn need to be aware of their handlers
        assert isinstance(sshandler, Managers.ssManager), ('handlers to colum objects '
                                                           'must be children of ssManager')
        self.handler = sshandler

        self.template_row = template_row

        self.load_attributes()

        if self.no_name() or self._other_condition_for_drop_col_() :
            raise self.BadColErr('Col_name must be defined to be a good Col')
        else:
            col_log.debug('created column %s' % self)

    def no_name(self):
        return isinstance(self.col_name, self.handler.NoDataError)

    def _other_condition_for_drop_col_(self):
        """
        # Should be overrided by the subclass to costumzing the condition for
        # not creating the column.
        :return: true if you want to stop making the column
        """
        return False

    def load_attributes(self):
        ''' loads all the attributes the handler knows about and
            therefore needs
            this shoud be called after init,
            but children of this should call it automatically in their init
        '''
        col_log.debug('loading attributes')
        for field in self.handler.template_fields:
            col_log.debug('loading %s' % field)
            self.load_attribute(field)

    def load_attribute(self, fieldkeyword):
        ''' this sets the self.fieldkeyword_header attribute
            & self.fieldkeyword attribute.

            the fieldkeyword_header is the column name from the manager
            the fieldkeyword is the value from the template for this row

            this throws a templateError if it can't find either the keyword in
            this manager or the indicated column in the template
        '''

        try:
            self._set_fieldkeyword_header_(fieldkeyword, post_fix='_header')


            # for every important field in a given hadler it should have a parse
            # function for that field called parse_'field'(fieldvalue)
            parser = self._get_parse_function_for_field_(fieldkeyword, parser_func_pre_fix="parse_")

            # make the value available right now
            thisheader = self.handler.template_fields[fieldkeyword];
            attribute_val = self.template_row[thisheader]  # get raw value

            setattr(self, fieldkeyword, parser(attribute_val, self))  # save parsed value

            col_log.debug('parsing %s from %s using %s' % (fieldkeyword,
                                                           attribute_val, parser.__name__))

        except Exception as e:
            raise self.handler.TemplateError(('Template not set up as expected.'
                                              ' could not parse it. error occured: %s') % e)

    def _set_fieldkeyword_header_(self, fieldkeyword, post_fix='_header'):
        header = fieldkeyword+post_fix
        setattr(self, header, self.handler.template_fields[fieldkeyword])

    def _get_parse_function_for_field_(self, fieldkeyword, parser_func_pre_fix = "parse_"):
        parser_func_name = 'parse_' + fieldkeyword
        return getattr(self.handler, parser_func_name,
                         self.handler.default_template_parser)

    # the following are required to use this obj as keys for a dict
    # you can also access them by their column name
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if hasattr(self, 'col_name'):
            return self.col_name
        else:
            return 'col_name not set for %s: %s' % (type(self), id(self))

    def __hash__(self):
        return self.col_name.__hash__()

    def __eq__(self, other):
        return self.col_name == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        return self.__str__() + str(other)


class srcCol(Col):
    ''' this adds funcitonality to columns defining specifcally
        to sink cols.
    '''

    def __init__(self, sourcehandler, template_row, **kwargs):
        ''' sourceCol requires some special things'''
        assert isinstance(sourcehandler, Managers.sourceManager), (
            'sinkCols require a source handler')

        Col.__init__(self, sourcehandler, template_row)

        # if there is no data in missing value, our default is the missing values
        if isinstance(self.missing_vals, self.handler.NoDataError):
            self.missing_vals = ''


class sinkCol(Col):
    ''' this adds funcitonality to columns defining specifcally
        to sink cols.
    '''

    def __init__(self, sinkhandler, template_row, **kwargs):
        '''sinkCol requires the handler to be a sinkManager'''
        assert isinstance(sinkhandler, Managers.sinkManager), (
            'sinkCols require a sink handler')

        Col.__init__(self, sinkhandler, template_row)

        # If no default has been entered, we see the default as a blank
        # Do I need to change
        if isinstance(self.default, self.handler.NoDataError):
            self.default = ''

        # set self.func to an actual function
        # use self.handler.globalfuncs to get func refereances or throw err
        if isinstance(self.func, self.handler.NoDataError): self.func = ''

        func_name = self.func.strip().lstrip()

        # If there is no function, then just use the plain copy
        if func_name == '':
            self.func = PlainCopy()
            return

        # if the function name actually exists as a function
        for func in self.handler.globalfuncs:
            if func.func_name == func_name:
                #import ipdb; ipdb.set_trace()
                self.func = func
                return
        user_error_log.log_mapping_error(self.col_name, self.id, "The function name is invalid.")

        #self.func = self.handler.globalfuncs[self.func.strip()]['ref']
        # This place can log user

        raise self.handler.TemplateError(('function %s for column '
                                              '%s is not valid. please change the template'
                                              ' to a valid function or blank') % (self.func, self.col_name))


    def find_mapping_columns(self, srcrow, sinkrow = None):
        """
            This method translates the mapper string to the actual data. Any column id surronded with "{}" is seen as
            the column id from sink manager.

        :param srcrow: the data row for source
        :param sinkrow: the data row for sink
        :return:
        """

        def find_col_in_col_lists(id, col_list):
            cols = [col for col in col_list if col.id == id]
            assert len(cols) <= 1, 'non unique sink ids (%s) in template' % id
            assert len(cols) == 1, 'id (%s) specified does not exist' % id
            return cols[0]

        INTEGER = "[0-9]+"
        SEQUENCE_COMMA = "{number}(,{number})*".format(number=INTEGER)

        # Example "{1,3},2,{3}"
        if isinstance(self.mappers, str):
            s = re.split("({.*?})", self.mappers) # *? means minimal catch for regular expression. {1},2,{3} will be matched as {1} not {1},2,{3}
            # [{1,3},2,{3}]
            col_data = []
            col_list = []
            for substring in s:
                if substring is None or substring == "":
                    continue
                match = re.search(SEQUENCE_COMMA, substring)
                if match:
                    items = match.group().split(",")
                    for id in items:
                        # {1,3} or {2}
                        if "{" in substring and "}" in substring:
                            # The number is the id, compare it with the sink row
                            # Find the column, and use the name as key
                            try:
                                sink_col = find_col_in_col_lists(id, sinkrow)
                                col_data.append(sinkrow[sink_col.col_name])
                                col_list.append(sink_col)
                            except KeyError as e:
                                user_error_log.log_mapping_error("The sink column id in the mapper string has to be smaller"
                                                                 "than the id of this column")
                                raise e
                        else:
                            src_col = find_col_in_col_lists(id, srcrow)
                            col_list.append(src_col)
                            col_data.append(srcrow[src_col.col_name])

            return col_list, col_data
        raise Exception("Unexpected error")

    # What this method should do is to parse 1,2, {1,2,3}, 4 into two columns. One has the sink column, the other
    # has the source column
    def find_mapping_columns_development2(self, srcrow, sinkrow=None):
        '''This method turn the attribute mappers into a list
            of corresponding srcCol Object.
        '''

        mappers_result = []
        sink_col_mapper = []

        source_col_id = []
        sink_col_id = []
        data_list = []

        def find_col_in_col_lists(id, col_list):
            cols = [col for col in col_list if col.id == id]
            assert len(cols) <= 1, 'non unique sink ids (%s) in template' % id
            assert len(cols) == 1, 'id (%s) specified does not exist' % id
            return cols[0]

        if isinstance(self.mappers, str):

            # split the string into a list of string by,
            # Find the curly bracket
            # then substring it
            # create a new string by combing the rest if there is still something after the curly bracket
            # split it

            # Use regular expression to check the syntax
            # This should be done before the program even gets down to this place

            # And this is the format. We can parse string with the template of this format

            curly_start_index = self.mappers.find("{")
            curly_end_index = self.mappers.find("}")
            if curly_start_index * curly_end_index < 0:
                raise Exception("Format error and syntax check fail")

            # If there are only source column
            if curly_start_index == -1 and curly_end_index == -1:
                mappers = [find_col_in_col_lists(id, srcrow) for id in self.mappers.split(",")]
                data_list = [srcrow[col.col_name] for col in mappers]

            if curly_start_index != -1 and curly_end_index != -1:
                sink_col_string = ""
                source_col_string = ""
                if curly_start_index > 0:
                    # Example: 1,2,3,{1,2},5
                    sink_col_string = self.mappers[curly_start_index + 1 : curly_end_index] # 1,2
                    source_col_string = self.mappers[:curly_start_index - 1] + self.mappers[curly_end_index + 1:] # 1,2,3,5
                elif curly_start_index == 0:

                    # Exmaple: {1,2,3},5,6
                    # If no souce col defined, e.g {1,2,3}, the source_col_string will be ""
                    sink_col_string = self.mappers[curly_start_index + 1: curly_end_index]  # 1,2,3
                    source_col_string = self.mappers[curly_end_index + 2:]  # 5,6


                sink_col = [find_col_in_col_lists(id, sinkrow) for id in sink_col_string.split(",")]
                sink_data = [sinkrow[col.col_name] for col in sink_col]

                source_col = []
                source_data = []
                if source_col_string != "":
                    source_col = [find_col_in_col_lists(id, srcrow) for id in source_col_string.split(",")]
                    source_data = [srcrow[col.col_name] for col in source_col]
                # to restore the position order in the source_col 1,2,3,5 -> 1,2,3,1,2(two are for sink),5
                mappers = source_col
                mappers[curly_start_index: curly_start_index] = sink_col

                data_list = source_data
                data_list[curly_start_index: curly_start_index] = sink_data

            return mappers, data_list

    def convert(self, src_datacol_zip):
        ''' this will convert the src_data to a proper value for this column
            src_col_def may be a list or a src_data

            sets self.value and returns it.
        '''

        # list of sequences, not list in Python 3
        unzip = list(src_datacol_zip)

        # change them to lsits so mutable
        srcdat = [i[0] for i in unzip]
        srccols = [i[1] for i in unzip]
        # print('srcdat:',srcdat)
        # print('*srcdat:',*srcdat)
        try:
            col_log.debug('CONVERTING %s for handler %s' % (self,
                                                            self.handler))
            col_log.debug('FROM dat (%s) using %s with args (%s)' % (
                srcdat, self.func.func_name, self.args))


            if isinstance(srcdat, self.handler.NoDataError):
                self.dat = srcdat
            elif hasattr(self.args, '__len__') and self.args.__len__() > 0:
                col_log.debug('CALLING %s(%s, %s)' % (self.func.func_name,
                                                      srcdat, [arg for arg in self.args]))
                arg  = [i for i in self.args]
                self.dat = self.func.execute(*srcdat, args=arg)
            else:
                col_log.debug('CALLING %s(%s)' % (self.func.__name__, srcdat))
                self.dat = self.func.execute(*srcdat)

        except UserErrorNotificationException as e:
            user_error_log.log_mapping_error(self.col_name, self.id, str(e))
            raise Exception(('Error raised while '
                             'running %s(%s). Error: %s') % (self.func, srcdat, e))
        except UserWarningNotificationException as e:
            user_error_log.log_mapping_warning(self.col_name, self.id, str(e))

        except DropRowException as e:
            raise DropRowException(('Error raised while '
                                                 'running %s(%s). Error: %s') % (self.func.func_name, srcdat, e))

        except Exception as e:
            col_log.error('err while converting %s with %s: %s' % (self,
                                                                   src_datacol_zip, e))
            #return self.handler.NoDataError
            raise Exception(('Error raised while '
            'running %s(%s). Error: %s')%(self.func.func_name, srcdat, e))

        col_log.debug('CONVERTED TO (%s)' % self.dat)
        return self.dat


