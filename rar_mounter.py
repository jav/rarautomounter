#! /usr/bin/env python

#first import my own libraries
import file_picker

#then import system libraries
import argparse
import os
import subprocess
import sys


parser = argparse.ArgumentParser(description='Mount a compress filed as a dir.')
parser.add_argument('-d', '--base-dir', dest="basedir",
						required=True,
						help='Base directory.')
parser.add_argument('-l', '--make-links', nargs='+',
						default=['avi', 'mkv', 'mp4'],
						help='Automatically add a link to any files that matches fileendings (e.g. "--make-link avi mkv mp4")')
parser.add_argument('-n', dest='noop', action='store_true',
						default=False,
						help='All actions become noops')
parser.add_argument('--mount-command',
						default="archivemount",
						help='Mount command.')
parser.add_argument('--mount-options', nargs='*',
						default=['readonly', 'allow_other'],
						help="Optional arguments for the mount command. Single chars have '-' prepended, longer strings have '-o ' prepended.")
parser.add_argument('--umount-command',
						default="fusermount",
						help="Umount command.")
parser.add_argument('--umount-options', nargs='*',
						default=['u', 'z'])



args = parser.parse_args()

def error(err_str):
	sys.stderr.write("Error: %s"%(err_str, ))

def warn(warn_str):
	sys.stderr.write("Warning: %s"% (warn_str, ))

def mount(dest, source, mount_command, mount_options, noop):
	''' Attempt to create a mountpoint and mount the compressed file to there.'''
	mount_cmd = [mount_command, source, dest]
	for mount_option in mount_options:
		if len(mount_option) == 1:
			mount_cmd.append("-%s"%mount_option)
		else:
			mount_cmd.append("-o")
			mount_cmd.append(mount_option)
	if noop:
		print "mount(): subprocess.call(%s)" % (mount_cmd, )
	if not noop:
		print "subprocess.call(%s)" % (mount_cmd, )
		subprocess.call(mount_cmd)

def symlink(dest, dir_to_scan, ext, noop):
	'''Scan a mountpoint for files with extentions and
	   create symlinks to them.'''
	for f in os.listdir(dir_to_scan):
		if ext == os.path.splitext(f)[0]:
			print "link %s as %s" % (f, os.path.join(dest, f))

def create_mountpoint(mountpoint, noop):
	if len(os.listdir(mountpoint)) != 0:
		warn("mountpoint (%s) is not empty."%(mountpoint, ))
		if not noop:
			os.makedirs(dest)
		else:
			print "create dir %s"%mountpoint

def umount(d, umount_command, umount_options, noop):
	umount_cmd = [umount_command, d]
	for umount_option in umount_options:
		if len(umount_option) == 1:
			umount_cmd.append("-%s"%umount_option)
		else:
			umount_cmd.append("-o")
			umount_cmd.append(mount_option)
	if noop:
		print "umount(): subprocess.call(%s)" % (umount_cmd, )
	if not noop:
		print "subprocess.call(%s)" % (umount_cmd, )
		subprocess.call(umount_cmd)



def main(**kwargs):
	print "kwargs", kwargs
	basedir = kwargs['basedir'] #break if this fails
	noop = kwargs['noop']

	make_links = kwargs['make_links']

	mount_command = kwargs['mount_command']
	mount_options = kwargs['mount_options']

	umount_command = kwargs['umount_command']
	umount_options = kwargs['umount_options']



	fp = file_picker.FilePicker()
	fp.set(basedir)


	for dir_name, file_name in fp.get_rars():
		full_file_name = os.path.join(dir_name, file_name)
		mountpoint = "%s.mountpoint" % full_file_name
		source = full_file_name
		
		create_mountpoint(mountpoint, noop)
		if os.listdir(mountpoint) > 0:
			umount(mountpoint, umount_command, umount_options, noop)

		mount(mountpoint, source, mount_command, mount_options, noop)

		for ext in make_links:
			dir_to_scan = mountpoint
			symlink(dir_name, mountpoint, ext, noop)


	

if __name__ == '__main__':
	main(**vars(args))


