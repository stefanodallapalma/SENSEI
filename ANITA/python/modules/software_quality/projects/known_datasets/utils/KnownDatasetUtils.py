from utils.FileUtils import getdirs

known_datasets_path = "../resources/known_datasets/"


def get_dataset_names():
    return getdirs(known_datasets_path)