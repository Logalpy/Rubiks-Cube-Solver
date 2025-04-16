from Thistlethwaites import ThistlethwaiteSolver
from cube import RubiksCube

def debug_phase1():
    # Create a solved cube
    cube = RubiksCube()
    solver = ThistlethwaiteSolver(cube)
    
    print("Initial solved cube state:")
    print(cube)
    print(f"Phase 1 state (should be True for solved): {solver.get_phase1_state()}")
    
    print("\nApplying R U (should disorient corners):")
    cube.move("R")
    cube.move("U")
    print(cube)
    print(f"Phase 1 state after R U (should be False): {solver.get_phase1_state()}")
    
    print("\nTrying to solve Phase 1:")
    solution = solver.solve_phase(1)
    print(f"Solution moves: {solution}")
    
    print("\nFinal cube state:")
    print(cube)
    print(f"Final Phase 1 state (should be True): {solver.get_phase1_state()}")
    
    # Debug corner orientation
    print("\nDebug corner orientation:")
    corners = [
        ("U", (0,0), "L", (0,0), "B", (0,2), "ULB"),  # ULB corner
        ("U", (0,2), "B", (0,0), "R", (0,2), "UBR"),  # UBR corner
        ("U", (2,0), "F", (0,0), "L", (0,2), "UFL"),  # UFL corner
        ("U", (2,2), "R", (0,0), "F", (0,2), "URF"),  # URF corner
        ("D", (0,0), "F", (2,0), "L", (2,2), "DFL"),  # DFL corner
        ("D", (0,2), "R", (2,0), "F", (2,2), "DRF"),  # DRF corner
        ("D", (2,0), "L", (2,0), "B", (2,2), "DLB"),  # DLB corner
        ("D", (2,2), "B", (2,0), "R", (2,2), "DBR"),  # DBR corner
    ]
    
    for corner in corners:
        f1, p1, f2, p2, f3, p3, name = corner
        sticker1 = cube.faces[f1][p1[0]][p1[1]]
        sticker2 = cube.faces[f2][p2[0]][p2[1]]
        sticker3 = cube.faces[f3][p3[0]][p3[1]]
        print(f"{name} corner: {sticker1}-{sticker2}-{sticker3}")

if __name__ == "__main__":
    debug_phase1()