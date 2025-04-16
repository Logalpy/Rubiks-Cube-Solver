import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cube import RubiksCube
from Thistlethwaites import ThistlethwaiteSolver



cube = RubiksCube()
cube.load_from_cube_data({
    'top': [['R', 'R', 'O'], ['W', 'W', 'O'], ['O', 'O', 'Y']],  # Up/white
    'front': [['W', 'W', 'B'], ['R', 'G', 'W'], ['B', 'O', 'Y']],  # front/green
    'bottom': [['O', 'B', 'R'], ['G', 'Y', 'O'], ['R', 'Y', 'B']],  # Down/yellow
    'left': [['W', 'Y', 'W'], ['W', 'O', 'R'], ['Y', 'Y', 'G']],  # Left/orange
    'right': [['Y', 'B', 'W'], ['Y', 'R', 'G'], ['R', 'B', 'G']],  # Right/red
    'back': [['G', 'G', 'O'], ['B', 'B', 'R'], ['B', 'G', 'G']]   # Back/blue
}
)

print(cube)
solver = ThistlethwaiteSolver(cube)
solution1 = solver.solve_phase(0)
solution2 = solver.solve_phase(1)
solution3 = solver.solve_phase(2)
solution4 = solver.solve_phase(3)
solution = solution1 + solution2 + solution3 + solution4
print(f"Solution moves1: {solution1}")
print(f"Solution moves2: {solution2}")
print(f"Solution moves3: {solution3}")
print(f"Solution moves4: {solution4}")