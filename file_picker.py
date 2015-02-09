import errno
import logging
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
        
        ext_prio = ['.rar', '.r00', '.000']
        for dir_name, subdirs, files in os.walk(root_dir):
            found_file = None
            for file_name in files:
                ext = os.path.splitext(file_name)[1]
                if ext in ext_prio:
                    if found_file is None:
                        found_file = file_name
                    elif ext_prio.index( ext ) < ext_prio.index(os.path.splitext(found_file)[1]): 
                        found_file = file_name

            if found_file is not None:
                self.file_list.append([dir_name, found_file])


        self.flag_is_traversing_files = False

        
    def get_rars(self):
        for f in self.file_list:
            yield f

