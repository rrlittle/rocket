import Managers
from loggers import col_log
from Functions.function_api import PlainCopy

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
                self.func = func
                return

        #self.func = self.handler.globalfuncs[self.func.strip()]['ref']
        raise self.handler.TemplateError(('function %s for column '
                                              '%s is not valid. please change the template'
                                              ' to a valid function or blank') % (self.func, self.col_name))

   # def _other_condition_for_drop_col_(self):
        # The NI in the default stands for Not Include, which will make this
        # column not show up in the final output
    #    if not isinstance(self.default, self.handler.NoDataError):
     #       if self.default == "NI":
      #          return True

    def map_src(self, srcrow):
        '''This method turn the attribute mappers into a list
            of corresponding srcCol Object.
        '''

        mappers_result = []
        if isinstance(self.mappers, str):
            mappers_id = self.mappers.split(',')
            for mid in mappers_id:
                cols = [col for col in srcrow if col.id == mid]
                assert len(cols) <= 1, 'non unique src ids (%s) in template' % mid
                assert len(cols) == 1, 'id (%s) specified does not exist' % mid
                mappers_result.append(cols[0])
            self.mappers = mappers_result

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
        except self.handler.DropRowException as e:
            raise self.handler.DropRowException(('Error raised while '
                                                 'running %s(%s). Error: %s') % (self.func, srcdat, e))

        except Exception as e:
            col_log.error('err while converting %s with %s: %s' % (self,
                                                                   src_datacol_zip, e))
            #return self.handler.NoDataError
            raise Exception(('Error raised while '
            'running %s(%s). Error: %s')%(self.func, srcdat, e))

        col_log.debug('CONVERTED TO (%s)' % self.dat)
        return self.dat
