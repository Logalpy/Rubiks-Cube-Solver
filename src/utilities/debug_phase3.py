from Thistlethwaites import ThistlethwaiteSolver
from cube import RubiksCube

def debug_phase3():
    # Create a solved cube
    cube = RubiksCube()
    solver = ThistlethwaiteSolver(cube)
    
    print("Initial solved cube state:")
    print(cube)
    print(f"Phase 3 state (should be True for solved): {solver.get_phase3_state()}")
    
    print("\nApplying some half turns to scramble the cube:")
    # Apply a sequence of half turns to scramble the cube while maintaining Phase 2
    cube.move("U2")
    cube.move("R2")
    cube.move("F2")
    print(cube)
    print(f"Phase 3 state after moves (should be False): {solver.get_phase3_state()}")
    
    print("\nTrying to solve Phase 3:")
    solution = solver.solve_phase(3)
    print(f"Solution moves: {solution}")
    
    print("\nFinal cube state:")
    print(cube)
    print(f"Final Phase 3 state (should be True): {solver.get_phase3_state()}")
    
    # Debug cube state
    print("\nDebug cube state:")
    print(cube)

if __name__ == "__main__":
    debug_phase3()