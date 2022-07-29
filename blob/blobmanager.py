from os import walk, path, getenv
import confs
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import logging, sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")


def uploadBlob(blob_srv_client, container, filename, full_path):
    try:

        blob_client = blob_srv_client.get_blob_client(container=container, blob=filename)
        # Upload the created file
        with open(full_path, "rb") as data:
            blob_client.upload_blob(data)
            logging.debug('uploaded file {0}'.format(full_path))
    except Exception as ex:
        logging.debug(ex)


def list_container_content(blob_srv_client):
    # List the blobs in the container
    # Create the container
    container_client = blob_srv_client.get_container_client(container=confs.AUDIO_CONTAINER)
    blob_list = container_client.list_blobs()
    for blob in blob_list:
       logging.debug('Blob : {0}'.format(blob.name))


def folder_walker(root):
    files = next(walk(root), (None, None, []))[2]
    filesToSend = []
    for file in files:
        if file.startswith('.'):  # do not add hidden files to list
            continue
        filesToSend.append((file, path.join(root, file)))
    return filesToSend


def upload_audio_to_blob():
    blob_service_client = BlobServiceClient.from_connection_string(confs.MEDIA_CONNECTION_STRING)
    for file, file_path in folder_walker(confs.audio_path):
        uploadBlob(blob_service_client, confs.AUDIO_CONTAINER, file, file_path)
    list_container_content(blob_service_client)


if __name__ == '__main__':

    upload_audio_to_blob()
