from contextlib import contextmanager
from rdflib.namespace import Namespace
from ..datasource import Informational
from .file_ds import FileDataSource, DirectoryDataSource
from .common_data import DS_NS
from ..capability import Capable
from ..capabilities import FilePathCapability


class LocalFileDataSource(Capable, FileDataSource):
    '''
    File paths should be relative -- in general, path names on a given machine are not portable
    '''
    rdf_namespace = Namespace(DS_NS['LocalFileDataSource#'])
    file_name = Informational(display_name='File name')

    needed_capabilities = [FilePathCapability()]

    @contextmanager
    def file_contents(self):
        yield open(self.file_name.one(), 'b')

    def accept_capability_provider(self, cap, provider):
        self._base_path_provider = provider

    def basedir(self):
        return self._base_path_provider.file_path()


class LocalDirectoryDataSource(Capable, DirectoryDataSource):
    '''
    File paths should be relative -- in general, path names on a given machine are not portable
    '''
    directory_path = Informational(display_name='Directory path')

    needed_capabilities = [FilePathCapability()]

    def accept_capability_provider(self, cap, provider):
        self._base_path_provider = provider

    def basedir(self):
        return self._base_path_provider.file_path()


__yarom_mapped_classes__ = (LocalFileDataSource, LocalDirectoryDataSource)
