__author__ = 'Administrator'

from trg.analysis.src_tables   import Src_Tables
from trg.analysis.src_columns  import Src_Columns

def getsqlsource_(data, glo):
    srctbls = Src_Tables()
    srccols = Src_Columns()
    fromtbls = srctbls.sourcetbls_(data, "from", glo)
    jointbls = srctbls.sourcetbls_(data, "join table", glo)
    cols = srccols.sourcecols_(data, glo)
    fromtbls.extend(jointbls)
    return fromtbls