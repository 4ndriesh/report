# -*- coding: utf-8 -*-
import pandas as pd

class MergeXlsx:
    def merge_report(self,dataFrameTamp,xlsx,path_exist_report,Name_TS,Kod_PU,Name_TU):
        for key in dataFrameTamp:
            if key=="№5":
                exist_report = xlsx.open_sheet(path=path_exist_report, skiprows=5)
                exist_report.get(key).rename(columns={exist_report.get(key).columns[2]: Name_TS}, inplace=True)
                dataFrameTamp.update({key: dataFrameTamp.get(key).merge(exist_report.get(key).iloc[:, 2:-1], how='left', on=Name_TS).drop_duplicates()})
            else:
                exist_report = xlsx.open_sheet(path=path_exist_report, skiprows=6)
                exist_report.get(key).rename(columns={exist_report.get(key).columns[1]: Name_TU,exist_report.get(key).columns[-1]: Kod_PU}, inplace=True)
                dataFrameTamp.update({key:dataFrameTamp.get(key).merge(exist_report.get(key).fillna('').astype(str).iloc[:,1:], how='left', on=[Name_TU,Kod_PU])})
        return dataFrameTamp

    def check_dat(self):
        pass
    def check_csv(self):
        pass