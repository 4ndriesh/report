# -*- coding: utf-8 -*-
__author__ = 'BiziurAA'

from logging_err import Logger

import os

import pandas as pd
from itertools import chain
from pathlib import Path

from rw_xlsx import Xlsx
from basesetting import BaseSettings

from merge_xlsx import MergeXlsx
import walk_dir

if __name__ == "__main__":
    xlsx = Xlsx()
    dir = BaseSettings()
    log = Logger(dir.BASE_DIR_LOG)
    yaml = dir.get_config()
    for direct, listDir, file in walk_dir.walk_dbsta(dir.BASE_DIR_PROJECT):
        filePrj = Path(listDir, file)
        sheets_prj = xlsx.open_book(path=filePrj)
        st_yaml = [sheet for sheet in sheets_prj if not sheet.startswith(('К_', 'ТУ_'))]

        lsNameSt = list(map(lambda nameSt: '{0}{1}'.format('К_', nameSt), st_yaml))

        all = list(set(list(chain(st_yaml, lsNameSt))) & set(sheets_prj))
        dataFramePrj = xlsx.open_sheet(skiprows=1, sheet_name=all,path=filePrj)
        for stationTS in st_yaml:
            stationTU = '{0}{1}'.format('К_', stationTS)
            stations = list(filter(lambda x: x in sheets_prj, [stationTS, stationTU]))
            dataFrameTS = dataFramePrj.get(stationTS)
            dataFrameTamp = xlsx.open_sheet(skiprows=7,path=dir.BASE_DIR_TAMPL)
            sheets_tampl = list(dataFrameTamp.keys())

            sheets_tampl_maket = xlsx.open_book(path=dir.BASE_DIR_TAMPL_MAKET)
            dictMaket = dict.fromkeys(sheets_tampl_maket, pd.DataFrame())
            dataFrameTU = dataFramePrj.get(stationTU)

            mer = MergeXlsx(dataFrameTS, dataFrameTU, yaml)

            # if (yaml.get('create_maket')):
            path_temp_mak = Path(dir.BASE_DIR_REPORT, '{0}{1}{2}'.format('Ведомость ', stationTS, '  макет.xlsx'))
            xlsx.copy_xlsx(dir.BASE_DIR_TAMPL_MAKET, path_temp_mak)
            if stationTU in stations:
                TU = mer.tu(dataFrameTU, dataFrameTamp, sheets_tampl)
                dictMaket.update({sheets_tampl_maket[0]: TU})

            path_csv = Path(dir.BASE_DIR_DAT_MAKET, '{0}{1}'.format(stationTS.upper(), '.txt'))
            TS_Arm = xlsx.read_csv(path=path_csv,delimiter=yaml.get('delimiterDAT'))
            formatTS=mer.formatTS
            TS = dataFrameTS.filter(items=formatTS).fillna('')
            # TS = TS[~TS[formatTS[1]].str.contains('Резерв', na=False)]
            dataFrameTamp.update({sheets_tampl[0]: TS})
            if not TS_Arm.empty:
                TS = pd.concat([TS, TS_Arm.iloc[:, [1, 2]]], axis=1)
                TS = TS[~TS[formatTS[1]].str.contains('Резерв', na=False)]

            dictMaket.update({sheets_tampl_maket[1]: TS})
            xlsx.write_to_excel(dictMaket, 6, 0, stationTS, path=path_temp_mak)

            # if yaml.get('merge_reports'):
            name_rep = '{0}{1}{2}'.format('Ведомость ', stationTS, '.xlsx')
            path_temp_rep = Path(dir.BASE_DIR_REPORT, name_rep)
            xlsx.copy_xlsx(dir.BASE_DIR_TAMPL, path_temp_rep)

            path_exist_report = Path(dir.BASE_DIR_EXREPORT, name_rep)
            exist_report = xlsx.open_sheet(path=path_exist_report, sheet_name=None,skiprows=1)
            dataFrameTamp = mer.merge_report(exist_report,yaml,dataFrameTamp=dataFrameTamp,path=path_exist_report)

            xlsx.write_to_excel(dataFrameTamp, 7, 0, stationTS, path=path_temp_rep)

            path_csv = Path(dir.BASE_DIR_CSV, '{0}{1}'.format(stationTS.upper(), '.csv'))
            exist_report = xlsx.read_csv(path=path_csv, skiprows=0, delimiter=';')
            if not exist_report.empty:
                name_station = exist_report.loc[1, 'NETNAME']
                exist_report=mer.rename_columns(exist_report)

                # if yaml.get('check_csv'):
                dictMaket = mer.check_csv(exist_report, dictMaket)

                # if yaml.get('check_dat'):
                for path_csv in [Path(dir.BASE_DIR_DAT, '{0}{1}{2}'.format(name_station.lower(), '#1', '.txt')),
                                 Path(dir.BASE_DIR_DAT, '{0}{1}{2}'.format(name_station.upper(), '#1', '.txt'))]:
                    if os.path.exists(path_csv):
                        exist_dat = xlsx.read_csv(path=path_csv, skiprows=0, delimiter='\t').loc[2:, :]
                        dictMaket = mer.check_dat(exist_dat.loc[2:, :], dictMaket, TS)

                if not dictMaket.get('ТУ').empty or not dictMaket.get('ТС').empty:
                    path_csv = Path(dir.BASE_DIR_CSV, '{0}{1}{2}'.format('Ведомость ', stationTS, '  csv.xlsx'))
                    xlsx.copy_xlsx(dir.BASE_DIR_TAMPL_CSV, path_csv)
                    xlsx.write_to_excel(dictMaket, 7, 0, stationTS, path=path_csv)
    # qml()
