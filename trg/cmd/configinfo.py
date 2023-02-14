try:
    import ConfigParser
except:
    import configparser

import os
from trg.tool.crypt_tool import Crypt_Decrypt_Tool

class Config:
    def __init__(self):
        self.version = 2
        try:
            self.x_ = ConfigParser.ConfigParser()
        except:
            self.x_ = configparser.ConfigParser()
            self.version = 3

    def config(self):
        return self.x_


class ConfigInfo:
    def __init__(self):
        self.config        = Config()
        self.config_reader = self.config.config()
        config_path        = os.path.abspath('config.conf')
        info               = self.config_readfile(config_path)
        if info:
            self.db_info  = info['database_info']
            self.host     = self.db_info['ip addr']
            self.port     = self.db_info['port']
            self.username = self.db_info['usrname']
            self.dbname   = self.db_info['dbname']
            self.dbtype   = self.db_info['dbtype']
            self.key      = self.db_info['key']
            crypt         = Crypt_Decrypt_Tool(key=self.key)
            password1     = str.encode(self.db_info['password']).strip()
            self.passwd   = crypt.decrypt_pwd(password1).decode()

            #print("self.host=",      self.host)
            #print("self.port=",      self.port)
            #print("self.username=", self.username)
            #print("self.dbname=",   self.dbname)
            #print("self.dbtype=",   self.dbtype)
            #print("self.key=",      self.key)
            #print("password1=",     password1)
            #print("self.passwd=",  self.passwd)
        else:
            if self.config.version == 2:
                self.host     = raw_input("ip addr: ")
                self.port     = raw_input("port: ")
                self.username = raw_input("username: ")
                self.dbname   = raw_input("dbname :")
                self.dbtype   = raw_input("dbtype : ")
                password      = raw_input("password : ")  # should use getpass,pycharm console can't use.so use input
            else:
                self.host     = input("ip addr: ")
                self.port     = input("port: ")
                self.username = input("username: ")
                self.dbname   = input("dbname :")
                self.dbtype   = input("dbtype : ")
                password      = input("password : ")  # should use getpass,pycharm console can't use.so use input
            crypt_tool = Crypt_Decrypt_Tool()
            self.passwd     = str.encode(password)
            encrypt_pwd = crypt_tool.encrypt_pwd(self.passwd)
            self.config_write(config_path, self.host, self.port, \
                                    self.username, encrypt_pwd, self.dbname, self.dbtype, crypt_tool.get_key())

    def read_(self):
        return self.host, self.port, self.username, self.passwd, self.dbname, self.dbtype

    def config_readfile(self, path_):
        config_info = {}
        self.config_reader.read(path_)
        sections = self.config_reader.sections()
        for section in sections:
            section_node = {}
            for option in self.config_reader.options(section):
                section_node[option] = self.config_reader.get(section,option)
            config_info[section] = section_node
        return config_info

#    def config_set(self, path_, password):                       # it seems no use
#        password = password.decode()                             # bytes ---> string
#        self.Config.read(path_)
#        self.Config['database_info']['password'] = password  # Config[][]
#        with open(path_,'w') as fileconfig:
#            self.Config.write(fileconfig)                        # write changed option to fileconfig at path_

    # ---- config_write() is not fully debugged   !!!!!!!!!!!!!!!!
    def config_write(self, path_, host, port, username, password, dbname, dbtype, key):
        # first time run,configfile is null.use this function
        self.config_reader.add_section("database_info")
        self.config_reader.set('database_info','ip addr', host)
        self.config_reader.set('database_info','port',    port)
        self.config_reader.set('database_info','usrname',username)
        self.config_reader.set('database_info','dbname', dbname)
        self.config_reader.set('database_info','dbtype', dbtype)
        self.config_reader.set('database_info','key',     str(key))
        password = password.decode()       # bytes ---> string
        self.config_reader.set('database_info','password',password)
        with open(path_,'w') as fileconfig:
            self.config_reader.write(fileconfig)  # write changed options to configfile.

    def flag_read(self):
        f = open("flg_ini_load.conf", "r")
        flag = f.readline()
        f.close()
        if flag.strip() == "True":
            return True
        else:
            return False

    def flag_write(self, dataInitFlag):
        f = open("flag.conf", "w")
        f.write(dataInitFlag)
        f.close()


