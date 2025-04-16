from Thistlethwaites import ThistlethwaiteSolver
from cube import RubiksCube

def test_scramble(cube, solver, scramble, name=""):
    print(f"\n=== Testing {name if name else 'scramble'}: {scramble} ===")
    print("Initial cube state:")
    print(cube)
    print(f"Phase 0 state before scramble: {solver.get_phase0_state()}")
    
    # Apply scramble
    for move in scramble.split():
        cube.move(move)
    
    print("\nCube state after scramble:")
    print(cube)
    print(f"Phase 0 state after scramble: {solver.get_phase0_state()}")
    
    print("\nTrying to solve Phase 0:")
    solution = solver.solve_phase(0)
    if isinstance(solution, list):
        solution_str = ' '.join(solution)
        solution_len = len(solution)
    else:
        solution_str = solution
        solution_len = len(solution.split())
    
    print(f"Solution moves: {solution_str}")
    print(f"Solution length: {solution_len}")
    
    print("\nFinal cube state:")
    print(cube)
    print(f"Final Phase 0 state: {solver.get_phase0_state()}\n")
    print("-" * 50)

def debug_phase0():
    # Create a solved cube
    cube = RubiksCube()
    solver = ThistlethwaiteSolver(cube)
    
    # Test cases with different complexities
    scrambles = [
        ("Simple F move", "F"),
        ("Medium scramble", "F R U B"),
        ("Complex scramble", "F R U R' U' F' R U R' U' R U R'"),
        ("Very complex scramble", "F R U R' U' F' B L B' R B L' B' R'"),
        ("Super complex scramble", "R U R' U R U2 R' F R U R' U' F' U2 B U2 B'")
    ]
    
    for name, scramble in scrambles:
        try:
            # Reset cube to solved state for each test
            cube = RubiksCube()
            solver = ThistlethwaiteSolver(cube)
            test_scramble(cube, solver, scramble, name)
        except Exception as e:
            print(f"Error testing {name}: {str(e)}")
            continue
    
    # Debug edge orientation detection for the last scramble state
    print("\nFinal edge orientation detection:")
    edges = [
        ("U", (0,1), "B", (0,1), "UB"),  # UB edge
        ("U", (1,2), "R", (0,1), "UR"),  # UR edge
        ("U", (2,1), "F", (0,1), "UF"),  # UF edge
        ("U", (1,0), "L", (0,1), "UL"),  # UL edge
        ("F", (0,1), "U", (2,1), "FU"),  # FU edge
        ("F", (1,2), "R", (1,0), "FR"),  # FR edge
        ("F", (2,1), "D", (0,1), "FD"),  # FD edge
        ("F", (1,0), "L", (1,2), "FL"),  # FL edge
    ]
    
    for edge in edges:
        f1, pos1, f2, pos2, name = edge
        sticker1 = cube.faces[f1][pos1[0]][pos1[1]]
        sticker2 = cube.faces[f2][pos2[0]][pos2[1]]
        print(f"{name} edge: {sticker1}-{sticker2}")

if __name__ == "__main__":
    debug_phase0()