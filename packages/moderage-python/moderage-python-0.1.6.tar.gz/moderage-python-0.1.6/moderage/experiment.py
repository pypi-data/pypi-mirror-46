import logging

class Experiment():
    """
    Returned when an experiment has been loaded.

    Contains helper methods.
    """

    def __init__(self, experiment, mr_service, experiment_cache_location=None):

        self._logger = logging.getLogger("Experiment")

        self._experiment_cache_location = experiment_cache_location

        self.metaCategory = experiment['metaCategory']
        self.files = experiment['files'] if 'files' in experiment else []
        self.meta = experiment['meta']
        self.parents = experiment['parents']

        self.id = experiment['id']

        self._mr = mr_service

        self._logger.info('Experiment Info:')
        for k_m, v_m in experiment['meta'].items():
            self._logger.info('%s: %s' % (k_m, str(v_m)))

    def get_file(self, filename):
        """
        Get a file handle by it's filename
        :return: a BufferedReader containing the file
        """

        if self._experiment_cache_location is None:
            return None

        file_info = self.get_file_info(filename)
        cached_filename = self._experiment_cache_location.joinpath(file_info['id'])
        return open(str(cached_filename), 'rb')

    def get_file_info(self, filename):
        """
        Get a file info by it's filename
        :param filename:
        :return:
        """

        for f in self.files:
            if f['filename'] == filename:
                return f

    def load_parents(self, ignore_files=False):
        """
        Returns a generator that will return each parent in turn
        :param ignore_files: Will not automatically download files associated with the parent
        :return:
        """

        loaded_parents = []

        for parent in self.parents:
            yield self._mr.load(parent['id'], parent['metaCategory'], ignore_files)

    def add_files(self, files):
        """
        Add files to this experiment
        :param files:
        :return:
        """
        experiment = self._mr.add_files(self.id, self.metaCategory, files)
        self.files = experiment.files

    def add_parents(self, parents):
        """
        Add parents to this experiment
        :param parents:
        :return:
        """
        experiment = self._mr.add_parents(self.id, self.metaCategory, parents)
        self.parents = experiment.parents