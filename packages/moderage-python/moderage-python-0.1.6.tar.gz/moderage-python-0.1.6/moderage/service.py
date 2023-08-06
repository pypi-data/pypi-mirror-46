import yaml
import magic
from pathlib import Path
import logging

from moderage.clients import LocalClient, ServerClient
from moderage.experiment import Experiment


class ModeRage():

    def __init__(self, config_file=None):

        self._server_config_defaults = {
            'host': 'localhost',
            'port': '8118',
        }

        self._local_config_defaults = {

        }

        self._logger = logging.getLogger("Mode Rage client")

        self._logger.info('Attempting to load Mode Rage config from  ./.mrconfig')

        mode, config = self._load_config(config_file)

        self.mode = mode

        cache_location = config['cache_location']
        if not cache_location.exists():
            cache_location.mkdir()

        self._logger.debug('Cache location: [%s]' % str(cache_location))

        if mode == 'server':
            self._host = config['host']
            self._port = config['port']
            self._root_url = '%s:%s/v0/experiment' % (self._host, self._port)
            self._client = ServerClient(self._root_url, cache_location, self)

        # Will save and load from local cache and use tinydb for file lookup
        if mode == 'local':
            self._client = LocalClient(cache_location, self)

    def _load_config(self, config_location=None):
        """
        Looks for .mrconfig in local directory and loads settings if present
        """

        local_defaults = {
            'cache_location': Path.home().joinpath('.moderage')
        }

        # Use default config location if none is available
        if not config_location:
            config_location = './.mrconfig'

        try:
            with open(config_location, 'r') as config_file:
                config = yaml.safe_load(config_file)

                mode = config['mode']

                cache_location = Path(config['cache_location'] if 'cache_location' in config \
                    else local_defaults['cache_location'])

                # expand any tilde '~' characters to full directory
                cache_location = cache_location.expanduser()

                if mode == 'server':
                    server_config = config['server'] if 'server' in config else self._server_config_defaults
                    return 'server', {**server_config, 'cache_location': cache_location}
                elif mode == 'local':
                    local_config = config['local'] if 'local' in config else self._local_config_defaults
                    return 'local', {**local_config, 'cache_location': cache_location}

        except IOError as e:
            self._logger.info('Cannot load .mrconfig file. Using defaults.', e)

        return 'local', local_defaults


    def save(self, meta_category, meta, parents=None, files=None):
        """
        :param parents: list of objects containing the id and category of experiments that this experiment relies on

        for example:

        {
            "id": "05c0581c-7ece-4cad-a26f-0e415ea1b01d",
            "metaCategory": "grid_world"
        }

        :param meta_category: A category name for this experiment, or this dataset
        :param meta: meta information for this experiment or dataset
        :param files: A list of files and metadata associated with this experiment or dataset

        Files must be in the following format:

        [
            "filename": "./path/to/my/file.xyz",
            "caption": "This is a description of my file"
        ]

        :return:
        """

        self._logger.info('Saving data to category %s' % meta_category)

        if files is not None:
            files = [self._process_file_info(file) for file in files]

        return self._client.save(meta_category, meta, parents=parents, files=files)

    def add_parents(self, id, meta_category, parents):
        """

        :param id:
        :param meta_category:
        :param parents:
        :return:
        """

        self._logger.info('Adding parents to data experiment %s in category %s' % (id, meta_category))

        return self._client.add_parents(id, meta_category, parents)


    def add_files(self, id, meta_category, files):
        """

        :param id:
        :param meta_category:
        :param files:
        :return:
        """

        self._logger.info('Adding files to data experiment %s in category %s' % (id, meta_category))

        if files is not None:
            files = [self._process_file_info(file) for file in files]

        return self._client.add_files(id, meta_category, files)

    def load(self, id, meta_category, ignore_files=False):
        """
        Load an experiment
        :param id: the id of the experiment
        :param meta_category: the category of the experiment
        :param ignore_files: If this is set to true, the files will not be downloaded and cached
        """

        self._logger.info('Loading data with id [%s] in category [%s]' % (id, meta_category))

        return self._client.load(id, meta_category, ignore_files)

    def _process_file_info(self, file):
        """
        Get the mime type of the file
        :param file:
        :return:
        """

        local_filename = file['file'] if 'file' in file else file['filename']

        file['contentType'] = magic.from_file(local_filename, True)

        return file
