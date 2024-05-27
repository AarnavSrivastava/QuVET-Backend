# using flask_restful 
from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api 

from circuit_types import Gate, QuantumGate, Wire

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

class Circuit(Resource):
    def post(self):
        data = request.get_json()

        wires = []

        for wire_json in data["data"]:
            gates = []

            for gate_json in wire_json["gates"]:
                gate = Gate(len(gates), QuantumGate[gate_json["type"]], len(wires))
                gates.append(gate)
            
            wire = Wire(len(wires), gates)
            wires.append(wire)
        
        
        
        return make_response(jsonify({'data': len(wires)}), 201)
  
# adding the defined resources along with their corresponding urls 
api.add_resource(Running, '/') 
# api.add_resource(Square, '/square/<int:num>')
api.add_resource(Circuit, '/circuit')
  
  
# driver function 
if __name__ == '__main__': 
    app.run(debug = True) 