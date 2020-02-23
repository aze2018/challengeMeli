import requests
import json
import config
from Extractor import *

def post_api(url, data):
    rta = requests.post(url, data = json.dumps(data))
    if rta.status_code == 200:
        print(rta.text)
    else:
        print("Error: Intente nuevamente")

def main():
    #---------Extraccion de Informacion---------
    extractor = Extractor()
    OS_Data = extractor.get_os_information()
    Server_Data = extractor.get_server_data()
    Processor_Data = extractor.get_processor_information()
    Processes_data = extractor.get_processes_information()
    Users_Data = extractor.get_users_information()
    #-------------------------------------------

    #------Envio de Informacion a la API--------
    dictonary_set = {'OS':OS_Data,
                     'Proccesor':Processor_Data,
                     'Server':Server_Data,
                     'Users':Users_Data ,
                     'Processes':Processes_data}

    post_api(config.URL_API,dictonary_set)
    #-------------------------------------------

main()

