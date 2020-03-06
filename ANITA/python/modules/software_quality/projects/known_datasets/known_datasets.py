import os
import pandas as pd

from utils.FileUtils import getdirs, getfiles
from exception.NoDatasetFoundException import NoDatasetFoundException
from modules.software_quality.projects.known_datasets import DUTA

known_datasets_path = "..resources/known_datasets/"


def get_dataset_names():
    datasets = getdirs(known_datasets_path)
    return datasets


def get_stored_dataset_name(dataset_name):
    datasets = get_dataset_names()
    for i in range(len(datasets)):
        if dataset_name.lower == datasets[i]:
            return datasets[i]

    return None


def load_csv(dataset_name, delimiter):
    datasets = get_dataset_names()
    low_case_datasets = [lc_dat.lower() for lc_dat in datasets]

    if dataset_name.lower() not in low_case_datasets:
        raise NoDatasetFoundException()

    index = low_case_datasets.index(dataset_name.lower)
    dataset_path = os.path.join(known_datasets_path, datasets[index])

    files = getfiles(dataset_path)
    for file in files:
        if file.endswith(".csv"):
            return pd.read_csv(os.path.join(dataset_path, file), delimiter=delimiter)

    raise FileNotFoundError()


def generate_extra_informations(dataset_name, files_path):
    """Generate extra information, if a dataset passed as input is one of the case stored in the system"""
    name = get_stored_dataset_name(dataset_name)
    if name is None:
        raise NoDatasetFoundException()

    if name.lower() == "duta":
        json_info = DUTA.get_extra_informations(files_path)
        print(str(json_info))