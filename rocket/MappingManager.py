from Managers import sourceManager, sinkManager, Manager
import utils
from __init__ import templatedir, templ_delimiter, secretdir
from loggers import map_log
from  template_kit.template_writer import TemplateWriter
from template_kit.template_parser import TemplateParser, TemplateParseError
from template_kit.TemplateComponents import Header
from template_kit.components_behavior_protocols import ComponentResponseProtocol, ComponentWriteProtocol
from template_kit.template_structure import TemplateStructure
import csv
from os import startfile,rename, path, remove
from Functions.function_api import DropRowException, UserErrorNotificationException, UserWarningNotificationException
from error_generator import user_error_log

class MappingManager(Manager, ComponentResponseProtocol, ComponentWriteProtocol):
    ''' this class is responsible for implementing the
        core algorithms governing the operation of
        the conversion routine.
        it is also in charge of creation and parsing of
        the template file.
    '''
    delimiter = templ_delimiter

    def __init__(self, source=sourceManager, sink=sinkManager):
        ''' it's imperative that this instance know about
            a source and sink manager. they are the providers
            for all the information in the raw files.
            this should never be using raw info
        '''
        super(MappingManager, self).__init__()

        assert issubclass(source, sourceManager), 'Source has to be the'\
                                                  'subclass of sourceManager, not %s' % source
        assert issubclass(sink, sinkManager), 'Sink must be the subclass of sinkManager, '\
                                              'not %s' % sink
        self.source = source()
        self.sink = sink()
        # let the source and sink know which mapping manager it is
        self.source.mapping_manager = self
        self.sink.mapping_manager = self

        # ensures that src and sink do not have colliding fieldnames
        # if they do there will be an issue with parsing and creating the
        # template all the headers must template headers must be unique
        self.check_valid_src_sink_combo()

        # make the functions of each available via utils
        # check for naming conflicts
        # pass functions down to sink manager for the sinkcolumns to use
        self.globalfuncs = self.load_functions()
        setattr(self.sink, 'globalfuncs', self.globalfuncs)

        # set the structure
        # I want to update the structure
        self.template_structure = self.get_template_structure()
        self.user_notice = ""

    def get_template_structure(self):
        """
        validate the type of the template_structure
        :return:
        """
        template_structure = self._set_template_structure_()
        if isinstance(template_structure, TemplateStructure):
            return template_structure
        raise Exception("set template structure has to set an instance of TemplateStructure")

    def _set_template_structure_(self):
        template_structure = TemplateStructure()
        template_structure.set_to_default_structure()
        return template_structure

    def load_functions(self):
        """ must be overriden by Mapping manager subclasses.in order to include functions
        that are aware of both source and sink schemes.It should be a dictionary looks like
        {"mean":{"ref": mean }  },
        mean is the reference of the mean function
        """
        return {}

    def check_valid_src_sink_combo(self):
        ''' ensures that src and sink do not have colliding fieldnames
            if they do there will be an issue with parsing and creating the
            template all the headers must template headers must be unique'''
        # generate list of all the headers
        template_headers = list(self.source.template_fields.values()) + list(self.sink.template_fields.values())

        # find collisions
        collisions = []
        tmp = []

        for header in template_headers:
            if header not in tmp:
                tmp.append(header)
            else:
                collisions.append(header)

        # raise error if there are any collisions
        if len(collisions) != 0:
            raise self.TemplateError(('collisions detected in src and'
                                      ' sink handler template_fieldnames. please modify these fields '
                                      'to ensure unique headers: %s') % collisions)

    def parse_template(self, will_respond=True):
        """
            this function utilises self.sink and self.source
            to parse the template file. each manager will
            take the columns they know about.

            After the parser parses the template, it will send those data through
            the protocal method implemented below, started with "respond_to_...".

            For "mapping info", after the mapping manager receives the mapping info, it will ask the
            sink and source manager to parse it by using load-template

            For "User notice",

        :param will_respond:
                    If this flg is true, than the template will use itself as the delegator, leading those
                delegate methods get executed after the completion of the parser.

                    If this flag is false, than the template will use a default delegater, which basically does nothing
        :return:
        """

        '''This is a hard code template parser. Later it shall be refactored to accept customized template'''

        parser = None
        if will_respond:

            # the parser will notify the delegator to respond to the template
            # Mapping manager will read in the mapping information here
            parser_with_delegate = self.template_structure.get_template_parser(delegate=self)
            parser_with_delegate.parse_template(self.get_template_filepath())
            parser_with_delegate.close_file()
            return
        else:
            parser_without_delegate = self.template_structure.get_template_parser()
            parser_without_delegate.parse_template(self.get_template_filepath())
            parser_without_delegate.close_file()

    def get_template_filepath(self, title='Template', allownew=False, save=False):
        ''' this gets the filepath to a file. which is assumed to be
            a template file. we will rely on source sink handlers for error
            checking when they load it in

            allownew should decide if it's okay to allow a new file or not
        '''
        if hasattr(self, 'templ_path'):
            return self.templ_path

        self.templ_path = self.get_filepath(title=title,
                                            initialdir=templatedir,
                                            save=save,
                                            filetype='templates',
                                            allownew=allownew)
        return self.templ_path

    def _remind_user_notice_(self):
        '''This will be called before user tries to load the data
        This should be overrided by respond_to_user_notice. Soon this should
        give the user an option about whether they want read it. Default is show
        '''
        if self.user_notice != "":
            prompt = "\n The template has this important instruction on how to use the template.\n" \
                     " Please read it and press ENTER to continue the whole process \n\n"
            prompt += "User Notification: \n"
            prompt += "%s" % self.user_notice
            input(prompt)

    def load_source_data(self):
        # User notice may have some important information about how to load source data
        map_log.critical('loading data')
        self._remind_user_notice_()
        self.source.load_data()  # ensure src has data

    def convert(self, clear_sink=True):
        ''' this function implements the core algorithm of rocket.
            this sets up the core behaviour of the template files.
            basically it applies the function specified with the
            arguments provided to the columns in the source
            and save the returning value in sink.

            the goal here is to fill up sink.data in prep for sink.write
        '''

        if clear_sink:  # if sink is not already initialized
            self.sink.initialize_data()  # clear any data in sink
        for rowid, srcrow in enumerate(self.source):
            self.sink.add_row()  # we want to fill in a new row
            map_log.info('converting row {0}'.format(rowid))

            try:
                # go through all the columns defined in the template
                for sinkcoldef in self.sink.col_defs:
                    try:

                       # mapperslist = sinkcoldef.find_mapping_columns(srcrow=srcrow, sinkrow=self.sink[-1])
                        mapperslist, srcdat = sinkcoldef.find_mapping_columns(srcrow=srcrow, sinkrow=self.sink[-1])
                        # get col objs from src
                        # src cols required to compute the sink value

                        if not isinstance(mapperslist, self.sink.NoDataError):
                            #srccols = self.source.get_column_defs(*mapperslist)
                            # list of columns in the source datafile we need to grab

                            # get the data
                            # srcdat = [srcrow[col.col_name] for col in mapperslist]

                            # list of data values from src datafile
                            # zip the data with it's defining object
                            # needed for sinkcol.convert

                            # convert it to the sink value using the function inside sinkcoldef
                            sinkdat = sinkcoldef.convert(zip(srcdat, mapperslist))

                            # print('output:',sinkdat)
                            # save the sink value to the last row
                            self.sink[-1][sinkcoldef] = sinkdat

                        else:
                            self.sink[-1][sinkcoldef] = self.sink.NoDataError()
                            # self.sink[-1][sinkcoldef] = sinkcoldef.default


                    except DropRowException as e:
                        user_error_log.log_runtime_warning(column_name=sinkcoldef.col_name, column_id=sinkcoldef.id,
                                                           message=str(e))
                        raise e
                    except Exception as e:
                        map_log.error(('A not drop row exception happen when'
                                       'processing data in a row: %s') % e)
                        self.sink[-1][sinkcoldef] = self.sink.NoDataError()
                        continue

                # after the row is done use ensure row
                self.sink.ensure_row(self.sink.data[-1])  # raise drop row exception if row not right

            except DropRowException as e:
                # drop the row if it should't be included in the dataset
                map_log.error(('not including source row %s in sink: err'
                               ' at %s (%s)') % (rowid, sinkcoldef, e))
                self.sink.drop_row()
            except Exception as e:
                map_log.error('not droprow exception: %s' % e)
                continue

        map_log.critical('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nDONE CONVERSION')
        return self.sink.data

    def get_mapperids(self, mapper_string):
        # print('################### %s'%mapper_string)
        mapper_ids = []
        if '::' not in mapper_string:
            return mapper_string.split(',')

        if '::' in mapper_string:
            mapper_temp = mapper_string.split('::')
            try:
                start = int(min(mapper_temp))
                end = int(max(mapper_temp))
                mapper_ids = [str(x) for x in range(start, end + 1)]
                return mapper_ids
            except ValueError:
                raise DropRowException

    def make_template(self, delegate=None):
        ''' leverages the sink and source handlers to make the template
            file.

            writes handler documentation as top header using
            self.template_header

            then calls sink handler to write it's documentation as the second
            header

            then calls source header to write it's documentation as the third
            header

            then writes global funcs with their documentation as the 4th header

            finally uses sink.get_template_fields and source.get_template_fields
            to populate the final template header.

            then calls sink and source.populate_template to populate the
            template.

            for a specific mapping manager include a list of strings to be
            included as the header for that thing.
        '''

        def _get_template_path_():
            if hasattr(self, 'templ_path'):
                return self.templ_path
            else:
                return self.get_template_filepath(title='Select a template file',
                                                  save=True, allownew=True)

        def handle_tmeplate_err(errstr, err):
            map_log.error(('%s... Template field getting deleted and '
                           'rocket quitting. Error: %s') % (errstr, err))
            raise Exception()

        templ_path = _get_template_path_()
        try:
            if delegate is not None:
                template_writer = self.template_structure.get_template_writer(delegate=delegate, delimiter=self.delimiter)
            else:
                template_writer = self.template_structure.get_template_writer(delimiter=self.delimiter)
            template_writer.write_template(templ_path)
            template_writer.close_and_save_file()

        except Exception as e:
            handle_tmeplate_err("Template Error", e)
        # the template fields for each handler are defined upon initialization
        # of the handlers. they are defined in the code and extended for each
        # custom handler if they so choose.
        # they will be in order of definition in the __init__
            return None
        finally:
            pass

        map_log.debug('Template created')
        return templ_path

    def update_header(self):

        try:
            self.parse_template(will_respond=False)
        except TemplateParseError as e:
            map_log.critical("Template Error, exiting updating")
            return

        # Update the data in the header
        for c in self.template_structure.components:
            if isinstance(c, Header):
                header_list = self._get_headers_content_()
                header_list_with_indention = [[""] + line for line in header_list]
                c.content = header_list_with_indention
            break

        # rename the old file as backup
        template = self.get_template_filepath()
        template_dir, filename = path.split(template)
        temp_name = path.join(template_dir, filename + "temp")
        rename(template, temp_name)

        # if the any exception happens
        try:
            self.make_template(delegate=None)
            remove(temp_name)
        except Exception as e:
            rename(temp_name,template)
        return template

    def update_error(self):
        try:
            self.parse_template(will_respond=False)
        except TemplateParseError as e:
            map_log.critical("Template Error, exiting updating")
            return

        template = self.get_template_filepath()
        template_dir, filename = path.split(template)
        temp_name = path.join(template_dir, filename + "temp")
        try:
            rename(template, temp_name)
        except PermissionError as e:
            input(('FAIL: Template %s was not opened successfully for updating error. perhaps it is open. '
                   'close it and hit enter to cont') % template)
            rename(template, temp_name)

        try:
            self.make_template(delegate=user_error_log)
            remove(temp_name)
        except Exception as e:
            remove(template)
            rename(temp_name, template)
        return template

    #########################################################################################
    # These are the delegates method that is used to determine what to do
    # with different components
    ##################################################################################
    def respond_to_instru_info(self, instru_info):
        self.sink.set_instru_info(instru_name=instru_info.get_instru_name(), version=instru_info.get_version())

    def respond_to_header(self, header):
        self.header = header

    def respond_to_mapping_info(self, mapping_info):
        for handler in [self.source, self.sink]:
            map_log.debug(('loading template into '
                           'handler %s') % type(handler).__name__)
            mapping_info.seek(0)
            handler.load_template(mapping_info)

    def respond_to_user_notice(self, user_notice):
        self.user_notice = user_notice

    # delegate method for writing the tempalte
    def add_extra_content_to_header(self, header):
        header_list = self._get_headers_content_()
        header_list_with_indention = [[""]+line for line in header_list]
        header.content = header_list_with_indention

    def _get_headers_content_(self):
        header = []
        header = self.add_templ_header(header)
        header = self.sink.add_templ_header(header)
        header = self.source.add_templ_header(header)
        header = self._get_func_names_(header)
        return header

    # I want to add the explanation to function name
    # One line a function explanation
    def _get_func_names_(self, header_content=[]):
        def _add_all_func_name():
            all_func_name = [x for x in self.globalfuncs]
            return all_func_name

        def _add_functions_with_explanation_():
            '''
            This function will be used to add the explanation for the function
            :return:
            '''
            all_funcs = []

            # If I add the class for Function. You can default the func_explanation in the function superclass
            # and no catch needs to be done.

            for func in self.globalfuncs:

                # try:
                #     func_explanation = self.globalfuncs[x]['doc']
                # except KeyError:
                #     func_explanation = "NO EXPLANATION right now"
                # Generate the function line
                func = ["", func.func_name, func.documentation]
                all_funcs.append(func)
            return all_funcs

        func_header_prompt = ["Possible functions you can use are: "]
        func_header = _add_functions_with_explanation_()

        header_content.append(func_header_prompt)
        header_content += func_header
        return header_content

    def add_extra_content_to_mapping_info(self, mapping):
        mapping.content.append(self._add_mapping_headers_from_src_sink())

    def _add_mapping_headers_from_src_sink(self):
        srctemplatefields = list(self.source.template_fields.values())
        sinktemplatefields = list(self.sink.template_fields.values())
        return sinktemplatefields + srctemplatefields

    def add_extra_content_to_instru_info(self, instru_info):
        instru_key = instru_info.INSTRU_NAME_KEY
        version_key = instru_info.VERSION_KEY
        instru_info_line = ["", instru_key, "", version_key, ""]
        instru_info.content.append(instru_info_line)