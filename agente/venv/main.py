import platform
import cpuinfo
import psutil
import socket
import requests
import json
import datetime

def post_api(url, data):
    rta = requests.post(url, data = json.dumps(data))

    if rta.status_code == 200:
        print(rta.text)
    else:
        print("Error")

def get_os_information():
    return {'System_Name' : platform.system(), 'Node' : platform.node(), 'Version' : platform.version()}

def get_server_data(): #IP Y FEcha
    return {'IP':socket.gethostbyname(socket.gethostname()),'Date' : str(datetime.datetime.now()) } #revisar

def get_date():
    return

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

url_1 = "http://127.0.0.1:5000/"
url_2 = "http://127.0.0.1:5000/Processor_Data"
url_3 = "http://127.0.0.1:5000/Processes_Data"
url_4 = "http://127.0.0.1:5000/Users_Data"

def main():
    Server_Data = get_server_data()
    OS_Data = get_os_information()
    Processor_Data = get_processor_information()
    Processes_data = get_processes_information()
    Users_Data = get_users_information()

    dictonary_set = {'OS':OS_Data, 'Proccesor':Processor_Data, 'Server':Server_Data,'Users':Users_Data ,'Processes':Processes_data}

    post_api(url_1,dictonary_set)

main()


'''
OS_Data = {'System_Name' : platform.system(), 'Node' : platform.node(), 'Version' : platform.version()}
response_1 = requests.post("http://127.0.0.1:5000/OS_Data", data = json.dumps(OS_Data))
print(response_1.text)


processor_information = cpuinfo.get_cpu_info()
Processor_Data =  {'Brand' : processor_information['brand'], 'Speed' : processor_information['hz_actual'], 'Vendor_ID' : processor_information['vendor_id']}
response_2 = requests.post("http://127.0.0.1:5000/Processor_Data", data = json.dumps(Processor_Data))
print(response_2.text)


processes_list = psutil.process_iter()
Processes_Data = {}
for x in processes_list:
    try:
        if x.pid not in Processes_Data.keys():
            Processes_Data[x.pid] = x.name()
    except(psutil.NoSuchProcess, psutil.AccessDenied,psutil.ZombieProcess):
        pass

response_3 = requests.post("http://127.0.0.1:5000/Processes_Data", data=json.dumps(Processes_Data))
print(response_3.text)

usernames_list = []
for user in psutil.users():
    usernames_list.append(user.name)

response_4 = requests.post("http://127.0.0.1:5000/Users_Data", data=json.dumps(usernames_list))
print(response_4.status_code)
print(response_4.text)




-------------------
    # post_api(url_1, OS_Data)
    

    #post_api(url_2,Processor_Data)

    # post_api(url_3, Processes_data)

    #post_api(url_4, Users_Data)








'''''