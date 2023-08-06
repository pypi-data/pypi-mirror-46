from pathlib import Path
import utils as th
from hlvox import Voice
import unittest


# Stand-in files for testing
normal_files = ["hello.wav", "my.wav", "name.wav", "is.wav", "vox.wav",
                "_comma.wav", "_period.wav"]
empty_files = []
no_punct_files = ["hello.wav", "my.wav", "name.wav", "is.wav", "vox.wav"]
inconst_format_files = ["hello.mp3", "my.wav", "name", "is.wav", "vox.mp4",
                        "_comma.wav", "_period.wav"]
alarm_files = ["hello.wav", "my.wav", "name.wav", "is.wav", "vox.wav",
               "_comma.wav", "_period.wav", "dadeda.wav", "woop.wav"]
alph_files = ["a.wav", "b.wav", "c.wav", "_comma.wav", "_period.wav"]
test_files = {"normal": normal_files, "empty": empty_files,
              "no_punct": no_punct_files, "inconst_format": inconst_format_files,
              "alarm": alarm_files, "alph": alph_files}


test_filepath = "./tests/tempfiles"
test_filepath_p = Path(test_filepath)
test_exportpath = "./tests/tempexport"
test_exportpath_p = Path(test_exportpath)

# Example info file
ex_info_file = {"alarms": ["dadeda", "woop"]}


test_files_paths = {name: test_filepath_p.joinpath(name)
                    for name in test_files.keys()}


class test_file_handling(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        th.clean_test_files(test_filepath, test_exportpath)

        th.create_test_files(test_filepath, test_files)

    def test_empty_files(self):
        with self.assertRaises(Exception) as error:
            Voice(test_files_paths["empty"],
                  test_exportpath_p.joinpath("empty"))

        self.assertEqual(str(error.exception), "No words found")

    # ?: Removed for now, could use some rethinking
    # def test_no_punct_files(self):
    #     # TODO: test no comma, no period, both

    #     with self.assertRaises(Exception) as error:
    #         Voice(test_files_paths["no_punct"], test_exportpath)

    #     self.assertEqual(str(error.exception), "Incomplete Punctuation")

    def test_inconsistent_format(self):

        with self.assertRaises(Exception) as error:
            Voice(test_files_paths["inconst_format"],
                  test_exportpath_p.joinpath("inconst_format"))

        self.assertEqual(str(error.exception), "Inconsistent Audio Formats")

    def test_audio_format(self):

        unit = Voice(test_files_paths["normal"],
                     test_exportpath_p.joinpath("normal"))

        self.assertEqual(unit.get_audio_format(), "wav")
        unit.exit()

    @classmethod
    def tearDownClass(cls):
        th.clean_test_files(test_filepath, test_exportpath)


class test_dict_contents(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        sub_test_files = ["normal", "alph"]
        th.create_test_files(test_filepath, dict(
            (key, test_files[key]) for key in sub_test_files))

    def setUp(self):
        self.tu = None

    def tearDown(self):
        self.tu.exit()

    def test_basic_dict(self):
        self.tu = Voice(test_files_paths["normal"],
                        test_exportpath_p.joinpath("normal"))

        expected_names = [
            name[:-4] for name in normal_files if name not in ["_comma.wav", "_period.wav"]]
        expected_names.extend([",", "."])

        tu_dict = self.tu.get_words()

        self.assertCountEqual(expected_names, tu_dict)

    def test_alphab(self):
        self.tu = Voice(test_files_paths["alph"],
                        test_exportpath_p.joinpath("alph"))

        expected_names = [",", ".", "a", "b", "c"]

        tu_dict = self.tu.get_words()

        self.assertEqual(expected_names, tu_dict)

    @classmethod
    def tearDownClass(cls):
        th.clean_test_files(test_filepath, test_exportpath)


class test_voice_info_loading(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        sub_test_files = ["alarm"]
        th.create_test_files(test_filepath, dict(
            (key, test_files[key]) for key in sub_test_files))
        th.create_info(ex_info_file, test_files_paths["alarm"])

    def setUp(self):
        self.tu = None

    def tearDown(self):
        self.tu.exit()

    def test_alarm_read(self):
        self.tu = Voice(test_files_paths["alarm"],
                        test_exportpath_p.joinpath("alarm"))
        print(self.tu.alarms)

        self.assertCountEqual(self.tu.alarms, ["dadeda", "woop"])

    @classmethod
    def tearDownClass(cls):
        th.clean_test_files(test_filepath, test_exportpath)


# TODO: sayable/unsayable might take the place of this


class test_sentence_lists(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        th.create_test_files(test_filepath, test_files)

    @classmethod
    def tearDownClass(cls):
        th.clean_test_files(test_filepath, test_exportpath)

    def setUp(self):
        self.tu = Voice(test_files_paths["normal"],
                        test_exportpath_p.joinpath("normal"))

    def tearDown(self):
        self.tu.exit()

    def test_empty_sentence(self):
        ret = self.tu.get_sentence_list("")

        self.assertEqual([], ret)

    def test_simple_sentence(self):
        ret = self.tu.get_sentence_list("hello")

        self.assertEqual(["hello"], ret)

    def test_simple_punct(self):
        ret = self.tu.get_sentence_list("hello, world")

        self.assertEqual(["hello", ","], ret)

    def test_comp_punct(self):
        ret = self.tu.get_sentence_list("hello , world. Vox , , says hi")

        self.assertEqual(["hello", ",", ".",
                          "vox", ",", ","], ret)

    def test_punct_only(self):
        ret = self.tu.get_sentence_list(",")

        self.assertEqual([","], ret)

    def test_no_space_punct(self):
        ret = self.tu.get_sentence_list(",.")

        self.assertEqual([",", "."], ret)

    def test_temp(self):
        ret = self.tu.get_sentence_list("hello. my name, is, vox")

        self.assertEqual(["hello", ".", "my", "name",
                          ",", "is", ",", "vox"], ret)

    def test_punct_location(self):
        # Not sure how to deal with types like ".hello"
        # for now it will treat it as just a period and throw out all the characters after it
        ret1 = self.tu.get_sentence_list("hello.")
        ret2 = self.tu.get_sentence_list(".hello")
        ret3 = self.tu.get_sentence_list(".hello.")

        self.assertEqual(["hello", "."], ret1)
        self.assertEqual(["."], ret2)
        self.assertEqual([".", "."], ret3)

    def test_trailing_whitespace(self):
        ret1 = self.tu.get_sentence_list("hello ")
        ret2 = self.tu.get_sentence_list("hello\n")
        ret3 = self.tu.get_sentence_list("hello \n")
        ret4 = self.tu.get_sentence_list("hello \n\r")
        ret5 = self.tu.get_sentence_list("hello \n\r vox ")

        self.assertEqual(["hello"], ret1)
        self.assertEqual(["hello"], ret2)
        self.assertEqual(["hello"], ret3)
        self.assertEqual(["hello"], ret4)
        self.assertEqual(["hello", "vox"], ret5)


class test_filename_from_sent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        th.create_test_files(test_filepath, test_files)

    @classmethod
    def tearDownClass(cls):
        th.clean_test_files(test_filepath, test_exportpath)

    def setUp(self):
        self.tu = Voice(test_files_paths["normal"],
                        test_exportpath_p.joinpath("normal"))

    def tearDown(self):
        self.tu.exit()

    def test_not_gen_sent(self):
        fp = self.tu.get_filepath_from_sent("hello")

        self.assertEqual(fp, None)

    def test_simple_sent(self):
        self.tu.generate_audio("hello")

        fp = self.tu.get_filepath_from_sent("hello")

        self.assertEqual(fp, test_exportpath_p.joinpath(
            "normal").joinpath("1.wav"))


class test_sayable_unsayable(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        th.create_test_files(test_filepath, test_files)

    @classmethod
    def tearDownClass(cls):
        th.clean_test_files(test_filepath, test_exportpath)

    def setUp(self):
        self.tu = Voice(test_files_paths["normal"],
                        test_exportpath_p.joinpath("normal"))

    def tearDown(self):
        self.tu.exit()

    def test_empty_sent(self):
        ret_say = self.tu.get_sayable("")
        ret_unsay = self.tu.get_unsayable("")

        self.assertEqual([], ret_say)
        self.assertEqual([], ret_unsay)

    def test_simple_sent(self):
        ret_say = self.tu.get_sayable("hello")
        ret_unsay = self.tu.get_unsayable("hello")

        self.assertEqual(["hello"], ret_say)
        self.assertEqual([], ret_unsay)

    def test_duplicates(self):
        sent = "hello hello world world , , . . duplicates! duplicates"

        ret_say = self.tu.get_sayable(sent)
        ret_unsay = self.tu.get_unsayable(sent)

        self.assertCountEqual(["hello", ",", "."], ret_say)
        self.assertCountEqual(
            ["world", "duplicates", "duplicates!"], ret_unsay)

    def test_comp_sent(self):
        sent = "hello, world. Vox can't say some of this."

        ret_say = self.tu.get_sayable(sent)
        ret_unsay = self.tu.get_unsayable(sent)

        self.assertCountEqual(["hello", ",", "vox", "."], ret_say)
        self.assertCountEqual(
            ["world", "can't", "say", "some", "of", "this"], ret_unsay)

    def test_dup_punct(self):
        sent = "hello... world"

        ret_say = self.tu.get_sayable(sent)
        ret_unsay = self.tu.get_unsayable(sent)

        self.assertCountEqual(["hello", "."], ret_say)
        self.assertCountEqual(["world"], ret_unsay)


class test_sentence_generation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        th.create_test_files(test_filepath, test_files)

    @classmethod
    def tearDownClass(cls):
        th.clean_test_files(test_filepath, test_exportpath)

    def setUp(self):
        self.tu = Voice(test_files_paths["normal"],
                        test_exportpath_p.joinpath("normal"))

        self.exp_ret = {"sentence": None,
                        "sayable": None,
                        "unsayable": None,
                        "path": None}

        self.exports = None
        self.exp_exports = None

    def tearDown(self):
        self.tu.exit()
        th.clean_test_files(test_filepath, test_exportpath,
                            db_exports_only=True)

    def test_empty_sent(self):
        ret = self.tu.generate_audio("")
        self.exports = list(test_exportpath_p.joinpath("normal").iterdir())

        self.exp_ret["sentence"] = ""
        self.exp_ret["sayable"] = []
        self.exp_ret["unsayable"] = []

        self.exp_exports = []

        self.assertEqual(self.exp_ret, ret)
        self.assertEqual(self.exp_exports, self.exports)

    def test_unsayable_sent(self):
        ret = self.tu.generate_audio("whatthefuckdidyoujustsaytome")
        self.exports = list(test_exportpath_p.joinpath("normal").iterdir())

        self.exp_ret["sentence"] = ""
        self.exp_ret["sayable"] = []
        self.exp_ret["unsayable"] = ["whatthefuckdidyoujustsaytome"]

        self.exp_exports = []

        self.assertEqual(self.exp_ret, ret)
        self.assertEqual(self.exp_exports, self.exports)

    def test_sayable_sent(self):
        sentence = "hello, my name is vox"
        ret = self.tu.generate_audio(sentence)

        # exp_path = test_exportpath_p.joinpath(
        #     "0.wav")

        exp_path = self.tu.get_filepath_from_sent("hello , my name is vox")
        self.exports = list(test_exportpath_p.joinpath("normal").iterdir())

        self.exp_ret["sentence"] = "hello , my name is vox"
        self.exp_ret["sayable"] = [",", "hello", "is", "my", "name", "vox"]
        self.exp_ret["unsayable"] = []
        self.exp_ret["path"] = exp_path

        self.exp_exports = [exp_path]

        self.assertEqual(self.exp_ret, ret)
        self.assertEqual(self.exp_exports, self.exports)

    def test_duplicate_sent(self):
        exp_path = test_exportpath_p.joinpath(
            "0.wav")
        self.tu.generate_audio("hello")
        self.tu.generate_audio("hello")

        exp_path = self.tu.get_filepath_from_sent("hello")

        self.exports = list(test_exportpath_p.joinpath("normal").iterdir())

        self.assertEqual(self.exports, [exp_path])

    def test_duplicate_words(self):
        ret = self.tu.generate_audio("hello hello hello")
        exp_path = self.tu.get_filepath_from_sent("hello hello hello")
        self.exports = list(test_exportpath_p.joinpath("normal").iterdir())

        self.exp_ret["sentence"] = "hello hello hello"
        self.exp_ret["sayable"] = ["hello"]
        self.exp_ret["unsayable"] = []
        self.exp_ret["path"] = exp_path

        self.exp_exports = [exp_path]

        self.assertEqual(self.exp_ret, ret)
        self.assertEqual(self.exp_exports, self.exports)

    def test_dup_punct(self):
        ret = self.tu.generate_audio("hello... hello")
        exp_path = self.tu.get_filepath_from_sent("hello . . . hello")
        self.exports = list(test_exportpath_p.joinpath("normal").iterdir())

        self.exp_ret["sentence"] = "hello . . . hello"
        self.exp_ret["sayable"] = [".", "hello"]
        self.exp_ret["unsayable"] = []
        self.exp_ret["path"] = exp_path

        self.exp_exports = [exp_path]

        self.assertEqual(self.exp_ret, ret)
        self.assertEqual(self.exp_exports, self.exports)

    def test_multiple_sent(self):

        self.tu.generate_audio("hello")
        self.tu.generate_audio("vox")
        self.tu.generate_audio(".")
        self.tu.generate_audio(",")

        test_paths = []
        test_paths.append(self.tu.get_filepath_from_sent("hello"))
        test_paths.append(self.tu.get_filepath_from_sent("vox"))
        test_paths.append(self.tu.get_filepath_from_sent("."))
        test_paths.append(self.tu.get_filepath_from_sent(","))

        # TODO: fix the stupid double joinpaths
        exp_paths = [test_exportpath_p.joinpath("normal").joinpath("1.wav"), test_exportpath_p.joinpath("normal").joinpath(
            "2.wav"), test_exportpath_p.joinpath("normal").joinpath("3.wav"), test_exportpath_p.joinpath("normal").joinpath("4.wav")]

        self.assertEqual(exp_paths, test_paths)

    # def test_potential_overwrite1(self):

    #     self.tu.generate_audio("hello.")
    #     self.tu.generate_audio("hello..")

    #     test_paths = []
    #     test_paths.append(self.tu.get_filepath_from_sent("hello"))
    #     test_paths.append(self.tu.get_filepath_from_sent("hello."))
    #     test_paths.append(self.tu.get_filepath_from_sent("hello.."))

    #     exp_paths = [test_exportpath_p.joinpath("normal").joinpath("1.wav"), test_exportpath_p.joinpath(
    #         "normal").joinpath("2.wav"), test_exportpath_p.joinpath("normal").joinpath("3.wav")]

    #     self.assertEqual(exp_paths, test_paths)

    # def test_potential_overwrite2(self):
    #     self.tu.generate_audio("hello")

    #     test_paths = []
    #     test_paths.append(self.tu.get_filepath_from_sent("hello"))

    #     exp_paths = [test_exportpath_p.joinpath("normal").joinpath("1.wav")]

    #     self.assertEqual(exp_paths, test_paths)

    #     self.tu.generate_audio("hello.")


class test_get_sayable_string(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        th.create_test_files(test_filepath, test_files)

    @classmethod
    def tearDownClass(cls):
        th.clean_test_files(test_filepath, test_exportpath)

    def setUp(self):
        self.tu = Voice(test_files_paths["normal"],
                        test_exportpath_p.joinpath("normal"))

    def tearDown(self):
        self.tu.exit()

    def test_simple_sent(self):
        ret = self.tu.get_sentence_string("hello")

        self.assertEqual(ret, "hello")

    def test_comp_sent(self):
        ret = self.tu.get_sentence_string("hello. my name, is, vox")

        self.assertEqual(ret, "hello . my name , is , vox")


class test_get_generated_sentences(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        th.create_test_files(test_filepath, test_files)

    @classmethod
    def tearDownClass(cls):
        th.clean_test_files(test_filepath, test_exportpath)

    def setUp(self):
        self.tu = Voice(test_files_paths["normal"],
                        test_exportpath_p.joinpath("normal"))

    def tearDown(self):
        self.tu.exit()
        th.clean_test_files(test_filepath, test_exportpath,
                            db_exports_only=True)

    def test_no_sentences(self):
        ret = self.tu.get_generated_sentences()

        self.assertEqual(ret, [])

    def test_single_sentences(self):
        self.tu.generate_audio("hello")

        ret = self.tu.get_generated_sentences()

        self.assertEqual(ret, ["hello"])

    def test_multiple_sentences(self):
        self.tu.generate_audio("hello")
        self.tu.generate_audio("vox")

        ret = self.tu.get_generated_sentences()

        self.assertEqual(ret, ["hello", "vox"])
