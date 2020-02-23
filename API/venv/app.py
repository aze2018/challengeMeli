from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from database_singleton import Database_Singleton

app = Flask(__name__)
api = Api(app)

@app.route("/", methods=['POST'])
def persist_information():
    data_dictionary = request.get_json(force=True)

    instance_db = Database_Singleton()

    instance_db.insert_OS_Data(data_dictionary['OS'])
    instance_db.insert_Proccesor_Data(data_dictionary['Proccesor'])
    instance_db.insert_servers_Data(data_dictionary['OS'],data_dictionary['Proccesor'],data_dictionary['Server'])
    instance_db.insert_processes_data(data_dictionary['Processes'], data_dictionary['Server'])
    instance_db.insert_users_data(data_dictionary['Users'],data_dictionary['Server'])

    return jsonify({'Status API Challenge Meli': 'Informacion recibida correctamente'})

@app.route("/", methods=['GET'])
def index():
    return jsonify({'Status API': 'API Meli Challenge'})

if __name__ == '__name__':
    app.run(debug = True)
