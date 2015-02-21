#! /usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description='Mount a compress filed as a dir.')
parser.add_argument('-d', '--base-dir', dest="basedir", required=True,
						help='Base directory.')
parser.add_argument('-l', '--make-links', nargs='+',
						help='Automatically add a link to any files that matches fileendings (e.g. "--make-link avi mkv mp4")')
parser.add_argument('-n', dest='noop', action='store_true', default=False,
						help='All actions become noops')

args = parser.parse_args()

print(args)




def main(**kwargs):
	print "kwargs", kwargs
	basedir = kwargs['basedir'] #break if this fails
	noop = kwargs.get('noop', False)
	make_links = kwargs.get('make_links', False)

	

if __name__ == '__main__':
	main(**vars(args))


