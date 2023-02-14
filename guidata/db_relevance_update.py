import copy

# to check
# haven't start to use it
# try to make a module that can go over all filelist, or nodelist, and check if any of them can
# be database relevant for the connected database
# that means, I need
# (1) a mechanism to indicate the currently connected databases, which can be more than one
# (2) when nodelist is loaded, there needs to be a way to indicate whether a sql file is database
#     relevance, and relevance to what database.

#
class DatabaseReleVanceCheck:
    def __init__(self):
        i = 1

    def nodeid(self, filelist, sql, glo):
        sqllist = []
        for file_ in filelist:
            suffix = file_[5]
            if suffix == 'sql':
                print("travel_dir.py,   build_sqllist(),   file_=", file_)
                glo.fileid = file_[0]
                sqlcontent = file_[8]
                sqlobj = SqlDecom()  # SQL decomposition root

                #                print("travel_dir.py,     file_[6]=", file_[6])
                sql_decom_list = sqlobj.a_file_sqldecoms_(sqlcontent, glo)
                if sql_decom_list:
                    if type(sql_decom_list) == type([]):
                        print("build_sqllist(),  sql_decom success")
                        #                        print("travel_dir.py,      111  sql_decom_list=", sql_decom_list)
                        sqllist.extend(sql_decom_list)
                    elif type(sql_decom_list) == type("xxx"):
                        #                        print("travel_dir.py,      222  sql_decom_list=", sql_decom_list)
                        file_[9] = str(sql_decom_list)