import platform
import cpuinfo
import psutil
import socket
import datetime

def get_os_information():
    return {'System_Name' : platform.system(), 'Node' : platform.node(), 'Version' : platform.version()}

def get_server_data():
    return {'IP':socket.gethostbyname(socket.gethostname()),'Date' : str(datetime.datetime.now()) }

def get_processor_information():
    processor_information = cpuinfo.get_cpu_info()
    return {'Brand': processor_information['brand'], 'Speed': processor_information['hz_actual'], 'Vendor_ID': processor_information['vendor_id']}

def get_processes_information():
    processes_list = psutil.process_iter()
    Processes_Data = {}
    for x in processes_list:
        try:
            if x.pid not in Processes_Data.keys():
                Processes_Data[x.pid] = x.name()
        except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return Processes_Data

def get_users_information():
    usernames_list = []
    for user in psutil.users():
        usernames_list.append(user.name)
    return usernames_list