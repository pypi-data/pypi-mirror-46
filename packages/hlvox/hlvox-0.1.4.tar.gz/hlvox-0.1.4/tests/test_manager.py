import utils as th
import unittest
from pathlib import Path
from hlvox import Voice, Manager

test_filepath = "./tests/tempfiles"
test_filepath_p = Path(test_filepath)
test_exportpath = "./tests/tempexport"
test_exportpath_p = Path(test_exportpath)

test_files = {
    "v1": ["hello.wav"],
    "v2": ["hello.wav"],
    "v3": ["hello.wav"]
}


class test_voice_import(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        th.clean_test_files(test_filepath, test_exportpath)

        th.create_test_files(test_filepath, test_files)

    @classmethod
    def tearDownClass(cls):
        th.clean_test_files(test_filepath, test_exportpath)

    def setUp(self):
        self.tu = Manager(test_filepath, test_exportpath)

    def tearDown(self):
        self.tu.exit()

    def test_export_dir_creation(self):
        exp_export_dirs = [test_exportpath_p.joinpath("v1"),
                           test_exportpath_p.joinpath("v2"),
                           test_exportpath_p.joinpath("v3")]

        export_dirs = test_exportpath_p.iterdir()

        self.assertCountEqual(exp_export_dirs, export_dirs)

    def test_voice_list(self):

        exp_voice_list = ["v1", "v2", "v3"]

        self.assertCountEqual(exp_voice_list, self.tu.get_voice_names())


class test_get_voice(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        th.clean_test_files(test_filepath, test_exportpath)

        th.create_test_files(test_filepath, test_files)

    @classmethod
    def tearDownClass(cls):
        th.clean_test_files(test_filepath, test_exportpath)

    def setUp(self):
        self.tu = Manager(test_filepath, test_exportpath)

    def tearDown(self):
        self.tu.exit()

    def test_get_voice(self):
        voice = self.tu.get_voice("v1")

        self.assertEqual("v1", voice.name)

    def test_get_wrong_voice(self):
        voice = self.tu.get_voice("nope")

        self.assertEqual(None, voice)
