from contextlib import contextmanager
from rdflib.namespace import Namespace
from ..datasource import Informational, DataSource
from .common_data import DS_NS


class FileDataSource(DataSource):
    rdf_namespace = Namespace(DS_NS['FileDataSource#'])
    md5 = Informational(display_name='MD5 hash')
    sha256 = Informational(display_name='SHA-256 hash')
    sha512 = Informational(display_name='SHA-512 hash')

    @contextmanager
    def file_contents(self):
        raise NotImplementedError()

    def update_hash(self, algorithm):
        import hashlib
        hsh = hashlib.new(algorithm)
        with self.file_contents() as f:
            hsh.update(f.read())
        getattr(self, algorithm).set(hsh.hexdigest())


class DirectoryDataSource(DataSource):
    rdf_namespace = Namespace(DS_NS['DirectoryDataSource#'])
    md5 = Informational(display_name='MD5 hashes',
                        description='A table of MD5 hashes for every file')
    sha256 = Informational(display_name='SHA-256 hashes',
                           description='A table of SHA-256 hashes for every file')
    sha512 = Informational(display_name='SHA-512 hashes',
                           description='A table of SHA-512 hashes for every file')


__yarom_mapped_classes__ = (FileDataSource, DirectoryDataSource,)
