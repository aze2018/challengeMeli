import pymysql
import sshtunnel

class Database_Singleton(object):

    _instance = None

 #   engine = create_engine('mysql+pymysql://aze2020:meli1234@aze2020.mysql.pythonanywhere-services.com/aze2020$MELI_DB', pool_recycle=299)

#    connection = engine.connect()
    
    connection = pymysql.connect(
        host='aze2020.mysql.pythonanywhere-services.com',
        user='aze2020',
        passwd='meli1234',
        port = 3306,
        db='aze2020$MELI_DB'
    )

    def __new__(cls):
        if  Database_Singleton._instance is None:
            Database_Singleton._instance = object.__new__(cls)
        return Database_Singleton._instance

    def insert_OS_Data(self, os_dic):
        mycursor = self.connection.cursor()
        mycursor.callproc('insert_os_data',(os_dic['System_Name'],os_dic['Node'],os_dic['Version']))
        self.connection.commit()
        mycursor.close()

    def insert_Proccesor_Data(self, procc_dic):
        mycursor = self.connection.cursor()
        mycursor.callproc('insert_proccesor_data', (procc_dic['Brand'], procc_dic['Speed'], procc_dic['Vendor_ID']))
        self.connection.commit()
        mycursor.close()

    def insert_servers_Data(self, os_dic, procc_dic, server_dic):
        mycursor = self.connection.cursor()
        mycursor.callproc('insert_servers_data',
                            (   str(server_dic['Date']), server_dic['IP'],
                                procc_dic['Brand'],procc_dic['Vendor_ID'],procc_dic['Speed'],
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

