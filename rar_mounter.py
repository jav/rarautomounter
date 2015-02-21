#! /usr/bin/env python

#first import my own libraries
import file_picker

#then import system libraries
import argparse
import os


parser = argparse.ArgumentParser(description='Mount a compress filed as a dir.')
parser.add_argument('-d', '--base-dir', dest="basedir", required=True,
						help='Base directory.')
parser.add_argument('-l', '--make-links', nargs='+', default=[],
						help='Automatically add a link to any files that matches fileendings (e.g. "--make-link avi mkv mp4")')
parser.add_argument('-n', dest='noop', action='store_true', default=False,
						help='All actions become noops')

args = parser.parse_args()

def mount(dest, source):
	print "mount(): dest: %s, source: %s" % (dest, source)

def symlink(dest, dir_to_scan, ext):
	print "link(): dest: %s, dir_to_scan: %s, exts: %s" % (dest, dir_to_scan, ext)

def main(**kwargs):
	print "kwargs", kwargs
	basedir = kwargs['basedir'] #break if this fails
	noop = kwargs.get('noop', False)
	make_links = kwargs.get('make_links', False)


	fp = file_picker.FilePicker()
	fp.set(basedir)


	for dir_name, file_name in fp.get_rars():
		full_file_name = os.path.join(dir_name, file_name)
		mountpoint = "%s.mountpoint" % full_file_name
		source = full_file_name
		mount(mountpoint, source)
		for ext in make_links:
			dir_to_scan = mountpoint
			symlink(dir_name, mountpoint, ext)


	

if __name__ == '__main__':
	main(**vars(args))


