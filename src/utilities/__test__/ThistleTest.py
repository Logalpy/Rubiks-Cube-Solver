import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Thistlethwaites import ThistlethwaiteSolver

# Create cube data dictionary
cube_data = {
    'top': [['B', 'W', 'W'], ['B', 'W', 'W'], ['B', 'R', 'W']],
    'front': [['W', 'G', 'O'], ['W', 'G', 'Y'], ['O', 'O', 'W']],
    'bottom': [['G', 'G', 'G'], ['Y', 'Y', 'Y'], ['Y', 'G', 'B']],
    'left': [['O', 'O', 'O'], ['O', 'O', 'O'], ['R', 'B', 'Y']],
    'right': [['G', 'R', 'R'], ['R', 'R', 'R'], ['R', 'G', 'Y']],
    'back': [['B', 'B', 'Y'], ['B', 'B', 'Y'], ['R', 'W', 'G']]
}

# Create a RubiksCube for display purposes
# Create a CFOP solver with the cube_data
solver = ThistlethwaiteSolver(cube_data)
solution = solver.solve_phase(0)
solution2 = solver.solve_phase(1)
soltuion3 = solver.solve_phase(2)
print("Solved cube:")
print(solver.cube)
print("All moves:", solution + solution2 + soltuion3)
##print("Per‑phase moves:", solver.step_moves_list)
print(solver.get_phase0_state())
print(solver.get_phase1_state())
print(solver.get_phase2_state())