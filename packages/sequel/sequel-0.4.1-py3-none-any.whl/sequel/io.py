from urllib.parse import urlparse


class StorageFactory(object):
    def __init__(self):
        self._url_schemes_to_storage = {}
        self.register(None, NullStorage)
        self.register('', FileSystemStorage)

    def load_plugins(self, entry_point_group):
        import pkg_resources
        for entrypoint in pkg_resources.iter_entry_points(entry_point_group):
            try:
                self.register(entrypoint.name, entrypoint.load())
            except ImportError:
                pass

    def register(self, scheme, storage_class):
        self._url_schemes_to_storage[scheme] = storage_class

    def make_storage(self, url):
        if not isinstance(url, str):
            return self._url_schemes_to_storage[url](url)

        scheme = urlparse(url).scheme

        return self._url_schemes_to_storage[scheme](url)


class Storage(object):
    def __init__(self, url):
        self.url = url

    def write(self, text):
        raise NotImplementedError

    def read(self):
        raise NotImplementedError


class NullStorage(Storage):
    def write(self, text):
        print(text)

    def read(self):
        return ''


class FileSystemStorage(Storage):
    def write(self, text):
        parsed = urlparse(self.url)

        with open(parsed.path, mode='w') as opened:
            opened.write(text)

    def read(self):
        parsed = urlparse(self.url)

        try:
            with open(parsed.path) as opened:
                text = opened.read()
        except FileNotFoundError:
            text = ''

        return text
