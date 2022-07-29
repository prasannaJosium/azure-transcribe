from os import walk, path, getenv
import confs

import os
import logging, sys
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
import confs

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")
account_name = 'STORAGE_ACCOUNT_NAME'
account_key = 'STORAGE_ACCOUNT_ACCESS_KEY'
container_name = 'CONTAINER_NAME'
blob_name = 'IMAGE_PATH/IMAGE_NAME'


def get_blob_sas(account_name, account_key, container_name, blob_name):
    sas_blob = generate_blob_sas(account_name=confs.STORAGE_ACCOUNT_NAME,
                                 container_name=confs.AUDIO_CONTAINER,
                                 blob_name=blob_name,
                                 account_key=confs.MEDIA_ACCESS_KEY,
                                 permission=BlobSasPermissions(read=True),
                                 expiry=datetime.utcnow() + timedelta(hours=3))

    link = 'https://' + account_name + '.blob.core.windows.net/' + container_name + '/' + blob_name + '?' + sas_blob
    return link


def get_sas_list_for_container(blob_srv_client):
    global sas_urls
    # List the blobs in the container and collect them in a list
    sas_urls = []
    # Create the container
    container_client = blob_srv_client.get_container_client(container=confs.AUDIO_CONTAINER)
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        sas_url = get_blob_sas(confs.STORAGE_ACCOUNT_NAME, confs.MEDIA_ACCESS_KEY, confs.AUDIO_CONTAINER, blob.name)
        sas_urls.append(','.join([blob.name, sas_url]))
        logging.debug('Generated sas urls for {0}'.format(blob.name))
    return sas_urls


def create_sas_urls():
    global sas_urls
    blob_service_client = BlobServiceClient.from_connection_string(confs.MEDIA_CONNECTION_STRING)
    sas_urls = get_sas_list_for_container(blob_service_client)
    print('SAS URLS')
    filename = os.path.join(confs.base_loc, 'blob', 'links.txt')
    with open(filename, 'w', ) as f:
        for url in sas_urls:
            f.write(url + os.linesep)


if __name__ == '__main__':
    create_sas_urls()
