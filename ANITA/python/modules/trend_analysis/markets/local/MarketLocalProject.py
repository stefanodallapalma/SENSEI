import os
import shutil
from zipfile import ZipFile

# Local imports
from utils.FileUtils import getfiles

root_path = "../resources/trend_analysis/markets/"


class MarketLocalProject:
    def __init__(self, market_name):
        self.market_name = market_name

    @property
    def market_name(self):
        return self._market_name

    @market_name.setter
    def market_name(self, value):
        self._market_name = value

    @property
    def market_path(self):
        return os.path.join(root_path, self.market_name)

    @property
    def raw_path(self):
        return os.path.join(self.market_path, "raw")

    def dump_filepath(self, timestamp):
        dumps = getfiles(self.market_path, ext_filter="zip")
        for dump in dumps:
            if timestamp in dumps:
                return os.path.join(self.market_path, dump)

        return None

    def create_market_folder(self):
        try:
            os.mkdir(self.market_path)
        except OSError:
            return False

        return True

    def create_raw_folder(self):
        try:
            os.mkdir(self.raw_path)
        except OSError:
            return False

        return True

    def delete_raw_folder(self):
        shutil.rmtree(self.raw_path)

    def delete_zipfile(self, timestamp):
        zip_name = self.market_name + "_" + str(timestamp) + ".zip"
        zip_path = os.path.join(self.market_path, zip_name)

        if os.path.exists(zip_path):
            os.remove(zip_path)

    def save_and_extract(self, zip_file, timestamp):
        zip_name = self.market_name + "_" + str(timestamp) + ".zip"
        zip_path = os.path.join(self.market_path, zip_name)

        # Save zip
        zip_file.save(zip_path)

        if not os.path.exists(self.raw_path):
            self.create_raw_folder()

        # Extract
        zip = ZipFile(zip_path, "r")
        zip.extractall(self.raw_path)
