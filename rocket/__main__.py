'''
	this file is the main entry point for the rocket package.
	if this is run like ```python rocket/```
	use ```python rocket -h``` for help text

	try runing it witout any argumets and you will
	be a helpful text describing the argunents required

	note: this was built for python 3
'''
from __init__ import mapping_managers
from Controller import controller
import utils

parser = utils.make_args('runs the rocket data mapping package',
                         args={
                             ('-mm', '--mappingmanager'): {
                                 'choices': list(mapping_managers.keys()),
                                 'action': 'store',
                                 'required': True,
                                 'dest': 'mm',
                                 'help': ('required: choose one mapping'
                                          'manager you would like to use?')
                             },
                             ('-t', '--template'): {
                                 'dest': 'template',
                                 'const': True,
                                 'action': 'store_const',
                                 'help': 'make the template from two schemes'
                             },
                             ('-c', '--convert'): {
                                 'dest': 'convert',
                                 'action': 'store_const',
                                 'const': True,
                                 'help': ('converts a source datafile to sink '
                                          'datafile using template')
                             }
                         }
                         )

if __name__ == '__main__':
    # if this is run as a package
    # it requires arguments
    args = parser.parse_args()
    # print ('sources: %s <= %s'%(handlers['source'].keys(), args.source))
    # print ('sinks: %s <= %s'%(handlers['sink'].keys(), args.sink))
    # src = handlers['source'][args.source]
    # sink = handlers['sink'][args.sink]

    mappingManager = mapping_managers[args.mm]

    # print('chosen source: %s'%src)
    # print('chosen sink: %s'%sink)
    c = controller(mappingManager)

    template_path = None
    if args.template:
        template_path = c.make_template()
        print('created template at %s' % template_path)
    else:
        print('--template not provided skipping that')

    outfile_path = None
    if args.convert:
        outfile_path = c.do_convert(template_path=template_path)
        print('created outfile at %s' % outfile_path)
    else:
        print('--convert not provided skipping that')
