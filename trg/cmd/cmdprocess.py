from trg.travel.travel_ctrl       import travel_ctrl_
from trg.searches.searchctrl      import searchctrl_
from trg.analysis.analysis_ctrl   import analysis_ctrl_
from trg.sql_tool.data_drop       import drop_all_db_tables_


def cmdprocess_(op, path_, travel_type, glo):

    if op == 't' and travel_type == 'file system':
        travel_result = travel_ctrl_(path_, glo)
        return travel_result
    elif op == 's':
        searchctrl_(path_, glo)
    elif op == 'a':
        analysis_ctrl_(path_, glo)
    elif op == 'r':
        drop_all_db_tables_(glo)
