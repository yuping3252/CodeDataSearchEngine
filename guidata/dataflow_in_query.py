import copy


class DataFlowInQuery:
    def __init__(self):
        i = 1

    def dataflow(self, nodeid, nodelist, sqlqueryselcols, sqltrace, sqlinsertsels):
        node_clicked = []
        # ---------- find a node with given nodeid
        for node in nodelist:
            if nodeid == node[0]:
                node_clicked = node
                break
        file_id     = node_clicked[4]

        query_sqlid_list = []
        for selcol in sqlqueryselcols:
            if file_id == selcol[0] and selcol[1] not in query_sqlid_list:
                query_sqlid_list.append(selcol[1])
        a_file_querys = []
        for query_sqlid in query_sqlid_list:
            [a_sql_selsrcs, a_sql_inserts3] = \
                self.dataflow_single_query(file_id, query_sqlid, sqlqueryselcols, sqltrace, sqlinsertsels)

            # print("dataflow_in_query.py,   dataflow(),   a_sql_selsrcs=", a_sql_selsrcs, ",   a_sql_inserts3=", a_sql_inserts3)

            a_file_querys.append([a_sql_selsrcs, a_sql_inserts3])

        links = self.datalinks(a_file_querys)
        return a_file_querys, links

    # a_file_querys ......[insrttblid, insrttbl, insrtcol] + [sqlid, selcolpos, selcolnm] + [tablenm_, colnm_]
    def datalinks(self, a_file_query):
        links = []
        for query1 in a_file_query:
#            print("query1[1]=", query1[1])
            inserts = query1[1]
            for insert in inserts:
                insert_tbl   = insert[1]
                insert_col   = insert[2]
                insert_sqlid = insert[3]
                insert_pos   = insert[4]
#                print("    insert_tbl=", insert_tbl, "    insert_col=", insert_col)
                for query2 in a_file_query:
                    selcols = query2[0]
#                    print("        selcols=", selcols)
                    for selcol in selcols:
                        sel_sqlid  = selcol[0]
#                        print("            selcol=", selcol)
                        t = 0
                        for srccol in selcol:
                            if t > 2:
                                src_tbl = srccol[0]
                                src_col = srccol[1]
#                                print("                src_tbl=", src_tbl, "       src_col=", src_col)
                                if insert_tbl == src_tbl and insert_col == src_col:
                                    link = [insert_sqlid, insert_tbl, insert_col, insert_pos, sel_sqlid]
                                    links.append(link)
                            t += 1
#        print("-----------------------------dataflow_in_query, links=", links)
        return links

    def dataflow_single_query(self, file_id, query_sqlid, sqlqueryselcols, sqltrace, sqlinsertsels):

        # ---------- find all select cols in this sql file (need the top subquery block ID to identify final select)
        a_sql_selcols = []
        for selcol in sqlqueryselcols:
            if file_id == selcol[0] and query_sqlid == selcol[1]:
                a_sql_selcols.append(selcol)
                # selcol=[file_id, sqlid, inner_query, tbl, alias, col, subqueryid, colpos,
                #                                          upperblockid, unionornot, inqueryoffset]
        # ---------- find all sqlids and all traces in this sql file
        a_sql_traces = []
        for trace in sqltrace:
            if file_id == trace[0] and query_sqlid == trace[1]:
                a_sql_traces.append(trace)
                # trace=[file_id, sqlid, inner_query, selcolpos, colpos. tblnm, colnm]
        # ---------- find all inserts in this sql file
        a_sql_inserts = []
        for insert in sqlinsertsels:
            if file_id == insert[0]:
                a_sql_inserts.append(insert)
                # insert=[fileid,sqlid,insrtpos,insrt tblid,insrt tbl,insrt col,selq,tbl,col]
        # ----------- combined relevant columns from trace and selcol
        a_sql_sels        = []
        a_sql_sel_srccols = []
        for selcol in a_sql_selcols:
            inner_q_id = selcol[2]
            tablenm    = selcol[3]
            col        = selcol[5]
            colpos     = int(selcol[7])
            sel = [query_sqlid, colpos, col]
            if sel not in a_sql_sels:
                a_sql_sels.append(sel)                         # ------------ store distinct selects only
            for trace in a_sql_traces:
                file_id_      = trace[0]
                query_sqlid_  = trace[1]
                inner_q_id_   = trace[2]
                selcolpos_    = trace[3]
                tablenm_      = trace[5]
                if file_id == file_id_ and query_sqlid == query_sqlid_ and colpos == selcolpos_\
                    and inner_q_id == inner_q_id_ and tablenm == tablenm_:
                    tablenm_  = trace[5]
                    colnm_    = trace[6]
                    sel_srccol = [query_sqlid, colpos, col, [tablenm_, colnm_]]
                    a_sql_sel_srccols.append(sel_srccol)
            for trace in a_sql_traces:
                file_id_      = trace[0]
                query_sqlid_  = trace[1]
                inner_q_id_   = trace[2]
                selcolpos_    = trace[3]
                if file_id == file_id_ and query_sqlid == query_sqlid_ and colpos == selcolpos_\
                    and inner_q_id != inner_q_id_:
                    tablenm_ = trace[5]
                    colnm_   = trace[6]
                    sel_srccol = [query_sqlid, colpos, col, [tablenm_, colnm_]]
                    a_sql_sel_srccols.append(sel_srccol)
        a_sql_sel_srccols2 = []
        for sel_srccol in a_sql_sel_srccols:
            if sel_srccol not in a_sql_sel_srccols2:
                a_sql_sel_srccols2.append(sel_srccol)
        a_sql_selsrcs = []
        for sel in a_sql_sels:
            sqlid     = sel[0]
            selcolpos = sel[1]
            selcolnm  = sel[2]
            a_selsrc = [sqlid, selcolpos, selcolnm]
            for sel_srccol2 in a_sql_sel_srccols2:
                sqlid_     = sel_srccol2[0]
                selcolpos_ = sel_srccol2[1]
                selcolnm_  = sel_srccol2[2]
                srccol     = sel_srccol2[3]
                if  sqlid == sqlid_ and selcolpos   == selcolpos_ and selcolnm == selcolnm_:
                    a_selsrc.append(srccol)
            a_sql_selsrcs.append(a_selsrc)
# a_sql_selsrcs { [query_sqlid, colpos, col, [tablenm_, colnm_], [tablenm_, colnm_], ......}

        # --------- if union, eliminate select column names
        a_sql_selsrcs = self.union_sel_merge(a_sql_selsrcs)

        # --------- combined inserts with select
        # insert=[fileid,sqlid,insrtpos,insrt tblid,insrt tbl,insrt col,selq,tbl,col]
        a_sql_inserts2 = []
        for insert in a_sql_inserts:
            sqlid      = insert[1]
            insrtpos   = int(insert[2])
            insrttblid = insert[3]
            insrttbl   = insert[4]
            insrtcol   = insert[5]
            for sel in a_sql_selsrcs:
                if query_sqlid == sqlid and insrtpos == sel[1]:
                    insert2 =  [insrttblid, insrttbl, insrtcol] + sel
                    a_sql_inserts2.append(insert2)
        a_sql_inserts3 = self.union_insert_merge(a_sql_inserts2)
        return a_sql_selsrcs, a_sql_inserts3

    def union_sel_merge(self, a_sql_selsrcs):
        a_sql_nullcol = copy.deepcopy(a_sql_selsrcs)
        for a_col in a_sql_nullcol:
            a_col[2] = ""
        unioned = False
        a_sql_src_sets = []
        for nullcol in a_sql_nullcol:
            sel     = nullcol[:3]
            src_set = set()
            i = 0
            for src in nullcol[3:]:
                src1 = '%%%'.join(src)
                src_set.add(src1)
                i += 1
            if i > 1:
                unioned = True
            if [sel, src_set] not in a_sql_src_sets:
                a_sql_src_sets.append([sel, src_set])
        a_sql_sel_srccols = []
        for sel_src_set in a_sql_src_sets:
            sel = sel_src_set[0]
            src_set = sel_src_set[1]
            for src in src_set:
                src2 = src.split('%%%')
                sel.append(src2)
            a_sql_sel_srccols.append(sel)
        return a_sql_sel_srccols


    def union_insert_merge(self, a_sql_inserts2):
        a_sql_inserts3 = []
        for insert in a_sql_inserts2:
            if insert not in a_sql_inserts3:
                a_sql_inserts3.append(insert)
        return a_sql_inserts3
