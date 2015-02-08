import errno
import os

class FilePicker:
    def __init__(self):
        self.flag_is_traversing_files = False
        self.file_list = []

    def set(self, root_dir):
        self.root_dir = root_dir
        if not os.path.isdir(root_dir):
            raise OSError(errno.ENOENT, 'No such directory', root_dir)
        
        self.flag_is_traversing_files = True
        
        for dir_name, subdirs, files in os.walk(root_dir):
            print('Found directory: %s' % dir_name)
            for file_name in files:
                print('\t%s' % file_name)
                if os.path.splitext(file_name)[1] == ".rar":
                    self.file_list.append([dir_name, file_name])


        self.flag_is_traversing_files = False

        
    def get_rars(self):
        for f in self.file_list:
            yield f

