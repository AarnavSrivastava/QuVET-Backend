# using flask_restful 
from flask import Flask, jsonify, request, make_response, send_file
from flask_restful import Resource, Api 

from circuit_types import Gate, QuantumGate, Wire

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib
matplotlib.use('Agg')

import pennylane as qml
import numpy as np
import json
import uuid
dev = qml.device("default.qubit", wires=10)

# creating the flask app
app = Flask(__name__)
# creating an API object 
api = Api(app)

class Running(Resource): 
    def get(self): 
        return "Server is Running!"

def plotter(angles, output_states, bgcolor='#86acb5', output_file='plot.png'):
    # Extract the real and imaginary parts of the state vector
    real_parts = np.real(output_states)
    imag_parts = np.imag(output_states)

    dosis_font_path = 'fonts/Dosis-VariableFont_wght.ttf'
    dosis_font = fm.FontProperties(fname=dosis_font_path)

    # Create a figure
    fig, ax = plt.subplots(figsize=(12, 6))

    # Set the background color for the entire figure using the hex value
    fig.patch.set_facecolor(bgcolor)
    ax.set_facecolor(bgcolor)

    # Plot the real parts
    for i in range(real_parts.shape[1]):
        ax.plot(angles, real_parts[:, i], label=f'Real part of component {i}')

    # Plot the imaginary parts
    for i in range(imag_parts.shape[1]):
        ax.plot(angles, imag_parts[:, i], linestyle='--', label=f'Imaginary part of component {i}')

    # Set titles and labels
    ax.set_title('Real and Imaginary parts of the state vector components')
    ax.set_xlabel('Angle')
    ax.set_ylabel('Value')
    ax.legend()

    # Display the plot
    plt.tight_layout()
    plt.savefig(output_file, bbox_inches='tight', facecolor=fig.get_facecolor())

    # Close the plot to free up memory
    plt.close(fig)

@qml.qnode(dev)
def run_circuit_probs(wires):
    dev = qml.device("default.qubit", wires=len(wires))

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

@qml.qnode(dev)
def run_circuit_state(wires):
    dev = qml.device("default.qubit", wires=len(wires))

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
    
    return qml.state()

class RunCircuit(Resource):
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

        probs = run_circuit_probs(wires)

        return make_response(jsonify({'probabilities': probs.numpy().tolist()}), 201)

class GenCircuitImage(Resource):
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

        angles = np.linspace(0, 4 * np.pi, 50)  # Reduced from 200 to 50
        output_states = np.array([run_circuit_state(wires) for t in angles])

        plotter(angles, output_states, bgcolor='#86acb5', output_file=f'first_graph.png')

        return send_file(f'first_graph.png', as_attachment=True)
        # return make_response(jsonify({'probabilities': probs.numpy().tolist()}), 201)

# adding the defined resources along with their corresponding urls 
api.add_resource(Running, '/') 
# api.add_resource(Square, '/square/<int:num>')
api.add_resource(RunCircuit, '/circuit')
# api.add_resource(GenCircuitImage, '/circuit/graph')
  
  
# driver function 
if __name__ == '__main__': 
    app.run(debug = True) 