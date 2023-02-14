__author__ = 'Administrator'
from trg.sql_tool.data_retrieve import data_retrieve_db_
from trg.analysis.getsqlsource  import getsqlsource_

def analysis_ctrl_(op, glo):
    print("start analysis !!!!!!!!!!!!!!!")
#    retrieved = data_retrieve_db_("TR_Node", glo)
#    retrieved = data_retrieve_db_("TR_File", glo)
    retrieved_sql = data_retrieve_db_("TR_SQL", glo)
    tablelist = getsqlsource_(retrieved_sql, glo)
    return tablelist














