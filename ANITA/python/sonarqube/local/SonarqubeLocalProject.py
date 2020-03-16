import json, shutil, os
import utils.FileUtils as FileUtils
from os import mkdir, remove
from os.path import join, exists
from zipfile import ZipFile
from utils.ListUtils import array_split

root_path = "../resources/software_quality/"


class SonarqubeLocalProject:
    BUFFER_SIZE = 100

    def __init__(self, name):
        self._name = name

    @staticmethod
    def root_path():
        return root_path

    @property
    def project_path(self):
        return join(root_path, self._name)

    @property
    def buffer_path(self):
        return join(self.raw_path, "tmp")

    @property
    def jsonbuffer_path(self):
        jsonbuffer_name = self._name + "_" + "buffers.json"
        return join(self.project_path, jsonbuffer_name)

    @property
    def raw_path(self):
        return join(self.project_path, "raw")

    def create_project(self, new_project=True):
        try:
            if new_project:
                mkdir(self.project_path)
            mkdir(self.raw_path)
        except OSError:
            return False

        return True

    def delete_project(self):
        shutil.rmtree(self.project_path)

    def projectdir_is_empty(self):
        dirs = FileUtils.getdirs(self.project_path)
        files = FileUtils.getfiles(self.project_path)

        if len(dirs) + len(files) == 0:
            return True

        return False

    def save_and_extract(self, zip_file, timestamp):
        zip_name = self._name + "_" + timestamp + ".zip"
        zip_path = join(self.project_path, zip_name)

        # Save zip
        zip_file.save(zip_path)

        # Extract
        zip = ZipFile(zip_path, "r")
        zip.extractall(self.raw_path)

    def get_dumps(self):
        dumps = FileUtils.getfiles(self.project_path, ext_filter="zip")
        return [".".join(dump.split(".")[:-1]) for dump in dumps]

    def delete_dump(self, timestamp):
        dump_name = self._name + "_" + timestamp + ".zip"
        print(dump_name)
        dump_path = join(self.project_path, dump_name)
        print(dump_path)
        os.remove(dump_path)

    def last_timestamp(self):
        dump_list = FileUtils.getfiles(self.project_path, ext_filter="zip")

        last = 0
        for dump in dump_list:
            timestamp = dump.split("_")[1]
            if timestamp > last:
                last = timestamp

        return last

    def add_buffer_info(self):
        # Number of files loaded
        onlyfiles = FileUtils.getfiles(self.raw_path)

        json_buffer = {}
        buffers = array_split(onlyfiles, self.BUFFER_SIZE)

        i = 1
        for buffer in buffers:
            json_buffer[i] = buffer
            i += 1

        with open(self.jsonbuffer_path, 'w') as outfile:
            json.dump(json_buffer, outfile)

    def get_buffers(self):
        if not exists(self.jsonbuffer_path):
            return None

        return FileUtils.load_json(self.jsonbuffer_path)

    def create_buffer_folder(self):
        mkdir(self.buffer_path)

    def move_buffer(self, index):
        buffers = self.get_buffers()
        pages = buffers[str(index)]

        for page in pages:
            page_path = join(self.raw_path, page)
            new_page_path = join(self.buffer_path, page)
            shutil.copy(page_path, new_page_path)

    def clear_buffer_folder(self):
        for root, dirs, files in os.walk(self.buffer_path):
            for f in files:
                os.unlink(join(root, f))
            for d in dirs:
                shutil.rmtree(join(root, d))

    def delete_buffer_folder(self):
        shutil.rmtree(self.buffer_path)

    def get_raw_files(self):
        if not exists(self.raw_path) or not exists(self.jsonbuffer_path):
            return None

        files = []
        if exists(self.jsonbuffer_path):
            buffers = self.get_buffers()
            for key in buffers:
                files += buffers[key]
        else:
            files = FileUtils.load_json(self.raw_path)

        return files

    def delete_raw(self):
        shutil.rmtree(self.raw_path)
        remove(self.jsonbuffer_path)

    def exist(self):
        if exists(self.project_path):
            return True

        return False


