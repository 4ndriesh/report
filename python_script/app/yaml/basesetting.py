# -*- coding: utf-8 -*-
import os
import sys

import pandas as pd
import yaml

from singleton import singleton


@singleton
class BaseSettings:
    def __init__(self):
        self.BASE_DIR = os.getcwd()
        # if getattr(sys, 'frozen', False):
        #     # If the application is run as a bundle, the pyInstaller bootloader
        #     # extends the sys module by a flag frozen=True and sets the app
        #     # path into variable _MEIPASS'.
        #     self.BASE_DIR = os.getcwd()
        # else:
        #     self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.BASE_DIR_APP=os.path.join(self.BASE_DIR,'app')
        self.BASE_DIR_TAMP = os.path.join(self.BASE_DIR, 'temp')
        self.BASE_DIR_CONF = os.path.join(self.BASE_DIR_APP, 'yaml')
        self.BASE_DIR_LOG = os.path.join(self.BASE_DIR_APP, 'logging')
        self.BASE_DIR_REPORT = os.path.join(self.BASE_DIR, 'report')
        try:
            with open(os.path.join(self.BASE_DIR_CONF, 'setting.yaml'), 'r', encoding='utf-8') as yaml_config_file:
                self.CONFIG = yaml.safe_load(yaml_config_file)
        except Exception as e:
            self.CONFIG = {}

    # # @property
    # def get_settings(self):
    #     return self.__CONFIG
    #
    # @property
    # def base_dir(self):
    #     return self.__BASE_DIR
    #
    # @property
    # def base_dir_app(self):
    #     return self.__BASE_DIR_APP
    #
    # @property
    # def base_dir_tamp(self):
    #     return self.__BASE_DIR_TAMP
    #
    # @property
    # def base_dir_prj(self):
    #     return self.__BASE_DIR_PRJ
    #
    # @property
    # def base_dir_log(self):
    #     return self.__BASE_DIR_LOG


    def get_config(self):
        return self.CONFIG

    def in_param(self,dataFrame):
        return pd.concat(dataFrame.values()).iloc[:, 1]

    # def choose_unic_part(self, ls_param, dataFrame):
    #     # Сравниваем все варианты срезов, с вариантом который будет
    #     self.in_param = [x for x in ls_param if x in dataFrame.iloc[:, 2].tolist()]
    #     self.in_param.append(None)
    #     self.Dict_in_param = dict.fromkeys(self.in_param, pd.DataFrame())

    def format_sheet(self):
        self.choose_param = list(map(lambda x: set(self.in_param) & set(x), self.format_to_excel))







