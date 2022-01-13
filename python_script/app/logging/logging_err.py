# -*- coding: utf-8 -*-
import os

import logging
import logging.config
import yaml

from singleton import singleton
from basesetting import BaseSettings

@singleton
class Logger:
    # __instance = None

    # @staticmethod
    # def inst():
    #     if Logger.__instance == None:
    #         Logger.__instance = Logger()
    #     return Logger.__instance

    # def __new__(cls, *args, **kwargs):
    #     if cls.__instance is None:
    #         cls.__instance=super().__new__(cls)
    #     return cls.__instance

    def __init__(self):
        self.dir = BaseSettings()
        path_yaml= os.path.join(self.dir.BASE_DIR_LOG, 'config.yaml')
        try:
            with open(path_yaml, 'r') as f:
                log_cfg = yaml.safe_load(f.read())
                logging.config.dictConfig(log_cfg)
        except Exception as e:
            self.message_error(e)

    def message_error(self, err):
        logger = logging.getLogger('err')
        # logger.setLevel(logging.INFO)
        logger.error(err)


    def message_info(self, mess):
        logger = logging.getLogger('info')

        logger.info(mess)
        return mess

    def message_debug(self, mess):
        logger = logging.getLogger('debug')
        logger.info(mess)
