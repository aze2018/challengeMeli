import pymysql
import config

class Database_Singleton(object):
    _instance = None
    connection = None

    def __new__(cls):
        if  Database_Singleton._instance is None:
            Database_Singleton._instance = object.__new__(cls)
        return Database_Singleton._instance

    def iniciar_conexion(self):
        self.connection = pymysql.connect\
        (
            host = config.MYSQL_HOST,
            user = config.MYSQL_USER,
            passwd = config.MYSQL_PASSWORD,
            db = config.MYSQL_DB
        )
    def cerrar_conexion(self):
        self.connection.close()

    def insert_OS_Data(self, os_dic):
        self.iniciar_conexion()
        mycursor = self.connection.cursor()
        mycursor.callproc('insert_os_data',(os_dic['System_Name'],os_dic['Node'],os_dic['Version']))
        self.connection.commit()
        mycursor.close()

    def insert_Proccesor_Data(self, procc_dic):
        mycursor = self.connection.cursor()
        mycursor.callproc('insert_proccesor_data', (procc_dic['Brand'], procc_dic['Vendor_ID']))
        self.connection.commit()
        mycursor.close()

    def insert_servers_Data(self, os_dic, procc_dic, server_dic):
        mycursor = self.connection.cursor()
        mycursor.callproc('insert_servers_data',
                            (   str(server_dic['Date']), server_dic['IP'],
                                procc_dic['Brand'],procc_dic['Vendor_ID'],
                                os_dic['System_Name'], os_dic['Node'], os_dic['Version']
                            )
                          )
        self.connection.commit()
        mycursor.close()

    def insert_processes_data(self, procceses_dic, server_dic):
        fecha = str(server_dic['Date'])
        mycursor = self.connection.cursor()
        for PID_i, NAME_i in procceses_dic.items():
            mycursor.callproc('insert_processes_data', (fecha, PID_i, NAME_i))
        self.connection.commit()
        mycursor.close()

    def insert_users_data(self, users_list,server_dic):
        fecha = str(server_dic['Date'])
        mycursor = self.connection.cursor()
        for user_i in users_list:
            mycursor.callproc('insert_users_data', (fecha, user_i))
        self.connection.commit()
        mycursor.close()

