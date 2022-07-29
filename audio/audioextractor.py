import os

from os import walk, path
from pathlib import Path
from moviepy import editor as mp
import confs

import logging, sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")


def extract_audio_from_video(video_file, audio_path):
    audio_file = path.join(audio_path, Path(video_file).stem + '.mp3')
    if path.exists(audio_file):
        logging.debug('file already exist {0}'.format(audio_file))
        return

    try:
        # down sampling to 8KHz as we are interested only in voice content.
        audio_clip = mp.AudioFileClip(video_file, fps=8000)
        audio_clip.write_audiofile(audio_file)

    except OSError as e:
        logging.error(e.strerror)


def audio_extraction_walk(root):
    files = next(walk(root), (None, None, []))[2]
    for file in files:
        if file.startswith('.'):
            continue
        video_file = path.join(confs.video_clip_path, file)
        extract_audio_from_video(video_file, confs.audio_path)
        logging.debug('extracted audio for {0}'.format(video_file))


if __name__ == '__main__':
    audio_extraction_walk(confs.video_clip_path)
