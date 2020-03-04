import json, shutil, os
import utils.FileUtils as FileUtils
from datetime import datetime
from os import mkdir, remove
from os.path import join, exists
from zipfile import ZipFile
from utils.ListUtils import array_split

root_path = "../resources/html_pages/"


class SonarqubeLocalProject:
    BUFFER_SIZE = 100

    def __init__(self, name):
        self._name = name
        self._project_path = join(root_path, self._name)
        self._raw_path = join(self._project_path, "raw")
        self._tmp_path = join(self._raw_path, "tmp")

        jsonbuffer_name = name + "_" + "buffers.json"
        self._jsonbuffer_path = join(self._project_path, jsonbuffer_name)

    @property
    def project_path(self):
        return self._project_path

    @property
    def buffer_path(self):
        return self._tmp_path

    @property
    def jsonbuffer_path(self):
        return self._jsonbuffer_path

    def create_project(self, new_project=True):
        try:
            if new_project:
                mkdir(self._project_path)
            mkdir(self._raw_path)
        except OSError:
            return False

        return True

    def save_and_extract(self, zip_file):
        now = datetime.now()
        time = now.strftime("%Y-%m-%dT%H-%M-%S")

        zip_name = self._name + "_" + time + ".zip"
        zip_path = join(self._project_path, zip_name)

        # Save zip
        zip_file.save(zip_path)

        # Extract
        zip = ZipFile(zip_path, "r")
        zip.extractall(self._raw_path)

    def add_buffer_info(self):
        # Number of files loaded
        onlyfiles = FileUtils.getfiles(self._raw_path)

        json_buffer = {}
        buffers = array_split(onlyfiles, self.BUFFER_SIZE)

        i = 1
        for buffer in buffers:
            json_buffer[i] = buffer
            i += 1

        with open(self._jsonbuffer_path, 'w') as outfile:
            json.dump(json_buffer, outfile)

    def get_buffers(self):
        if not exists(self._jsonbuffer_path):
            return None

        return FileUtils.load_json(self._jsonbuffer_path)

    def create_buffer_folder(self):
        mkdir(self._tmp_path)

    def move_buffer(self, index):
        buffers = self.get_buffers()
        pages = buffers[str(index)]

        for page in pages:
            page_path = join(self._raw_path, page)
            new_page_path = join(self._tmp_path, page)
            shutil.copy(page_path, new_page_path)

    def clear_buffer_folder(self):
        for root, dirs, files in os.walk(self._tmp_path):
            for f in files:
                os.unlink(join(root, f))
            for d in dirs:
                shutil.rmtree(join(root, d))

    def delete_buffer_folder(self):
        shutil.rmtree(self._tmp_path)

    def get_raw_files(self):
        if not exists(self._raw_path) or not exists(self._jsonbuffer_path):
            return None

        files = []
        if exists(self._jsonbuffer_path):
            buffers = self.get_buffers()
            for key in buffers:
                files += buffers[key]
        else:
            files = FileUtils.load_json(self._raw_path)

        return files

    def delete_raw(self):
        shutil.rmtree(self._raw_path)
        remove(self._jsonbuffer_path)

    def exist(self):
        if exists(self._project_path):
            return True

        return False


