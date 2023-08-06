from optparse import OptionParser 
parser = OptionParser() 

add_option = parser.add_option
options = None
args = None

def parse():
	global options
	global args
	if None == options:
		(options, args) = parser.parse_args() 


def option():
	global options
	parse()
	return options

"""
if options.pdcl==True: 
    print 'pdcl is true' 
if options.zdcl==True: 
    print 'zdcl is true' 
"""
