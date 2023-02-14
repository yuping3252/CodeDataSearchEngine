__author__ = 'Administrator'


def drop_all_db_tables_(globaldata):
    # why this function is called data_clean:
    # first,this function use clean all data of user travel result include database table
    # second,in the future,we also add some function to remove the global data of user operated.


    # drop all our created tables in the special database
    dbserver = globaldata.dbserver_[-1]
    tablename_list2 = ['trdb','trtable','trcolumn','trtablerelate',
                      'trnode','trnodecontentdecomp',
                      'trsql','trsqlselect','trsqlfrom',
                      'trsqljoin','trsqlwhere','trsqlvstable',
                      'trsearchcategory','trsearchcase','trsearch',
                      'trsearchcond','trsearchnode']

    tablename_list = [
        "\"TRC_Case\"",
        "\"TRC_CaseSearchCross\"",
        "\"TRC_Display\"",
        "\"TRC_DisplayCaseCross\"",
        "\"TRC_NodeDisplayCoordinate\"",
        "\"TRC_SearchNodeCross\"",
        "\"TRO_MaxID\"",
        "\"TRR_FileDataFlow\"",
        "\"TRR_FileFile\"",
        "\"TRSQL_Block\"",
        "\"TRSQL_BlockColumn\"",
        "\"TRSQL_BlockHost\"",
        "\"TRSR_Chain\"",
        "\"TRSR_PickupNodeCross\"",
        "\"TRSR_Result\"",
        "\"TRSR_ResultNodeList\"",
        "\"TRSR_SearchChainCross\"",
        "\"TRS_CondCross\"",
        "\"TRS_Condition\"",
        "\"TRS_SearchHead\"",
        "\"TRS_StartItem\"",
        "\"TRT_CategoryAssoc\"",
        "\"TRT_CategoryCommon\"",
        "\"TRT_CategoryCommonHistory\"",
        "\"TRT_CategoryTech\"",
        "\"TRT_CategoryTechHistory\"",
        "\"TRT_CommonTerm\"",
        "\"TRT_CommonTermAssoc\"",
        "\"TRT_Owner\"",
        "\"TRT_TechTerm\"",
        "\"TR_Column\"",
        "\"TR_DB\"",
        "\"TR_DBCross\"",
        "\"TR_File\"",
        "\"TR_SQLTableCross\"",
        "\"TR_Server\"",
        "\"TR_SmallColumn\"",
        "\"TR_StoredProc\"",
        "\"TR_Table\"",
        "\"TR_TreeColumns\"",
        "\"TR_TreeFiles\"",
        "\"TR_TreeTables\""]

    for table in tablename_list:
        dbserver.tbldrop(table)
