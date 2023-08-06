import os
from pathlib import Path
from hlvox.voice import Voice


class Manager:
    def __init__(self, voices_path, exports_path):
        self.voices_path = Path(voices_path)
        self.exports_path = Path(exports_path)
        self.voices = self._load_voices(self.voices_path)
        # self._create_export_dirs(self.voices.keys())

    def _load_voices(self, path):
        voices = {}
        voice_folders = list(x for x in path.iterdir() if x.is_dir())
        for voice_folder in voice_folders:
            export_path = self.exports_path / voice_folder.name
            export_path.mkdir(parents=True, exist_ok=True)
            new_voice = Voice(path=voice_folder, export_path=export_path)
            voices[new_voice.name] = new_voice
        return voices

    # def _create_export_dirs(self, voices):
    #     for voice in voices:
    #         path = self.exports_path / voice
    #         if not path.exists():
    #             os.mkdir(path)

    def get_voice_names(self):
        """Gets names of available voices

        Returns:
            list -- list of voice name strings
        """

        return list(self.voices.keys())

    def get_voice(self, name):
        """Get voice of requested name

        Args:
            name ({string}): name of voice to get

        Returns:
            {voxvoice}: requested voice
        """
        if name in self.voices:
            return self.voices[name]
        else:
            return None

    def exit(self):
        for voice_name in self.voices:
            self.voices[voice_name].exit()
