# -*- coding: utf-8 -*-
import os

import logging
import logging.config
import yaml

from singleton import singleton

@singleton
class Logger:
    def __init__(self,BASE_DIR_LOG):
        try:
            with open(BASE_DIR_LOG, 'r') as f:
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
