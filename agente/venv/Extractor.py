import platform
import cpuinfo
import psutil
import socket
import datetime

#---------Clases para extraer Informacion del Servidor

class Extractor:
    # ----Extracion de Informacion del sistema operativo
    # ----Campos: Nombre del sistema - Distribucion (Debian por ejemplo) - Version del sistema
    def get_os_information(self):
        return {'System_Name': platform.system(), 'Node': platform.node(), 'Version': platform.version()}

    #----Extraccion de Informacion del servidor
    #----Campos: IP del Servidor - Datetime de extraccion
    def get_server_data(self):  # IP Y FEcha
        return {'IP': socket.gethostbyname(socket.gethostname()), 'Date': str(datetime.datetime.now())}  # revisar

    #----Extraccion de Informacion del Procesador
    #----Campos: Nombre del Procesador - Velocidad - Fabricante
    def get_processor_information(self):
        processor_information = cpuinfo.get_cpu_info()
        return {'Brand': processor_information['brand'], 'Vendor_ID': processor_information['vendor_id']}

    #----Extraccion de Informacion de los Procesos
    #----Campos: Process ID - Nombre del Proceso
    def get_processes_information(self):
        processes_list = psutil.process_iter()
        Processes_Data = {}
        for x in processes_list:
            try:
                if x.pid not in Processes_Data.keys():
                    Processes_Data[x.pid] = x.name()
            except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return Processes_Data

    #----Extraccion de Informacion de usuarios conectados
    #----Campos: Nombre del Usuario
    def get_users_information(self):
        usernames_list = []
        for user in psutil.users():
            usernames_list.append(user.name)
        return usernames_list
