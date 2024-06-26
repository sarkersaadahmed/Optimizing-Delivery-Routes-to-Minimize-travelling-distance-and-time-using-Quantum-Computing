import numpy as np
from qiskit.optimization import QuadraticProgram #provides quadratic problems which in a way can either be solved classic or quantum
#as mentioned the fact that quantum computer can act both as a classical behaivour and quantum behaivour
from qiskit.optimization.algorithms import MinimumEigenOptimizer #provides different quantum algorithms which
#in this case makes use of whatever algorithm is required to output a ground state adibaple pathway
from qiskit.aqua.algorithms import QAOA #the main algorithm [Quantum Approximate Optimization Algorithm] 
#one of the fundamental algorithms to output an approximate and adibaple pathway
from qiskit.aqua.components.optimizers import COBYLA #converting classical parameters into quantum algorithms
from qiskit import Aer #Backend simulator for qiskit modules which allows the quantum
#algorithms to run on classical hardware in order to simulate quantum circuits

#for easy purposes rather than using anonymous nodal points like A, B, C, D or E or any variables
#actual numbers has been used to identify the actual nodal point value to ensure when
#calculating the hamiltonian sum weight when calculating edge nodal points
#to observe the minimal cost, no stress on nodal points are
#made
distances = np.array([[0, 10, 15, 20],
                      [10, 0, 35, 25],
                      [15, 35, 0, 30],
                      [20, 25, 30, 0]])
qp = QuadraticProgram()

#identified the length [or the distance] of those nodal point values as
#num_cities identifying the value between two nodal points

num_cities = len(distances) 
for i in range(num_cities): #i denotes the starting city and we will iterate the length of the distances from the starting city
    for j in range(num_cities): #j denotes final city
        if i != j: #our main objective is to ensuire that the final city is not equivalent to the initial city due to hadamard cycle
            qp.binary_var(name=f'x_{i}_{j}') #hadamard cycle should move once and i == j would mean it didnt move

objective = 0 #same thing here BUT because we need to find the nodal points, we will continue to update the nodal points
for i in range(num_cities): #everytime one nodal point to another nodal point journey has been made 
    for j in range(num_cities): #as long as that starting nodal point is not equivalent to final nodal point
        if i != j:
            objective += distances[i][j] * qp.get_variable(f'x_{i}_{j}')
qp.minimize(objective)

for i in range(num_cities):
    qp.linear_constraint(linear={f'x_{i}_{j}': 1 for j in range(num_cities) if i != j}, sense='==', rhs=1)
    qp.linear_constraint(linear={f'x_{j}_{i}': 1 for j in range(num_cities) if i != j}, sense='==', rhs=1)
#we set constrains because as stated by the hadamard cycle "the nodal points can only move once"
