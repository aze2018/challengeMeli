from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from database_singleton import Database_Singleton

app = Flask(__name__)
api = Api(app)

@app.route("/", methods=['POST'])
def persist_information():
    data_dictionary = request.get_json(force=True)

    instance_db = Database_Singleton() ##testearlo dsp

    instance_db.insert_OS_Data(data_dictionary['OS'])
    instance_db.insert_Proccesor_Data(data_dictionary['Proccesor'])
    instance_db.insert_servers_Data(data_dictionary['OS'],data_dictionary['Proccesor'],data_dictionary['Server'])
    instance_db.insert_processes_data(data_dictionary['Processes'], data_dictionary['Server'])
    instance_db.insert_users_data(data_dictionary['Users'],data_dictionary['Server'])

    return jsonify(data_dictionary)

@app.route("/", methods=['GET'])
def index():
    return jsonify({'Status API': 'API Meli Challenge'})


if __name__ == '__name__':
    app.run(debug = True, port=5000)






'''
class OS(Resource): #Sistemas Operativos
    def post(self):
        os_data = request.get_json(force=True)
        instance_db = Database_Singleton()
        instance_db.insert_OS_Data(os_data['System_Name'],os_data['Node'],os_data['Version'])

        #handlear
        instance_db.set_os_id(os_data['System_Name'],os_data['Node'],os_data['Version'])

        return jsonify(os_data)

class Proccesor(Resource): #Procesadores
    def post(self):
        processor_data = request.get_json(force=True)
        instance_db = Database_Singleton()
        instance_db.insert_Proccesor_Data(processor_data['Brand'], processor_data['Vendor_ID'], processor_data['Speed'])

        return jsonify(processor_data)

class Procceses(Resource): #Procesos en ejecucion
    def post(self):
        processes_data = request.get_json(force=True)
        #persistir aca

        return jsonify(processes_data)

class User(Resource): #Usuarios
    def post(self):
        users_data = request.get_json(force=True)
        #persistir aca

        return jsonify({'Status' : 'Users Information received'})

api.add_resource(OS, '/OS_Data')
api.add_resource(Proccesor, '/Processor_Data')
api.add_resource(Procceses, '/Processes_Data')
api.add_resource(User, '/Users_Data')
'''