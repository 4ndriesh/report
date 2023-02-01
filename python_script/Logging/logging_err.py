# -*- coding: utf-8 -*-
import os

# import logging
import logging.config
import yaml
from pathlib import Path
from .singleton import singleton


@singleton
class Logger:
    def __init__(self):
        try:
            with open((Path(__file__).parents[0]/'config.yaml'), 'r') as f:
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
