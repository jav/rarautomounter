#! /usr/bin/env python

#first import my own libraries
import file_picker

#then import system libraries
import argparse
import os
import subprocess
import sys



def error(err_str):
	sys.stderr.write("Error: %s\n"%(err_str, ))

def warn(warn_str):
	sys.stderr.write("Warning: %s\n"% (warn_str, ))

def actions_log(fh, cmd, arg):
	fh.write("%s %s\n"%(cmd, arg))

def mount(dest, source, mount_command, mount_options, actions_log_fh, noop):
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
		ret = subprocess.call(mount_cmd)
		if ret == 0:
			actions_log(actions_log_fh, "mount", dest)

def symlink(dest, dir_to_scan, ext, actions_log_fh, noop):
	'''Scan a mountpoint for files with extentions and
	   create symlinks to them.'''
	for f in os.listdir(dir_to_scan):
		if ext == os.path.splitext(f)[1].replace('.', ''):
			print "link %s as %s" % (os.path.abspath(os.path.join(dir_to_scan, f)), os.path.join(dest, f))
			if not noop:
				#TODO: if the file exists, and is not a symlink, abort
				#TODO :if the file exists and is a symlink, remove it
				#create the symlink
				try:
					os.symlink(
						os.path.abspath(os.path.join(dir_to_scan, f)),
						os.path.join(dest, f)
						)
					actions_log(actions_log_fh, "symlink", os.path.join(dest,f))
				except:
					pass # Because I don't know how to handle a failure of this

def create_mountpoint(mountpoint, actions_log_fh, noop):
	if len(os.listdir(mountpoint)) != 0:
		warn("mountpoint (%s) is not empty."%(mountpoint, ))
		if not noop:
			try:
				os.makedirs(mountpoint)
				actions_log(actions_log_fh, "mk_mountpoint", os.path.join(dest,f))
			except OSError as exc:
				warn(exc)
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

	actions_log_fh = kwargs['actions_log_fh']


	fp = file_picker.FilePicker()
	fp.set(basedir)


	for dir_name, file_name in fp.get_rars():
		full_file_name = os.path.join(dir_name, file_name)
		mountpoint = "%s.mountpoint" % full_file_name
		source = full_file_name
		
		create_mountpoint(mountpoint, actions_log_fh, noop)
		if os.listdir(mountpoint) > 0:
			umount(mountpoint, umount_command, umount_options, noop)

		mount(mountpoint, source, mount_command, mount_options, actions_log_fh, noop)

		for ext in make_links:
			dir_to_scan = mountpoint
			symlink(dir_name, mountpoint, ext, actions_log_fh, noop)


	

if __name__ == '__main__':
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
	parser.add_argument('--actions-log', dest="actions_log_fh",
							type=argparse.FileType('w'),
							default="actions.log",
							help="Actions log for cleanup operations.")
	parser.add_argument('--debug',
							default=False
							help="Debug output.")

	args = parser.parse_args()

	main(**vars(args))


