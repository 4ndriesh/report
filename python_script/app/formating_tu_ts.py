# -*- coding: utf-8 -*-
import pandas as pd

class TuTs:
    def tu(self,TU,format,dataFrameTamp,sheets_tampl):
        PP2=format[0]
        Name_TU=format[1]
        in_param=pd.concat(dataFrameTamp.values()).iloc[:, 1]
        TU = TU[~TU[PP2].astype(str).str.contains('--', na=False)]
        rows = list(TU[TU[Name_TU].isin(in_param)].index)
        rows.append(TU.last_valid_index()+1)
        dict_for_write = dict(map(lambda x: (TU.loc[rows[x], Name_TU], TU.loc[rows[x]:rows[x + 1]-1]), range(0, len(rows) - 1)))
        sheets_tampl=iter(sheets_tampl)
        next(sheets_tampl)
        for key in sheets_tampl:
            ls = [dict_for_write.get(x) for x in dataFrameTamp.get(key)[PP2] if dict_for_write.get(x) is not None]
            if ls: dataFrameTamp.update({key: pd.concat(ls)})
        TU[1] = "Да"
        TU[2] = "Да"
        TU[3] = "Да"
        return TU
    def ts(self,TS,SIGN):
        return TS[~TS[SIGN].str.contains('Резерв', na=False)]