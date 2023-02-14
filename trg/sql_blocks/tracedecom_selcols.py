__author__ = 'Administrator'

class TraceSelectCol:
    def __init__(self):
        i = 0

    def trace_sel_cols_(self, query_nested, traced_cols_):
        trace_lists = []
        for qnlist in query_nested:
            trace_list = []
            for qn in qnlist:
                trace_qn = []
                for col in traced_cols_:
                    if qn[0] == col[0]:
                        trace_qn.append(col)
                trace_list.append(trace_qn)
            trace_lists.append(trace_list)

        traced_sel_cols = []
        for trace_list in trace_lists:
            trace_list.reverse()
            cols = []
            for cols_ in trace_list:
                if cols_ != []:
                    cols = cols_
                    break
            if cols:
                for c in cols:
                    if traced_sel_cols.count(c) == 0:
                        traced_sel_cols.append(c)
        return traced_sel_cols
