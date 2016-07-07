'''
	this file is the main entry point for the rocket package. 
	if this is run like ```python rocket/``` 
	use ```python rocket -h``` for help text 

	try runing it witout any argumets and you will
	be a helpful text describing the argunents required 

	note: this was built for python 3
'''
from __init__ import handlers
from Managers import controller
import utils


if __name__ == '__main__': 
	# if this is run as a package
	# it requires arguments
	parser = utils.make_args('runs the rocket data mapping package',
		args={
			'--src':{   'choices': list(handlers['source'].keys()),
						# choices forces existing handler
						'action':'store',
						'dest':'source', # args.source
						'help':(	'required: choose one '
									'what is the source handler '
									'you would like to use?'),
						'required':True,
					},
			'--sink':{  'choices': list(handlers['sink'].keys()), 
						# choices forces existing handler
						'action':'store',
						'dest':'sink', # args.sink
						'help':(	'required: choose one '
									'what is the sink handler '
									'you would like to use?'),
						'required':True,
					},
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
						}
		}
	)
	args = parser.parse_args()
	src = handlers['sink'][args.source]
	sink = handlers['sink'][args.sink]

	c = controller(source=src, sink=sink)

	template_path = None
	if args.template:
		template_path = c.make_template()
		print('created template at %s'%template_path)
	else: print('--template not provided skipping that')

	outfile_path = None
	if args.convert: 
		outfile_path = c.do_convert(template_path=template_path)
		print('created outfile at %s'%outfile_path)
	else: print('--convert not provided skipping that')


