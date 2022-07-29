from os import walk, path
from pathlib import Path
import logging
from moviepy import editor as mp
import confs
import logging, sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")


def sub_clip_video(sourcefile, clipfile, starttime='00:05:00', endtime='00:10:00'):

    if path.exists(clipfile):
        logging.debug('file already exist {0}'.format(clipfile))
        return

    clip = mp.VideoFileClip(sourcefile)
    sub_clip = clip.subclip(starttime, endtime)
    sub_clip.write_videofile(clipfile, temp_audiofile='temp-audio.m4a', remove_temp=True, codec="libx264",
                             audio_codec='aac')


def video_clips_walk():
    files = next(walk(confs.video_path), (None, None, []))[2]
    for file in files:
        if file.startswith('.'):
            continue
        video_file = path.join(confs.video_path, file)
        video_clip_file = path.join(confs.video_clip_path, 'short_' + file)
        sub_clip_video(video_file, video_clip_file)
        logging.debug('created subclip for {0} between 00:05:00  to 00:10:00 timestamps'.format(video_file))


if __name__ == '__main__':
    video_clips_walk()
