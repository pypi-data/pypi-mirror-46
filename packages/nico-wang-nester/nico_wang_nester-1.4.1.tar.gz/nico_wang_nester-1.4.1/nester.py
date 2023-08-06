""" This is the "nester.py" module and it provides one function called print_lot()
	which prints lists that may or may not include nested lists."""
import sys
def print_lol(the_list,intend=False,level=0,fn=sys.stdout):
	"""This function takes one positional argument called "the_list", which 
		is any Python list (of - possibly - nested lists). Each data item in the
		provided list is (recursively) printed to the screen on it's own line.
		The second argument is to insert the Tap when it comes across a nested list."""
		
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item,intend,level+1,fn=fn)
		else:
			if intend:
				print('\t' *level, end='',file=fn)
			print(each_item,file=fn)
