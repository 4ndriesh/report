# -*- coding: utf-8 -*-
import os
from pathlib import Path
import yaml

from singleton import singleton
@singleton
class BaseSettings:
    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent.parent
        self.BASE_DIR_CONF = Path(self.BASE_DIR / 'out_in_data'/ 'setting.yaml')
        self.BASE_DIR_PROJECT= Path(self.BASE_DIR / 'out_in_data')
        self.BASE_DIR_LOG = Path(self.BASE_DIR / 'python_script'/'app' / 'logging' / 'config.yaml')
        self.BASE_DIR_REPORT = Path(self.BASE_DIR / 'out_in_data' /'report')
        self.BASE_DIR_EXREPORT = Path(self.BASE_DIR / 'out_in_data' /'exreport')
        self.BASE_DIR_CSV = Path(self.BASE_DIR/'out_in_data' / 'csv')
        self.BASE_DIR_DAT = Path(self.BASE_DIR/'out_in_data' / 'dat')
        self.BASE_DIR_DAT_MAKET = Path(self.BASE_DIR /'out_in_data' /'dat_maket')
        self.BASE_DIR_TAMPL_MAKET = Path(self.BASE_DIR /'out_in_data' / 'temp' / 'Tamplate_maket.xlsx')
        self.BASE_DIR_TAMPL = Path(self.BASE_DIR /'out_in_data' / 'temp' / 'Tamplate.xlsx')
        self.BASE_DIR_TAMPL_CSV = Path(self.BASE_DIR /'out_in_data' / 'temp' / 'Tamplate_csv.xlsx')
        try:
            with open(self.BASE_DIR_CONF, 'r', encoding='utf-8') as yaml_config_file:
                self.CONFIG = yaml.safe_load(yaml_config_file)
        except Exception as e:
            self.CONFIG = {}

    def get_config(self):
        return self.CONFIG

class FormatTS:
    def __init__(self,dataFrameTS,dataFrameTU,yaml):
        headTS = set(dataFrameTS.columns)
        self.SIGN = list(yaml.get('SIGN') & headTS)[0]
        self.Name_TS = list(yaml.get('Name_TS') & headTS)[0]
        self.GrImp = list(yaml.get('GrImp') & headTS)[0]
        self.PPTS = list(yaml.get('PPTS') & headTS)[0]
        self.formatTS = [self.PPTS, self.SIGN, self.Name_TS, self.GrImp]
        head = set(dataFrameTU.columns)
        self.PP2 = list(yaml.get('PP2') & head)[0]
        self.Name_TU = list(yaml.get('TU') & head)[0]
        self.Kod_PU = list(yaml.get('Kod_PU') & head)[0]
        self.formatTU=[self.PP2, self.Name_TU, self.Kod_PU]
