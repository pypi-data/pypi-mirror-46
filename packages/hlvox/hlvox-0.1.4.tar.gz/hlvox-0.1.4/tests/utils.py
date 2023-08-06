import os.path
from pathlib import Path
import json
import wave
import struct

# normal_files = ["hello.wav", "my.wav", "name.wav", "is.wav", "vox.wav"
#                 "_comma.wav", "_period.wav"]
# empty_files = []
# no_punct_files = ["hello.wav", "my.wav", "name.wav", "is.wav", "vox.wav"]
# inconst_format_files = ["hello.mp3", "my.wav", "name", "is.wav", "vox.mp4",
#                         "_comma.wav", "_period.wav"]
# test_files = {"normal": normal_files, "empty": [],
#               "no_punct": no_punct_files, "inconst_format": inconst_format_files,
#               }


def create_test_files(audio_path, files_dict):
    audio_path_p = Path(audio_path)
    audio_path_p.mkdir(parents=True, exist_ok=True)

    for path_name in files_dict.keys():
        path_name_d = audio_path_p.joinpath(path_name)
        path_name_d.mkdir(parents=True, exist_ok=True)

        for file in files_dict[path_name]:
            filepath = path_name_d.joinpath(file)
            # savefile = open(filepath, "w")
            savefile = wave.open(str(filepath), "w")

            # channels, datasize (16 bit), sample rate, number of samples
            savefile.setparams((1, 2, 11025, 500, "NONE", "Uncompressed"))
            savefile.writeframes(struct.pack('h', 1))
            savefile.close()


def clean_test_files(audio_path, export_path, db_exports_only=False):
    audio_path_p = Path(audio_path)
    export_path_p = Path(export_path)

    if audio_path_p.is_dir():
        test_dirs = list(x for x in audio_path_p.iterdir() if x.is_dir())
        for dirc in test_dirs:

            # Delete info if it exists
            infopath_dir = dirc.joinpath("info/")
            if infopath_dir.is_dir() and not db_exports_only:
                infopath_file = infopath_dir.joinpath("info.json")
                os.remove(infopath_file)
                os.rmdir(infopath_dir)

            # Delete db if it exists
            db_dir = dirc.joinpath("db/")
            if db_dir.is_dir():
                db_file = db_dir.joinpath("db.json")
                os.remove(db_file)
                os.rmdir(db_dir)

            if not db_exports_only:
                files = list(dirc.iterdir())

                for file in files:
                    os.remove(file)
                os.rmdir(dirc)
        if not db_exports_only:
            os.rmdir(audio_path)

    if export_path_p.is_dir():
        voice_export_dirs = list(export_path_p.iterdir())
        for voice_export_dir in voice_export_dirs:
            files = list(voice_export_dir.iterdir())
            for file in files:
                os.remove(file)
            os.rmdir(voice_export_dir)
        os.rmdir(export_path_p)


def create_info(info_dict, audio_path):
    info_dir = Path(audio_path).joinpath("info/")

    info_dir.mkdir(parents=True, exist_ok=True)

    info_file = info_dir.joinpath("info.json")

    with open(info_file, 'w') as file:
        json.dump(info_dict, file)


# def create_sentence(export_path, sentence_filenames):
#     export_path_p = Path(export_path)

#     export_path_p.mkdir(parents=True, exist_ok=True)

#     for sentence in sentence_filenames:
#         filepath = export_path_p.joinpath(sentence)
#         savefile = open(filepath, "w")
#         savefile.close()


# if __name__ == "__main__":
#     create_sentence("./tests/tempexport", "hello-world.wav")
