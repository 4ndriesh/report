# -*- coding: utf-8 -*-
import os

from functools import wraps
import pandas as pd
import itertools

from basesetting import FormatTS

class MergeXlsx(FormatTS):

    def validate_args(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            path = kwargs.get('path')
            if (os.path.exists(path)):
                return func(*args, **kwargs)
            else:
                print('{0}{1}'.format('Проверить ', path))
                return kwargs.get('dataFrameTamp')
                # raise Exception('{0}{1}'.format('Проверить ', path))

        return wrapped

    @validate_args
    def merge_report(self, exist_report,yaml,dataFrameTamp=pd.DataFrame(),path=''):
        for key in dataFrameTamp:
            if key == "№5":
                exist_report.get(key).rename(columns={exist_report.get(key).columns[2]: self.Name_TS}, inplace=True)
                dataFrameTamp.update({key: dataFrameTamp.get(key).merge(exist_report.get(key).iloc[:, [2,4,5]], how='left',
                                                                        on=self.Name_TS).drop_duplicates()})
            else:
                exist_report.get(key).rename(columns={exist_report.get(key).columns[1]: self.Name_TU,
                                                      exist_report.get(key).columns[yaml.get('№Kod_PU')]: self.Kod_PU}, inplace=True)
                dataFrameTamp.update({key: dataFrameTamp.get(key).merge(
                    exist_report.get(key).fillna('').astype(str).iloc[:, 1:], how='left',
                    on=[self.Name_TU, self.Kod_PU])})
        return dataFrameTamp

    def check_dat(self, exist_dat, dictMaket, TS):
        ls = []
        if not exist_dat.empty:
            list_col = list(exist_dat.columns.values)
            # ls = exist_dat.loc[2:,:].values.tolist()
            for column in list_col:
                li = exist_dat[column].tolist()
                ls.append(li)

        listcolumn = []
        for x, tmpls in enumerate(ls, start=1):
            for y, tmpcol in enumerate(tmpls, start=1):
                listcolumn.append('{0}{1}{2}'.format(x, '--', y))
        ls = list(itertools.chain(*ls))

        dictTmp = {self.GrImp: listcolumn, self.SIGN: ls}
        df = pd.DataFrame(dictTmp)
        df = df.drop(df.index[df[self.SIGN] == '*'])
        TS[self.GrImp] = TS[self.GrImp].replace('—', '--', regex=True)
        # TS = TS.drop(TS.index[TS[self.GrImp].str.contains('П-|A-|B-|А-|Б-')])
        merged = df.merge(TS.loc[:, [self.GrImp, self.SIGN]], indicator=True, how='outer').drop_duplicates(
            subset=[self.GrImp, self.SIGN], keep=False)
        t = merged[merged['_merge'] != 'both']
        t = t.replace({'_merge': {'left_only': 'ПО', 'right_only': 'Проект'}})
        dictMaket.update({'ТС': t})
        return dictMaket

    def check_csv(self, exist_report, dictMaket):
        key = 'ТУ'
        df2 = exist_report.reset_index()
        df2 = df2.loc[:, [self.Name_TU, self.Kod_PU]]
        df1 = dictMaket.get(key)
        df1[self.Name_TU] = df1[self.Name_TU].str.rstrip()
        df1 = df1.loc[:, [self.Name_TU, self.Kod_PU]].fillna('')
        df1 = df1.loc[df1[self.Kod_PU] != ''].reset_index()
        df1 = df1.loc[:, [self.Name_TU, self.Kod_PU]]
        df1[self.Kod_PU] = df1[self.Kod_PU].replace('//', '', regex=True)
        df2[self.Kod_PU] = df2[self.Kod_PU].replace('//', '', regex=True)
        df1[self.Kod_PU] = df1[self.Kod_PU].apply(int, base=16)
        df2[self.Kod_PU] = df2[self.Kod_PU].apply(int, base=16)
        merged = df1.merge(df2, indicator=True, how='outer').drop_duplicates(subset=[self.Name_TU, self.Kod_PU],
                                                                             keep=False)

        t = merged[merged['_merge'] != 'both']
        t[self.Kod_PU] = t[self.Kod_PU].apply(hex)
        t = t.replace({'_merge': {'left_only': 'Проект', 'right_only': 'ПО'}})
        dictMaket.update({key: t})
        return dictMaket

    def tu(self,dataFrameTU,dataFrameTamp,sheets_tampl):
        TU = dataFrameTU.filter(items=self.formatTU)
        in_param=pd.concat(dataFrameTamp.values()).iloc[:, 1]
        TU = TU[~TU[self.PP2].astype(str).str.contains('--', na=False)]
        rows = list(TU[TU[self.Name_TU].isin(in_param)].index)
        rows.append(TU.last_valid_index()+1)
        dict_for_write = dict(map(lambda x: (TU.loc[rows[x], self.Name_TU], TU.loc[rows[x]:rows[x + 1]-1]), range(0, len(rows) - 1)))
        sheets_tampl=iter(sheets_tampl)
        next(sheets_tampl)
        for key in sheets_tampl:
            ls = [dict_for_write.get(x) for x in dataFrameTamp.get(key)[self.PP2] if dict_for_write.get(x) is not None]
            if ls: dataFrameTamp.update({key: pd.concat(ls)})
        TU[1] = "Да"
        TU[2] = "Да"
        TU[3] = "Да"
        return TU

    def rename_columns(self,exist_report):
        exist_report.rename(columns={exist_report.columns[2]: self.Name_TU,
                                     exist_report.columns[-3]: self.Kod_PU}, inplace=True)
        return exist_report