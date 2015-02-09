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

    def test_get_rar_variants_from_dirs(self):
        try:
            needle_rar = "needle.rar"
            root_dir = tempfile.mkdtemp()
            os.mkdir(os.path.join(root_dir, "dir"))
            
            needle_rar = "needle.rar"
            needle_r00 = "needle.r00"
            needle_000 = "needle.000"

            dir_structure = [
                ["dir1", ["test", "test.00x", "rar", needle_rar]],
                ["dir2", ["test", "test.00x", "rar", needle_000, needle_r00, needle_rar]],
                ["dir3", ["test", "test.00x", "rar", needle_r00, needle_rar, needle_000]],
                ["dir4", ["test", "test.00x", "rar", needle_rar, needle_000, needle_r00]],
                ["dir5", ["test", "test.00x", "rar", needle_000, needle_r00]],
                ["dir6", ["test", "test.00x", "rar", needle_r00, needle_000]],
                ["dir7", ["test", "test.00x", "rar", needle_000]],
            ]
# variant 1 Plain rar
            for (d, files) in dir_structure :
                os.mkdir(os.path.join(root_dir, d))
                for f in files:
                    open(os.path.join(root_dir,d, f), 'a').close()

            fp = file_picker.FilePicker()
            fp.set(root_dir)
            log.debug(list(fp.get_rars()))
            self.assertEquals(7, sum(1 for i in fp.get_rars()))
            self.assertEquals(
                [
                    [os.path.join(root_dir, 'dir1'), needle_rar],
                    [os.path.join(root_dir, 'dir2'), needle_rar],
                    [os.path.join(root_dir, 'dir3'), needle_rar],
                    [os.path.join(root_dir, 'dir4'), needle_rar],
                    [os.path.join(root_dir, 'dir5'), needle_r00],
                    [os.path.join(root_dir, 'dir6'), needle_r00],
                    [os.path.join(root_dir, 'dir7'), needle_000],
                ], 
                list(fp.get_rars())
            )

        finally:
            try:
                shutil.rmtree(root_dir)  # delete directory
            except OSError as exc:
                if exc.errno != errno.ENOENT:  # ENOENT - no such file or directory
                    raise  # re-raise exception
