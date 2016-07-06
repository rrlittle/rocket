'''
    this file is the main entry point for the rocket package. 
    if this is run like ```python rocket``` it takes one of two 
    arguments.

    template or convert

Usage:
    rocket.py template

'''
import utils
import sys
import argparse
from os import getcwd
from os.path import join, isfile, abspath
import csv
import tkinter
import tkinter.filedialog as filedialog
from MappingManager import MappingManager

from Managers import sinkManager, sourceManager

def load_handlers():
    ''' loads the handlers from the extensions module within this package
        and returns them'''
    handlers = {'source':{}, 'sink':{}}
    import data_handlers
    from inspect import getmembers, isclass, isfunction
    for name in data_handlers.__all__:
        for i in [b for b in getmembers(getattr(data_handlers,name)) \
            if isclass(b[1])]:
            
            if issubclass(i[1], sinkManager): 
                print('adding %s to sinkManagers'%i[0])
                handlers['sink'][i[0]] = i[1]
                for j in [f[0] for f in getmembers(i[1]) if isfunction(f[1])]: 
                    print('\t',j)
            if issubclass(i[1], sourceManager):
                print('adding %s to sourceManagers'%i[0])
                handlers['source'][i[0]] = i[1]
                for j in [f[0] for f in getmembers(i[1]) if isfunction(f[1])]: 
                    print('\t',j)
    print('\n\n\n')
    return handlers

class controller(object):
    ''' this is the main orchestrator of the rocket program.
        it has two interesting functions to the public. 
        make_template - which makes a template using a source and sink manager
                        which a user must fill out
        convert - which takes a source datafile and mapping template
                    and converts the source datafile into the output template
        
    '''

    def __init__(self, source=None, sink=None):
        ''' initializes a controller object. 
        basically that just asserts that source and sink are subclasses of 
            source and sink managers 
        '''
        assert issubclass(source, sourceManager), ('source must be a child '
            'of sourceManager')
        self.source = source()
        # self.source.load_schema()

        assert issubclass(sink, sinkManager), ('sink must be a child '
            'of sinkManager')
        self.sink = sink()
        # self.sink.load_schema()

        self.mapper = MappingManager(self.source, self.sink)

    # prompts the user for source and sink schemas and a location for 
    # 
    def make_template(self):
        ''' this function gets two schemas from self.source and self.sink
            and combines them into a mapping template wjic th user can fill out
        '''
        self.sink.load_schema()
        self.source.load_schema()
        raise NotImplementedError(" make_template not implemented yet.")

    # prompts the user for a template file if none set.
    # a sink datafile
    # a source datafile
    # and converts the source datafile into sink datafile
    def do_convert(self, template_path=None):
        sinkpath = self.sink.get_file_outpath()
        srcpath = self.source.get_data_path()
        
        template_path = self.mapper.get_template_path()

        self.mapper.load_template(self.template_path, 
                                srcpath)

        self.mapper.mapping() # do the mapping to fill sinktable

        # create the csv outfile
        # TODO remove this stuff. sink_table should be passed directly to sink
        sink_table = self.mapper.sink_table
        fieldnames = [c.col_name for c in sink_table[0]]
        
        self.sink.write_outfile(sink_table, sinkpath)

    # sets self.template_path. basically prompts the user for a
    # what template they would like to use.  
    def get_template_path(self):
        templ_file_path = filedialog.askopenfilename(title=('please select'
            ' template file'), 
            initialdir=join(getcwd(),'mapping_files'))
        if templ_file_path == '': 
            print('no template file selected. quitting')
            sys.exit()
        self.template_path = templ_file_path

handlers = load_handlers()

if __name__ == '__main__':
    parser = utils.make_args('runs the rocket data mapping package',
        args={
            '--template':{  'dest':'template',
                            'const':True,
                            'action':'store_const',
                            'help':'make the template from two schemes'
            },
            '--convert':{   'dest':'convert', 
                            'action':'store_const',
                            'const':True,
                            'help': (   'converts a source datafile to sink '
                                        'datafile using template')
            },
            '--src':{   'choices': list(handlers['source'].keys()),
                        'action':'store',
                        'dest':'source',
                        'help':'what is the source type you would like to use?',
                        'required':True,
            },
            '--sink':{  'choices': list(handlers['sink'].keys()),
                        'action':'store',
                        'dest':'sink',
                        'help':'what is the sink type you would like to use?',
                        'required':True,
            }
        })

    # # if this is run as a package
    # parser = argparse.ArgumentParser(
    #     description='runs the rocket data mapping package')
    # parser.add_argument('--template', 
    #     dest='template',
    #     const=True,
    #     action='store_const',
    #     help='make the template from two schemes'
    #     )
    # parser.add_argument('--convert', 
    #     dest='convert', 
    #     action='store_const',
    #     const=True,
    #     help=(  'converts a source datafile to sink '
    #             'datafile using template')
    #     )
    # parser.add_argument('--src',
    #     choices= list(handlers['source'].keys()),
    #     action='store',
    #     dest='source',
    #     help='what is the source type you would like to use?',
    #     required=True,
    #     )
    # parser.add_argument('--sink',
    #     choices= list(handlers['sink'].keys()),
    #     action='store',
    #     dest='sink',
    #     help='what is the sink type you would like to use?',
    #     required=True,
    #     )
    args = parser.parse_args()
    

    c = controller(source=handlers['source'][args.source], 
                sink=handlers['sink'][args.sink])
    template_path=None
    if args.template: 
        template_path = c.make_template()
    else: print('--template not provided, skipping that')

    datafile_path = None
    if args.convert: 
        datafile_path = c.do_convert(template_path=template_path)
    else: print('--convert not provided, skipping that')
    
