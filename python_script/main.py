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
from merge_xlsx import MergeXlsx
import walk_dir
import itertools

if __name__ == "__main__":
    tuts=TuTs()
    xlsx = Xlsx()
    dir = BaseSettings()
    log = Logger()
    yaml = dir.get_config()
    # st_yaml = yaml.get('station')
    for direct, listDir, file in walk_dir.walk_dbsta(dir.BASE_DIR):
        filePrj=os.path.join(listDir,file)
        log.message_debug(filePrj)
        # filePrj = os.path.join(dir.BASE_DIR, *yaml.get('file_prj'))
        sheets_prj = xlsx.open_book(path=filePrj)
        st_yaml = [sheet for sheet in sheets_prj if not sheet.startswith(('К_','ТУ_'))]
        # all=[sheet for sheet in sheets_prj if not sheet.startswith(('ТУ_'))]

        lsNameSt = list(map(lambda nameSt: '{0}{1}'.format('К_', nameSt), st_yaml))
        # lsNameSt=[sheet for sheet in sheets_prj if  sheet.startswith(('К_'))]
        # all=list(chain(st_yaml, lsNameSt))

        all = list(set(list(chain(st_yaml, lsNameSt)))&set(sheets_prj))
        dataFramePrj = xlsx.open_sheet(path=filePrj, skiprows=1, sheet_name=all)
            # dataFramePrj = xlsx.open_sheet(path=filePrj, skiprows=1, sheet_name=all)
            # st_yaml=[sheet for sheet in all if not sheet.startswith(('К_'))]
        for st in st_yaml:
            stationTS = st
            stationTU = '{0}{1}'.format('К_', stationTS)
            stations = list(filter(lambda x: x in sheets_prj, [st, stationTU]))
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

            path_temp = os.path.join(dir.BASE_DIR, *yaml.get('name_tampl'))
            name_rep='{0}{1}{2}'.format('Ведомость ', stationTS, '.xlsx')
            path_temp_rep = os.path.join(dir.BASE_DIR_REPORT, name_rep)
            xlsx.copy_xlsx(path_temp, path_temp_rep)


            if(yaml.get('create_maket')):
                path_temp = os.path.join(dir.BASE_DIR, *yaml.get('name_tampl_maket'))
                path_temp_mak = os.path.join(dir.BASE_DIR_REPORT,
                                             '{0}{1}{2}'.format('Ведомость ', stationTS, '  макет.xlsx'))
                xlsx.copy_xlsx(path_temp, path_temp_mak)

                path_csv = os.path.join(dir.BASE_DIR_REPORT, '{0}{1}'.format(stationTS.upper(), '.txt'))
                if (os.path.exists(path_csv)):
                    TS_Arm = xlsx.read_csv(path_csv)
                    TS = pd.concat([TS, TS_Arm.iloc[:, [1, 2]]], axis=1)
                TS = tuts.ts(TS, SIGN)
                dictMaket.update({sheets_tampl_maket[1]: TS})
                xlsx.write_to_excel(dictMaket, 6, 0, path_temp_mak, stationTS)

            TS=tuts.ts(TS,SIGN)
            dataFrameTamp.update({sheets_tampl[0]: TS.filter(items=[PPTS, SIGN, Name_TS, GrImp])})

            if yaml.get('merge_reports'):
                path_exist_report = os.path.join(dir.BASE_DIR_EXREPORT, name_rep)
                if (os.path.exists(path_exist_report)):
                    mer=MergeXlsx()
                    dataFrameTamp=mer.merge_report(dataFrameTamp,xlsx,path_exist_report,Name_TS,Kod_PU,Name_TU)

            xlsx.write_to_excel(dataFrameTamp, 7, 0, path_temp_rep, stationTS)
            log.message_debug(stationTS)


            if yaml.get('check_csv'):
                path_csv = os.path.join(dir.BASE_DIR_CSV, '{0}{1}'.format(stationTS.upper(), '.csv'))
                if (os.path.exists(path_csv)):
                    exist_report=xlsx.read_csv(path_csv,skiprows=0,delimiter=';')
                    key='ТУ'
                    exist_report.rename(
                        columns={exist_report.columns[2]: Name_TU, exist_report.columns[-3]: Kod_PU},
                        inplace=True)
                    name_station=exist_report.loc[1,'NETNAME']
                    if yaml.get('check_dat'):
                        path_csv = os.path.join(dir.BASE_DIR_DAT, '{0}{1}{2}'.format(name_station.lower(),'#1', '.txt'))
                        # exist_dat=pd
                        if (os.path.exists(path_csv)):
                            exist_dat = xlsx.read_csv(path_csv, skiprows=0, delimiter='\t').loc[2:,:]
                        else:
                            path_csv = os.path.join(dir.BASE_DIR_DAT,'{0}{1}{2}'.format(name_station.upper(), '#1', '.txt'))
                        if (os.path.exists(path_csv)):
                            exist_dat = xlsx.read_csv(path_csv, skiprows=0, delimiter='\t').loc[2:,:]
                        if not exist_dat.empty:
                            list_col=list(exist_dat.columns.values)
                            # ls = exist_dat.loc[2:,:].values.tolist()
                            ls=[]
                            for column in list_col:
                                li = exist_dat[column].tolist()
                                ls.append(li)

                            listcolumn = []
                            for x, tmpls in enumerate(ls,start=1):
                                for y, tmpcol in enumerate(tmpls,start=1):
                                    listcolumn.append('{0}{1}{2}'.format(x, '--', y))
                            ls=list(itertools.chain(*ls))

                            dictTmp={GrImp:listcolumn,SIGN:ls}
                            df = pd.DataFrame(dictTmp)
                            df=df.drop(df.index[df[SIGN]=='*'])
                            TS[GrImp]=TS[GrImp].replace('—', '--', regex=True)
                            TS=TS.drop(TS.index[TS[GrImp].str.contains('П-|A-|B-|А-|Б-')])
                            merged = df.merge(TS.loc[:,[GrImp,SIGN]], indicator=True, how='outer').drop_duplicates(subset=[GrImp,SIGN], keep=False)
                            t = merged[merged['_merge'] != 'both']
                            t = t.replace({'_merge': {'left_only': 'ПО', 'right_only': 'Проект'}})
                            dictMaket.update({'ТС': t})

                    df2=exist_report.reset_index()
                    df2 = df2.loc[:, [Name_TU, Kod_PU]]
                    df1 = dictMaket.get(key)
                    df1[Name_TU] = df1[Name_TU].str.rstrip()
                    df1=df1.loc[:,[Name_TU,Kod_PU]].fillna('')
                    df1=df1.loc[df1[Kod_PU]!=''].reset_index()
                    df1 = df1.loc[:, [Name_TU, Kod_PU]]
                    df1[Kod_PU] = df1[Kod_PU].replace('//', '', regex=True)
                    df2[Kod_PU] = df2[Kod_PU].replace('//', '', regex=True)
                    df1[Kod_PU]= df1[Kod_PU].apply(int, base=16)
                    df2[Kod_PU] = df2[Kod_PU].apply(int, base=16)
                    merged=df1.merge(df2, indicator=True,how='outer').drop_duplicates(subset=[Name_TU,Kod_PU], keep=False)

                    t=merged[merged['_merge']!='both']
                    t[Kod_PU] = t[Kod_PU].apply(hex)
                    t=t.replace({'_merge': {'left_only': 'Проект', 'right_only': 'ПО'}})
                    dictMaket.update({key: t})
                    if not dictMaket.get('ТУ').empty or not dictMaket.get('ТС').empty:
                        path_temp = os.path.join(dir.BASE_DIR, *yaml.get('name_tampl_csv'))
                        path_csv = os.path.join(dir.BASE_DIR_CSV,
                                                     '{0}{1}{2}'.format('Ведомость ', stationTS, '  csv.xlsx'))
                        xlsx.copy_xlsx(path_temp, path_csv)

                        xlsx.write_to_excel(dictMaket, 7, 0, path_csv, stationTS)


    # qml()
