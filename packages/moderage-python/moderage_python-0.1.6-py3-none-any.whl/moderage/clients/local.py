from pathlib import Path

from moderage.clients.client import ModeRageClient
import uuid
import shutil
from tinydb import Query, TinyDB

from moderage.experiment import Experiment


class LocalClient(ModeRageClient):

    def __init__(self, cache_location, mr_service):
        super().__init__("Local Client", cache_location, mr_service)



    def save(self, meta_category, meta, files=None, parents=None):
        """
        Save using local tinydb and local cache only
        """

        meta_category_location = self._get_meta_category_cache_location(meta_category)

        if not meta_category_location.exists():
            meta_category_location.mkdir()

        db_location = meta_category_location.joinpath('db.json')
        db = TinyDB(str(db_location))

        id = str(uuid.uuid4())

        cache_location = meta_category_location.joinpath(id)
        if not cache_location.exists():
            cache_location.mkdir()

        # Move all the files into the cache
        file_info_list = self._save_files(cache_location, files)

        entry = {
            'metaCategory': meta_category,
            'id': id,
            'parents': parents,
            'meta': meta,
            'files': file_info_list
        }

        db.insert(entry)

        experiment_cache_location = self._get_experiment_cache_location(id, meta_category)

        return Experiment(entry, self._mr_service, experiment_cache_location)

    def _save_files(self, cache_location, files):
        file_info_list = []
        if files is not None:
            for file in files:
                file_info = {}
                file_info['id'] = str(uuid.uuid4())
                file_info['caption'] = file['caption']
                file_info['success'] = True
                file_info['contentType'] = file['contentType']

                # Save the filename and strip the directory information
                local_filename, uploaded_filename = self._process_filenames(file)
                file_info['filename'] = uploaded_filename

                # Save the location of the file in the filesystem
                location = str(cache_location.joinpath(file_info['id']))
                shutil.copy(local_filename, location)
                file_info['location'] = location
                file_info_list.append(file_info)
        return file_info_list

    def load(self, id, meta_category, ignore_files=False):
        """
        Load using local tinydb and local cache only
        """

        meta_category_location = self._get_meta_category_cache_location(meta_category)

        db_location = meta_category_location.joinpath('db.json')
        db = TinyDB(str(db_location))

        ExperimentQuery = Query()
        search_result = db.search(ExperimentQuery.id == id)
        assert len(search_result) == 1

        experiment = search_result[0]

        experiment_cache_location = self._get_experiment_cache_location(id, meta_category)

        return Experiment(experiment, self._mr_service, experiment_cache_location)

    def add_parents(self, id, meta_category, parents):
        """
        Add parents to an existing experiment
        :return: returns the experiment after the parents are added
        """

        meta_category_location = self._get_meta_category_cache_location(meta_category)

        db_location = meta_category_location.joinpath('db.json')
        db = TinyDB(str(db_location))

        # Get the current parents
        ExperimentQuery = Query()
        search_result = db.search(ExperimentQuery.id == id)
        assert len(search_result) == 1

        # Add the new parents to the old parents in the experiment
        experiment = search_result[0]
        new_parents = experiment['parents'] + parents

        # Update the DB
        db.update({'parents': new_parents}, ExperimentQuery.id == id)

        # Get the db entry after the update
        search_result = db.search(ExperimentQuery.id == id)
        assert len(search_result) == 1

        experiment_cache_location = self._get_experiment_cache_location(id, meta_category)
        return Experiment(search_result[0], self._mr_service, experiment_cache_location)


    def add_files(self, id, meta_category, files):
        """

        :param id:
        :param meta_category:
        :param files:
        :return:
        """

        meta_category_location = self._cache_location.joinpath(meta_category)

        db_location = meta_category_location.joinpath('db.json')
        db = TinyDB(str(db_location))

        # Get the current parents
        ExperimentQuery = Query()
        search_result = db.search(ExperimentQuery.id == id)
        assert len(search_result) == 1

        # Save the files to the cache
        file_info_list = self._save_files(meta_category_location, files)

        # Add the new files to the old files in the experiment
        experiment = search_result[0]
        new_files = experiment['files'] + file_info_list

        # Update the DB
        db.update({'files': new_files}, ExperimentQuery.id == id)

        # Get the db entry after the update
        search_result = db.search(ExperimentQuery.id == id)
        assert len(search_result) == 1

        experiment_cache_location = meta_category_location.joinpath(id)
        return Experiment(search_result[0], self._mr_service, experiment_cache_location=experiment_cache_location)