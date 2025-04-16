from Thistlethwaites import ThistlethwaiteSolver
from cube import RubiksCube

def debug_phase2():
    # Create a solved cube
    cube = RubiksCube()
    solver = ThistlethwaiteSolver(cube)
    
    print("Initial solved cube state:")
    print(cube)
    print(f"Phase 2 state (should be True for solved): {solver.get_phase2_state()}")
    
    print("\nApplying M E S (middle layer slice moves) to misalign edges:")
    # Simulate middle layer disruption with moves
    cube.move("R")
    cube.move("U")
    cube.move("R'")  # This sequence will put some edges out of their proper slice
    print(cube)
    print(f"Phase 2 state after moves (should be False): {solver.get_phase2_state()}")
    
    print("\nTrying to solve Phase 2:")
    solution = solver.solve_phase(2)
    print(f"Solution moves: {solution}")
    
    print("\nFinal cube state:")
    print(cube)
    print(f"Final Phase 2 state (should be True): {solver.get_phase2_state()}")
    
    # Debug edge positions
    print("\nDebug edge positions:")
    edges = [
        # E slice edges (middle layer)
        ("F", (1,0), "L", (1,2), "FL"),  # Front-Left
        ("F", (1,2), "R", (1,0), "FR"),  # Front-Right
        ("B", (1,0), "L", (1,0), "BL"),  # Back-Left
        ("B", (1,2), "R", (1,2), "BR"),  # Back-Right
        
        # M slice edges
        ("U", (1,0), "L", (0,1), "UL"),  # Up-Left
        ("D", (1,0), "L", (2,1), "DL"),  # Down-Left
        ("U", (1,2), "R", (0,1), "UR"),  # Up-Right
        ("D", (1,2), "R", (2,1), "DR"),  # Down-Right
        
        # S slice edges
        ("U", (2,1), "F", (0,1), "UF"),  # Up-Front
        ("D", (0,1), "F", (2,1), "DF"),  # Down-Front
        ("U", (0,1), "B", (0,1), "UB"),  # Up-Back
        ("D", (2,1), "B", (2,1), "DB"),  # Down-Back
    ]
    
    for edge in edges:
        f1, p1, f2, p2, name = edge
        sticker1 = cube.faces[f1][p1[0]][p1[1]]
        sticker2 = cube.faces[f2][p2[0]][p2[1]]
        print(f"{name} edge: {sticker1}-{sticker2}")

if __name__ == "__main__":
    debug_phase2()