import logging
import os
import tempfile
import unittest

import file_picker

log = logging

class test(unittest.TestCase):
    
    def SetUp(self):
        pass

    def test_list_rar_files_from_empty_dir(self):
        root_dir = tempfile.mkdtemp()
        os.mkdir(os.path.join(root_dir, "empty_dir"))
        fp = file_picker.FilePicker()
        fp.set(root_dir)
        self.assertEquals(0, sum(1 for i in fp.get_rars()))
