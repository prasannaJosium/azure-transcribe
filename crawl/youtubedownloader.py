from pytube import YouTube as YT
import confs
from os import path
import logging, sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")


def download(url, filepath, file_name):
    # making sure to add mp4 file extension
    file_name = file_name + '.mp4'
    # Donot download existing files.
    if path.exists((path.join(filepath, file_name))):
        logging.debug('file already exist {0}'.format(file_name))
        return

    try:
        yt = YT(url)
        yt.streams.filter(progressive=True, file_extension='mp4') \
            .order_by('resolution') \
            .desc() \
            .first() \
            .download(output_path=filepath, filename=file_name)
    except Exception as e:
        logging.error(e)
        pass


def parse_source(listOfVideos):
    links = []
    with open(listOfVideos, 'r') as source:
        for line in source:
            metadata = line.split('~')
            links.append(metadata)
    return links


def youtube_download():

    # read from the source list
    links = parse_source('listOfVideos.csv')
    # download them one my one.
    try:
        for link, filename in links:
            filename = ''.join(e for e in filename if e.isalnum())
            download(link, confs.video_path, filename)
            logging.debug('downloaded {0}'.format(filename))
    except:
        pass


if __name__ == '__main__':
    youtube_download()
