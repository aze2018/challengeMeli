import requests
import json
import getters, config

def post_api(url, data):
    rta = requests.post(url, data = json.dumps(data))
    if rta.status_code == 200:
        print(rta.text)
    else:
        print("Error: Intente nuevamente")

def main():
    Server_Data = get_server_data()
    OS_Data = get_os_information()
    Processor_Data = get_processor_information()
    Processes_data = get_processes_information()
    Users_Data = get_users_information()

    dictonary_set = {'OS':OS_Data, 'Proccesor':Processor_Data, 'Server':Server_Data,'Users':Users_Data ,'Processes':Processes_data}

    post_api(config.URL_API,dictonary_set)

main()

