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
        

        self.flag_is_traversing_files = False

        
    def get_rars(self):
        for f in self.file_list:
            yield f

