from pathlib import Path


def get_file_stem(file):
    return Path(file).stem


def get_mp3_filename(file):
    return Path(file).stem + '.mp3'


def get_speaker_timestams_file(file):
    return Path(file).stem + '_spk_ts.json'
