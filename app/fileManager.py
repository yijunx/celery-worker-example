# -------------------------------------------------------------------------------------------------------------
# Copyright (c) UCARE.AI Pte Ltd. All rights reserved.
#
# Author: XYJ (yijun@ucare.io)
# Created Date: Friday, June 18th 2021, 7:00:26 am
# -------------------------------------------------------------------------------------------------------------

from typing import List, Tuple, Union, Dict
from os import path
import os
from abc import ABC, abstractmethod
from config.app_config import conf
from werkzeug.datastructures import FileStorage
import csv
import logging

logger = logging.getLogger(__name__)



# METADATA_FILE_NAME = "metadata.json"
# MODEL_FILE_NAME = "model.pkl"
# REQUIREMENTS_FILE_NAME = "requirements.txt"

CHUNK_SIZE = 1024 * 512  # 512 kb


class MetaFileManager(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def upload_file(self, file: FileStorage, key: str) -> Tuple[int, int]:
        pass

    @abstractmethod
    def download_file(self, key: str) -> bytes:
        pass

    @abstractmethod
    def delete_file(self, key: str) -> None:
        pass

    # @abstractmethod
    # def read_file(self, key: str, page: int, size: int) -> List[dict]:
    #     pass


class PersistentVolumnFileManager(MetaFileManager):
    def __init__(self) -> None:
        # create folder if not there
        os.makedirs(conf.INPUT_DATA_STORAGE_FOLDER, exist_ok=True)
        os.makedirs(conf.OUTPUT_DATA_STORAGE_FOLDER, exist_ok=True)
        print("folder created!")

    def upload_file(self, file: FileStorage, key: str, name: str) -> Tuple[int, int]:
        path = os.path.join(conf.INPUT_DATA_STORAGE_FOLDER, key)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file.save(path)
        if name.endswith(".csv"):
            with open(path) as f:
                file_rows = sum(1 for _ in f) - 1
        else:
            file_rows = None
        file_size = os.stat(path).st_size
        return file_size, file_rows

    def delete_file(self, key: str) -> None:
        path = os.path.join(conf.INPUT_DATA_STORAGE_FOLDER, key)
        try:
            os.remove(path)
        except OSError:
            logger.warning(f"File {key} has been deleted already!")

    # def read_file(self, key: str, page: int, size: int) -> List[dict]:

    #     limit = size
    #     offset = (page - 1) * limit

    #     path = os.path.join(configurations.DATA_STORAGE_FOLDER, key)
    #     field_names = []
    #     try:
    #         with open(path, "r", encoding="utf-8-sig") as csv_file:
    #             csv_reader = csv.reader(csv_file, delimiter=",")
    #             for row in csv_reader:
    #                 field_names = row
    #                 break
    #     except IOError:
    #         raise FileIsNotFoundInStorage(key=key)

    #     n = 0
    #     result = []
    #     scanned_rows = 0
    #     with open(path, newline="") as csv_file:
    #         for _ in range(offset + 1):
    #             try:
    #                 next(csv_file)
    #                 scanned_rows += 1
    #             except StopIteration:
    #                 raise FileHasNotMoreContent(offset=scanned_rows)
    #         for row in csv.DictReader(csv_file, fieldnames=field_names):
    #             if n == limit:
    #                 break
    #             result.append(row)
    #             n += 1

    #     return result

    def download_file(self, key: str) -> bytes:
        path = os.path.join(conf.OUTPUT_DATA_STORAGE_FOLDER, key)
        try:
            with open(path, "rb") as fd:
                while 1:
                    buf = fd.read(CHUNK_SIZE)
                    if buf:
                        yield buf
                    else:
                        break
        except IOError:
            raise Exception(f"io error in download file...")
