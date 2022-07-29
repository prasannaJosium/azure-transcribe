from os import walk, path, getenv
import confs
from azure.storage.blob import BlobServiceClient
import logging, sys
import blobmanager as bm

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")


def upload_to_blob_store(local_path, container, connection_string):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    for filename, full_path in bm.folder_walker(local_path):
        bm.uploadBlob(blob_service_client, container, filename, full_path)

    bm.list_container_content(blob_service_client)


if __name__ == '__main__':
    upload_to_blob_store(confs.audio_path, confs.AUDIO_CONTAINER, confs.MEDIA_CONNECTION_STRING)
