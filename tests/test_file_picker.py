import logging
import os
import shutil
import tempfile
import unittest

import file_picker

log = logging

class test(unittest.TestCase):
    
    def SetUp(self):
        pass

    def test_list_rar_files_from_empty_dir(self):
        try:
            root_dir = tempfile.mkdtemp()
            os.mkdir(os.path.join(root_dir, "empty_dir"))
            fp = file_picker.FilePicker()
            fp.set(root_dir)
            self.assertEquals(0, sum(1 for i in fp.get_rars()))
        finally:
            try:
                shutil.rmtree(root_dir)  # delete directory
            except OSError as exc:
                if exc.errno != errno.ENOENT:  # ENOENT - no such file or directory
                    raise  # re-raise exception


    def test_get_nothing_from_a_spammy_dir(self):
        try:
            root_dir = tempfile.mkdtemp()
            os.mkdir(os.path.join(root_dir, "spammy_dir"))

            for f in ["test", "test.raar", "test.r4r", "test.00x", "rar"]:
                open(os.path.join(root_dir, f), 'a').close()
        
            fp = file_picker.FilePicker()
            fp.set(root_dir)
            self.assertEquals(0, sum(1 for i in fp.get_rars()))

        finally:
            try:
                shutil.rmtree(root_dir)  # delete directory
            except OSError as exc:
                if exc.errno != errno.ENOENT:  # ENOENT - no such file or directory
                    raise  # re-raise exception

    def test_get_rar_from_dir(self):
        try:
            needle_rar = "needle.rar"
            root_dir = tempfile.mkdtemp()
            os.mkdir(os.path.join(root_dir, "dir"))

            for f in ["test", "test.raar", "test.r4r", "test.00x", "rar", needle_rar]:
                open(os.path.join(root_dir, f), 'a').close()
        
            for f in os.listdir(root_dir):
                print os.path.join(root_dir, f)

            fp = file_picker.FilePicker()
            fp.set(root_dir)
            log.debug(list(fp.get_rars()))
            self.assertEquals(1, sum(1 for i in fp.get_rars()))
            self.assertEquals(
                [[root_dir, needle_rar]], 
                list(fp.get_rars())
            )

        finally:
            try:
                shutil.rmtree(root_dir)  # delete directory
            except OSError as exc:
                if exc.errno != errno.ENOENT:  # ENOENT - no such file or directory
                    raise  # re-raise exception
