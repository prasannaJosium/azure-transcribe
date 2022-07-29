import confs
import crawl.youtubedownloader as yt
import video.video_processing as vp
import audio.audioextractor as ae
import blob.blobmanager as bm
import blob.blob_sas_manager as bsm
import transcribe.transcribe as ts


import logging, sys

logging.basicConfig(stream=sys.stdout, level=confs.LOGGING_LEVEL,
                    format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")

if __name__ == '__main__':
    steps = 0
    done = False
    while not done:
        if steps == 0:
            logging.info("Downloading videos ...")
            yt.youtube_download()
            logging.info("Downloading completed")
        if steps == 1:
            logging.info("Extracting video clips ...")
            vp.video_clips_walk()
            logging.info("Completed extracting video clips")
        if steps == 2:
            logging.info("Extracting audio tracks ...")
            ae.audio_extraction_walk(confs.video_clip_path)
            logging.info("Audio extraction completed")
        if steps == 3:
            logging.info("Uploading audio files to blob store ...")
            bm.upload_audio_to_blob()
            logging.info(" uploading audio files completed")
        if steps == 4:
            logging.info("Generating SAS access urls to audio files ...")
            bsm.create_sas_urls()
            logging.info("SAS link generation completed")
        if steps == 5:
            logging.info('Starting transcription ...')
            ts.transcribe_audio()
            logging.info('Transcription completed')

        steps += 1
