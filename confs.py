import os
import logging

base_loc = os.path.dirname(__file__)
data_loc = os.path.join(base_loc, '../data')

multimedia_db = './db/media.db'
sas_link_file = './sas/'


video_path = os.path.join(data_loc, 'video')
video_clip_path = os.path.join(data_loc, 'clip')
audio_path = os.path.join(data_loc, 'audio')
transcripts_path = os.path.join(data_loc, 'transcripts')

# Azure blob containers used for uploading blobs and sas link generation
STORAGE_ACCOUNT_NAME = 'mediabucket' # name of the azure storage account
AUDIO_CONTAINER = 'audios'  # name of the azure storage container
TRANSCRIPTIONS_CONTAINER = 'transcriptions' # name of the container where the transcriptions will be put
MEDIA_ACCESS_KEY = os.getenv('AZURE_MEDIA_ACCESS_KEY')
MEDIA_CONNECTION_STRING = os.getenv('AZURE_MEDIA_ACCOUNT_CONNECTION_STRING')

# used in transcribe
ACCOUNT_API_KEY = os.getenv('PRIME_ACC_API_KEY')
SERVICE_REGION = "centralindia" # azure region

LOGGING_LEVEL = logging.DEBUG

