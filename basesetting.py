# -*- coding: utf-8 -*-
from pathlib import Path
import yaml
from python_script import *


@singleton
class BaseSettings:
    def __init__(self):
        self.BASE_DIR = Path(__file__).parents[0]
        # self.BASE_DIR = Path(__file__).resolve(strict=True).parent[0]
        self.BASE_DIR_CONF = self.BASE_DIR / 'out_in_data'/ 'setting.yaml'
        self.BASE_DIR_PROJECT= self.BASE_DIR / 'out_in_data'

        self.NAME_FILE_REPORT_MAKET='Ведомость {0} макет.xlsm'
        self.BASE_DIR_REPORT_MAKET = self.BASE_DIR_PROJECT /'report'

        self.NAME_FILE_REPORT='Ведомость {0}.xlsm'
        self.BASE_DIR_REPORT = self.BASE_DIR_PROJECT /'report'

        self.NAME_FILE_EXREPORT='Ведомость {0}.xlsx'
        self.BASE_DIR_EXREPORT = self.BASE_DIR_PROJECT /'exreport'

        self.BASE_DIR_CSV = self.BASE_DIR_PROJECT/ 'csv'
        self.BASE_DIR_DAT = self.BASE_DIR_PROJECT/ 'dat'
        self.BASE_DIR_DAT_MAKET = self.BASE_DIR_PROJECT /'dat_maket'
        self.BASE_DIR_TAMPL_MAKET = self.BASE_DIR_PROJECT / 'temp' / 'Tamplate_maket.xlsx'
        self.BASE_DIR_TAMPL = self.BASE_DIR_PROJECT / 'temp' / 'Tamplate.xlsm'
        self.BASE_DIR_TAMPL_CSV = self.BASE_DIR_PROJECT / 'temp' / 'Tamplate_csv.xlsx'
        try:
            with open(self.BASE_DIR_CONF, 'r', encoding='utf-8') as yaml_config_file:
                self.CONFIG = yaml.safe_load(yaml_config_file)
        except Exception as e:
            self.CONFIG = {}

    def get_config(self):
        return self.CONFIG

# class FormatTS:
#     def __init__(self,dataFrameTS,dataFrameTU,yaml):
#         headTS = set(dataFrameTS.columns)
#         self.SIGN = list(yaml.get('SIGN') & headTS)[0]
#         self.Name_TS = list(yaml.get('Name_TS') & headTS)[0]
#         self.GrImp = list(yaml.get('GrImp') & headTS)[0]
#         self.PPTS = list(yaml.get('PPTS') & headTS)[0]
#         self.formatTS = [self.PPTS, self.SIGN, self.Name_TS, self.GrImp]
#         head = set(dataFrameTU.columns)
#         self.PP2 = list(yaml.get('PP2') & head)[0]
#         self.Name_TU = list(yaml.get('TU') & head)[0]
#         self.Kod_PU = list(yaml.get('Kod_PU') & head)[0]
#         self.formatTU=[self.PP2, self.Name_TU, self.Kod_PU]
