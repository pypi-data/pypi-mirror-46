import logging
from pathlib import Path


class ModeRageClient():

    def __init__(self, name, cache_location, mr_service):
        self._logger = logging.getLogger(name)
        self._mr_service = mr_service
        self._cache_location = cache_location

    def _get_meta_category_cache_location(self, meta_category):
        return self._cache_location.joinpath(meta_category)

    def _get_experiment_cache_location(self, id, meta_category):
        return self._get_meta_category_cache_location(meta_category).joinpath(id)

    def save(self, meta_category, meta, parents=None, files=None):
        raise NotImplementedError()

    def load(self, id, meta_category, ignore_files=False):
        raise NotImplementedError()

    def add_parents(self, id, meta_category, parents):
        raise NotImplementedError()

    def add_files(self, id, meta_category, files):
        raise NotImplementedError()

    def _process_filenames(self, file):
        """
        Helper function for calculating what the uploaded filename should be, based on what the user has supplied
        as the 'files' upload of the save request
        """

        if 'file' in file:
            assert 'filename' in file, \
                'If \'file\' is specified, then an uploaded filename \'filename\' must be specified'

            uploaded_filename = file['filename']
            local_filename = file['file']
        else:
            local_filename = file['filename']
            uploaded_filename = Path(local_filename).name

        return local_filename, uploaded_filename
