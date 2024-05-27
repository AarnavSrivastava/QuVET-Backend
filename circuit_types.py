from enum import Enum

class Wire:
    def __init__(self, index, gates):
        self.index = index
        self.gates = gates

class QuantumGate(Enum):
    X = 'X',
    Y = 'Y',
    Z = 'Z',
    H = 'H',
    CNOT = 'CNOT',
    SWAP = 'SWAP',
    TOFFOLI = 'Toffoli',
    S = 'S',
    T = 'T',
    MEASUREMENT = 'Measurement'

class Gate:
    def __init__(self, index, gate_type, wires):
        self.index = index
        self.type = gate_type
        self.wires = wires