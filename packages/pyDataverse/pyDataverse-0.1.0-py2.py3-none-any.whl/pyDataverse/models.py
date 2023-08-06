from __future__ import absolute_import
from pyDataverse.api import DatafileApiData
from pyDataverse.api import DatasetApiData
from pyDataverse.api import DataverseApiData
from pyDataverse.utils import json_to_dict
from pyDataverse.utils import read_file


"""
Use Dataverse API Data models locally to prepare for further API useage.
Convert from different souurces and formats into one standardized data model
to make further processing easier. The data model is made for processing local
data, coming maybe from a Dataverse API, an ingest directory or another input.
"""


class DataverseBaseModel(object):
    """Base class for the dataverse models."""
    def import_from_json_file(self, filename):
        # TODO: add validate function
        """Imports api data from a json file.

        Parameters
        ----------
        filename : string
            Filename of json file.

        Returns
        -------
        dict
            api_data dict().

        """
        json_str = read_file(filename)
        api_data = json_to_dict(json_str)
        return api_data


class Dataverse(DataverseBaseModel):
    def __init__(self, dataverse_api_data):
        """Short summary.

        Parameters
        ----------
        dataverse_api_data : DataverseApiData()
            Description of parameter `dataverse_api_data`.

        Returns
        -------
        type
            Description of returned object.

        """
        # TODO: get version from api_data
        # set default values
        self.datasets = None
        self.version = None
        self.dataverse = None
        # set passed values
        self.api_data = dataverse_api_data

    def __str__(self):
        return 'pyDataverse Dataverse() model class.'

class Dataset(DataverseBaseModel):
    """

    One Dataset instance.

    For each version one instance necessary!
    """
    def __init__(self, dataset_api_data, data_type='dataset_class'):
        """Short summary.

        Parameters
        ----------
        dataset_api_data : DatasetApiData
            Description of parameter `dataset_api_data`.

        Returns
        -------
        type
            Description of returned object.

        """
        # set default values
        self.datafiles = None
        self.dataverse = None
        # set passed values
        self.api_data = dataset_api_data
        # set derived values
        self.version = self.api_data.version

    def __str__(self):
        return 'pyDataverse Dataset() model class.'


class Datafile(DataverseBaseModel):
    def __init__(self, datafile_api_data, dataset=None, file=None):
        """Short summary.

        Parameters
        ----------
        datafile_api_data : DatafileApiData()
            Description of parameter `datafile_api_data`.
        dataset : string
            Description of parameter `dataset`.
        file : dict()
            Description of parameter `file`.

        Returns
        -------
        type
            Description of returned object.

        """
        # TODO # {'file_location': 'STRING', 'file_location_type': 'URI oder FILEPATH'}
        # set default values
        self.dataset = None
        self.file = None
        # set passed values
        self.api_data = datafile_api_data
        # set derived values
        self.version = self.api_data.version

    def __str__(self):
        return 'pyDataverse Datafile() model class.'
