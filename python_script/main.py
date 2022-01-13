# -*- coding: utf-8 -*-
__author__ = 'BiziurAA'

from logging_err import Logger

import os
import re

import pandas as pd
from itertools import chain

from rw_xlsx import Xlsx
from basesetting import BaseSettings
from formating_tu_ts import TuTs

if __name__ == "__main__":
    tuts=TuTs()
    xlsx = Xlsx()
    dir = BaseSettings()
    log = Logger()
    yaml = dir.get_config()
    filePrj = os.path.join(dir.BASE_DIR, *yaml.get('file_prj'))
    sheets_prj = xlsx.open_book(path=filePrj)
    st_yaml = yaml.get('station')
    lsNameSt = list(map(lambda nameSt: '{0}{1}'.format('К_', nameSt), st_yaml))
    all = list(set(list(chain(st_yaml, lsNameSt)))&set(sheets_prj))
    dataFramePrj = xlsx.open_sheet(path=filePrj, skiprows=1, sheet_name=all)

    for st in st_yaml:
        stationTS = st
        stationTU = '{0}{1}'.format('К_', stationTS)
        stations = list(filter(lambda x: x in sheets_prj, [stationTS, stationTU]))
        dataFrameTS = dataFramePrj.get(stationTS)

        try:
            headTS = set(dataFrameTS.columns)
            SIGN = list(yaml.get('SIGN') & headTS)[0]
            Name_TS = list(yaml.get('Name_TS') & headTS)[0]
            GrImp = list(yaml.get('GrImp') & headTS)[0]
            PPTS = list(yaml.get('PPTS') & headTS)[0]
        except Exception as e:
            log.message_error(e)
            raise Exception(e)

        fileTamp = os.path.join(dir.BASE_DIR, *yaml.get('name_tampl'))
        dataFrameTamp = xlsx.open_sheet(path=fileTamp, skiprows=7)
        sheets_tampl = list(dataFrameTamp.keys())

        fileTampMeket = os.path.join(dir.BASE_DIR, *yaml.get('name_tampl_maket'))
        sheets_tampl_maket = xlsx.open_book(path=fileTampMeket)
        TS = dataFrameTS.filter(items=[PPTS, SIGN, Name_TS, GrImp]).fillna('')

        dictMaket = dict.fromkeys(sheets_tampl_maket, pd.DataFrame())

        if (stationTU in stations):
            dataFrameTU = dataFramePrj.get(stationTU)
            try:
                head = set(dataFrameTU.columns)
                PP = list(yaml.get('PP') & head)[0]
                PP2 = list(yaml.get('PP2') & head)[0]
                Name_TU = list(yaml.get('TU') & head)[0]
                Kod_PU = list(yaml.get('Kod_PU') & head)[0]
            except Exception as e:
                log.message_error(e)
                raise Exception(e)
            format=[PP2, Name_TU, Kod_PU]
            TU=dataFrameTU.filter(items=format)
            TU=tuts.tu(TU,format,dataFrameTamp,sheets_tampl)
            dictMaket.update({sheets_tampl_maket[0]: TU})

        path_temp = os.path.join(dir.BASE_DIR, *yaml.get('name_tampl_maket'))
        path_temp_mak = os.path.join(dir.BASE_DIR_REPORT, '{0}{1}{2}'.format('Ведомость ', stationTS, '  макет.xlsx'))
        xlsx.copy_xlsx(path_temp, path_temp_mak)

        path_temp = os.path.join(dir.BASE_DIR, *yaml.get('name_tampl'))
        path_temp_rep = os.path.join(dir.BASE_DIR_REPORT, '{0}{1}{2}'.format('Ведомость ', stationTS, '.xlsx'))
        xlsx.copy_xlsx(path_temp, path_temp_rep)

        path_csv = os.path.join(dir.BASE_DIR_REPORT, '{0}{1}'.format(stationTS.upper(), '.txt'))
        if (os.path.exists(path_csv)):
            TS_Arm = xlsx.read_csv(path_csv)
            TS = pd.concat([TS, TS_Arm.iloc[:, [1, 2]]], axis=1)

        TS=tuts.ts(TS,SIGN)

        dataFrameTamp.update({sheets_tampl[0]: TS.filter(items=[PPTS, SIGN, Name_TS, GrImp])})
        xlsx.write_to_excel(dataFrameTamp, 7, 0, path_temp_rep, stationTS)

        dictMaket.update({sheets_tampl_maket[1]:TS})
        xlsx.write_to_excel(dictMaket, 6, 0, path_temp_mak, stationTS)

        log.message_debug(stationTS)

    # qml()
