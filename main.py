# using flask_restful 
from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api 

from circuit_types import Gate, QuantumGate, Wire

import pennylane as qml
import numpy as np
import json

dev = qml.device("default.qubit", wires=10)

# creating the flask app
app = Flask(__name__)
# creating an API object 
api = Api(app)

# making a class for a particular resource 
# the get, post methods correspond to get and post requests 
# they are automatically mapped by flask_restful. 
# other methods include put, delete, etc. 
class Running(Resource): 
    # corresponds to the GET request. 
    # this function is called whenever there 
    # is a GET request for this resource 
    def get(self): 
        return "Server is Running!"
  
    # Corresponds to POST request 
    # def post(self):   
    #     data = request.get_json()     # status code 
    #     return make_response(jsonify({'data': data}), 201)

# # another resource to calculate the square of a number 
# class Square(Resource): 
#     def get(self, num): 
#         return jsonify({'square': num**2}) 

@qml.qnode(dev)
def run_circuit(wires):
    for i in range(len(wires)):
        w = wires[i]

        gates = w.gates

        for gate in gates:
            if gate.gate_type == QuantumGate.X:
                qml.PauliX(wires=i)
            elif gate.gate_type == QuantumGate.Y:
                qml.PauliY(wires=i)
            elif gate.gate_type == QuantumGate.Z:
                qml.PauliZ(wires=i)
            elif gate.gate_type == QuantumGate.H:
                qml.Hadamard(wires=i)
            elif gate.gate_type == QuantumGate.S:
                qml.S(wires=i)
            elif gate.gate_type == QuantumGate.T:
                qml.T(wires=i)
    
    return qml.probs([i for i in range(len(wires))])
    # return qml.state()

class Circuit(Resource):
    def post(self):
        data = request.get_json()

        if (isinstance(data, str)):
            data = json.loads(data)

        wires = []

        for wire_json in data["data"]:
            gates = []

            for gate_json in wire_json["gates"]:
                gate = Gate(len(gates), QuantumGate[gate_json["type"]], len(wires))
                gates.append(gate)
            
            wire = Wire(len(wires), gates)
            wires.append(wire)

        probs = run_circuit(wires)

        return make_response(jsonify({'probabilities': probs.numpy().tolist()}), 201)
  
# adding the defined resources along with their corresponding urls 
api.add_resource(Running, '/') 
# api.add_resource(Square, '/square/<int:num>')
api.add_resource(Circuit, '/circuit')
  
  
# driver function 
if __name__ == '__main__': 
    app.run(debug = True) 