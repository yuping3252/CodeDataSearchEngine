import re
import logging


def s_dflow_file(filename):
    relation = []
"""
    conn = dbconnect()
    file_id   = selecttb(conn,'sql_file','id',whc="name='%s'"%filename)
    logging.debug("fileid =%s",file_id[0][0])
    sql_all    = selecttb(conn,'sql_all',whc="prt_id=%s"%file_id[0][0])
    if sql_all:
        logging.debug("sql_all______=%s",sql_all)
        for node in sql_all:
            #logging.debug("node______=%s",node)
            if node and re.search('^select',node[1]):
                node_relation = {}
                from_node = selecttb(conn,'sql_frm',whc="prt_id=%s"%node[0])
                if from_node:
                    #logging.debug("parent_table = %s,file=%s",from_node[0][1],filename)
                    node_relation['par'] = from_node[0][1]
                    node_relation['cur'] = filename
                logging.debug("node_select =%s",node_relation)
            elif node and re.search('^insert',node[1]):
                logging.debug("_______________")
                node_relation = {}
                from_node = selecttb(conn,'sql_frm',whc="prt_id=%s"%node[0])
                to_node = selecttb(conn,'sql_inst',whc="prt_id=%s"%node[0])
                logging.debug("from=%s,to=%s",from_node,to_node)
                if from_node and to_node:
                    logging.debug("parent_table=%s,file=%s,child_table=%s",from_node[0][1],filename,to_node[0][1])
                    node_relation['par'] = from_node[0][1]
                    node_relation['cur'] = filename
                    node_relation['cld'] = to_node[0][1]
            if node_relation:
                relation.append(node_relation)
    #logging.debug("relation = %s",relation)
    return relation
"""
