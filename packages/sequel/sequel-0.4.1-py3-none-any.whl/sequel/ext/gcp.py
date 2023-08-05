from urllib.parse import urlparse

from google.cloud.storage.client import Client
from google.cloud.exceptions import Conflict, NotFound

from sequel.io import Storage


def get_blob(url):
    parsed = urlparse(url)
    bucket_name = parsed.netloc
    path = parsed.path

    bucket = Client().bucket(bucket_name)

    try:
        bucket.create()
    except Conflict:
        pass

    return bucket.blob(path)


class GoogleCloudStorage(Storage):
    def write(self, text):
        blob = get_blob(self.url)
        blob.upload_from_string(text, content_type='application/json')

    def read(self):
        blob = get_blob(self.url)
        try:
            as_string = blob.download_as_string()
        except NotFound:
            as_string = ""
        return as_string
