import unittest
import sys
import os
# Add the utilities directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from cube import RubiksCube
from Thistlethwaites import ThistlethwaiteSolver

class TestThistlethwaiteSolver(unittest.TestCase):
    def setUp(self):
        self.cube = RubiksCube()
        self.solver = ThistlethwaiteSolver(self.cube)

    def test_phase0_already_solved(self):
        """Test that a solved cube passes phase 0"""
        self.assertTrue(self.solver.get_phase0_state())
        
    def test_phase0_edge_orientation(self):
        """Test phase 0 with a scramble that only affects edge orientation"""
        # This scramble specifically disorients multiple edges
        scramble = ["F", "F", "B", "B"]  # Guaranteed to disorient edges
        self.verify_scramble_state(scramble)
        
        # Initial state should fail phase 0
        self.assertFalse(self.solver.get_phase0_state(), "Scramble should create bad edge orientations")
        
        # Solve phase 0
        solution = self.solver.solve_phase(0)
        
        # Verify phase 0 is solved
        self.assertTrue(self.solver.get_phase0_state(), "Edge orientation should be fixed")
        print(f"Phase 0 solution for edge orientation: {' '.join(solution)}")
        
    def test_phase0_difficult_case(self):
        """Test phase 0 with a more complex scramble"""
        # This scramble creates multiple bad edge orientations
        scramble = ["F", "F", "R", "F", "L", "F"]  # Multiple F moves guarantee bad orientations
        self.verify_scramble_state(scramble)
        
        # Initial state should fail phase 0
        self.assertFalse(self.solver.get_phase0_state(), "Complex scramble should create bad edge orientations")
        
        # Solve phase 0
        solution = self.solver.solve_phase(0)
        
        # Verify phase 0 is solved
        self.assertTrue(self.solver.get_phase0_state(), "Edge orientation should be fixed")
        print(f"Phase 0 solution for complex case: {' '.join(solution)}")
        
    def test_phase0_specific_edges(self):
        """Test phase 0 with specific edges misoriented"""
        # Create a case with exactly four edges misoriented (guaranteed to be possible to solve)
        scramble = ["F", "F"]  # Disorients exactly four edges
        self.verify_scramble_state(scramble)
        
        # Initial state should fail phase 0
        self.assertFalse(self.solver.get_phase0_state(), "Should have exactly four misoriented edges")
        
        # Solve phase 0
        solution = self.solver.solve_phase(0)
        
        # Verify phase 0 is solved
        self.assertTrue(self.solver.get_phase0_state(), "Edge orientation should be fixed")
        print(f"Phase 0 solution for specific edges: {' '.join(solution)}")

    def test_phase0_solution_length(self):
        """Test that phase 0 solutions don't exceed the theoretical maximum"""
        # Complex scramble designed to create maximum edge orientation issues
        scramble = ["F", "F", "B", "B", "L", "L", "R", "R"]
        self.verify_scramble_state(scramble)
        
        # Should be in a bad state
        self.assertFalse(self.solver.get_phase0_state(), "Should have maximum misoriented edges")
        
        # Solve phase 0
        solution = self.solver.solve_phase(0)
        
        # Verify solution length is within theoretical maximum (12 moves)
        self.assertLessEqual(len(solution), 12, "Solution should not exceed 12 moves")
        self.assertTrue(self.solver.get_phase0_state(), "Edge orientation should be fixed")
        print(f"Phase 0 solution length: {len(solution)} moves")
        print(f"Solution: {' '.join(solution)}")

    def test_phase1_corner_orientation(self):
        """Test phase 1 with a scramble that twists corners"""
        scramble = ["R", "U", "R'", "U", "R", "U2", "R'"]  # Sune, twists corners
        self.verify_scramble_state(scramble)
        self.assertFalse(self.solver.get_phase1_state(), "Scramble should create bad corner orientations")
        solution = self.solver.solve_phase(1)
        self.assertTrue(self.solver.get_phase1_state(), "Corner orientation should be fixed")
        print(f"Phase 1 solution: {' '.join(solution)}")

    def test_phase2_edge_slices(self):
        """Test phase 2 with a scramble that puts edges in the wrong slices"""
        scramble = ["R", "U", "R'", "U", "R", "U2", "R'", "F", "R", "U", "R'", "U", "R", "U2", "R'"]
        self.verify_scramble_state(scramble)
        self.assertFalse(self.solver.get_phase2_state(), "Scramble should create bad edge slices")
        solution = self.solver.solve_phase(2)
        self.assertTrue(self.solver.get_phase2_state(), "Edge slices should be fixed")
        print(f"Phase 2 solution: {' '.join(solution)}")

    def test_phase3_final_solve(self):
        """Test phase 3 with a scramble that permutes pieces but leaves orientation solved"""
        scramble = ["U2", "R2", "F2", "D2", "L2", "B2"]  # Only half turns, so orientation is preserved
        self.verify_scramble_state(scramble)
        self.assertFalse(self.solver.get_phase3_state(), "Scramble should leave cube unsolved for phase 3")
        solution = self.solver.solve_phase(3)
        self.assertTrue(self.solver.get_phase3_state(), "Cube should be fully solved after phase 3")
        print(f"Phase 3 solution: {' '.join(solution)}")

    def test_phase3_idempotence(self):
        """Test that applying a phase 3 solution to a solved cube keeps it solved (idempotence)."""
        # Use a solved cube
        solved_cube = RubiksCube()
        solver = ThistlethwaiteSolver(solved_cube)
        # Example phase 3 solution (should be identity for solved cube)
        phase3_moves = ["U2", "D2", "L2", "R2", "F2", "B2", "U2", "D2", "L2", "R2", "F2", "B2"]
        for move in phase3_moves:
            solved_cube.move(move)
        # After applying phase 3 moves, cube should still be solved
        self.assertTrue(solver.get_phase3_state(), "Cube should remain solved after phase 3 moves applied to solved cube")
        print("Phase 3 idempotence test passed.")

    def verify_scramble_state(self, scramble):
        """Helper method to apply scramble and print cube state"""
        print(f"\nApplying scramble: {' '.join(scramble)}")
        for move in scramble:
            self.cube.move(move)
        print("\nCube state after scramble:")
        print(self.cube)

def test_simple():
    # Create a cube and scramble it with a simple case
    cube = RubiksCube()
    solver = ThistlethwaiteSolver(cube)
    
    # Initial state should be solved
    assert solver.get_phase0_state(), "Initial state should be solved"
    print("\nInitial state:")
    print(cube)
    
    # Apply F move which disorients 4 edges
    cube.move("F")
    print("\nAfter F move:")
    print(cube)
    
    # Check that edges are now disoriented
    assert not solver.get_phase0_state(), "F move should disorient edges"
    
    # Solve phase 0
    solution = solver.solve_phase(0)
    print(f"\nPhase 0 solution: {' '.join(solution)}")
    
    # Verify solution
    assert solver.get_phase0_state(), "Solution should fix edge orientations"
    print("\nFinal state:")
    print(cube)

if __name__ == '__main__':
    unittest.main(verbosity=2)
    test_simple()

def test_phase0():
    # Create a solved cube first
    cube = RubiksCube()
    solver = ThistlethwaiteSolver(cube)
    
    # Test 1: A solved cube should pass phase 0
    print("Test 1: Solved cube")
    phase0_state = solver.get_phase0_state()
    print(f"Phase 0 state (should be False for solved cube): {phase0_state}")
    
    # Test 2: Apply moves that should misalign edges
    print("\nTest 2: Misaligned edges")
    # F move misaligns UF and DF edges
    cube.move("F")
    phase0_state = solver.get_phase0_state()
    print(f"After F move - Phase 0 state (should be True for bad edges): {phase0_state}")
    
    # Test 3: Try to solve Phase 0
    print("\nTest 3: Solving Phase 0")
    solution = solver.solve_phase(0)
    print(f"Solution moves: {solution}")
    
    # Check if the solution fixed the edge orientation
    final_state = solver.get_phase0_state()
    print(f"Final Phase 0 state (should be False for correct edges): {final_state}")

if __name__ == "__main__":
    test_phase0()

def test_full_solve():
    # Create a solved cube
    cube = RubiksCube()
    solver = ThistlethwaiteSolver(cube)
    
    print("\nInitial solved cube state:")
    print(cube)
    
    # Apply a complex scramble that affects all aspects (edge orientation, corner orientation, and slice positions)
    scramble = ["R", "U", "F", "L", "D'", "B", "R'", "U2"]
    print("\nApplying scramble:", " ".join(scramble))
    for move in scramble:
        cube.move(move)
    print("\nScrambled cube state:")
    print(cube)
    
    # Test Phase 0 (Edge Orientation)
    print("\n=== Phase 0: Edge Orientation ===")
    print(f"Initial Phase 0 state: {solver.get_phase0_state()}")
    phase0_solution = solver.solve_phase(0)
    print(f"Phase 0 solution: {phase0_solution}")
    print("\nCube state after Phase 0:")
    print(cube)
    print(f"Phase 0 complete: {solver.get_phase0_state()}")
    
    # Test Phase 1 (Corner Orientation)
    print("\n=== Phase 1: Corner Orientation ===")
    print(f"Initial Phase 1 state: {solver.get_phase1_state()}")
    phase1_solution = solver.solve_phase(1)
    print(f"Phase 1 solution: {phase1_solution}")
    print("\nCube state after Phase 1:")
    print(cube)
    print(f"Phase 1 complete: {solver.get_phase1_state()}")
    
    # Test Phase 2 (Edge Slices)
    print("\n=== Phase 2: Edge Slices ===")
    print(f"Initial Phase 2 state: {solver.get_phase2_state()}")
    phase2_solution = solver.solve_phase(2)
    print(f"Phase 2 solution: {phase2_solution}")
    print("\nCube state after Phase 2:")
    print(cube)
    print(f"Phase 2 complete: {solver.get_phase2_state()}")
    
    # Test Phase 3 (Complete with Half Turns)
    print("\n=== Phase 3: Final Solve ===")
    print(f"Initial Phase 3 state: {solver.get_phase3_state()}")
    phase3_solution = solver.solve_phase(3)
    print(f"Phase 3 solution: {phase3_solution}")
    print("\nFinal cube state:")
    print(cube)
    print(f"Phase 3 complete: {solver.get_phase3_state()}")
    
    # Print complete solution
    total_moves = phase0_solution + phase1_solution + phase2_solution + phase3_solution
    print("\nComplete solution:", " ".join(total_moves))
    print(f"Total moves: {len(total_moves)}")
    
    # Verify final state
    print("\nVerifying final state:")
    print("All phases complete:", all([
        solver.get_phase0_state(),
        solver.get_phase1_state(),
        solver.get_phase2_state(),
        solver.get_phase3_state()
    ]))
    
    # Debug final face colors
    print("\nFinal face colors:")
    faces = ['U', 'D', 'F', 'B', 'L', 'R']
    for face in faces:
        print(f"{face} face:")
        for row in cube.faces[face]:
            print(''.join(row))

if __name__ == "__main__":
    test_full_solve()

def test_phase3_specific():
    """Test Phase 3 with specific test cases"""
    cube = RubiksCube()
    solver = ThistlethwaiteSolver(cube)

    # Test Case 1: Cube with only U/D layer rotations
    print("\nTest Case 1: U/D layer rotations")
    test_scramble = ["U", "D'", "U'", "D"]
    for move in test_scramble:
        cube.move(move)
    solution = solver.solve_phase(3)
    print(f"Scramble: {' '.join(test_scramble)}")
    print(f"Solution: {' '.join(solution)}")
    assert solver.get_phase3_state(), "Cube should be solved"

    # Test Case 2: H-Permutation
    print("\nTest Case 2: H-Permutation")
    h_perm = ["R2", "U2", "R", "U2", "R2", "U2", "R2", "U2", "R", "U2", "R2"]
    for move in h_perm:
        cube.move(move)
    solution = solver.solve_phase(3)
    print(f"Scramble: {' '.join(h_perm)}")
    print(f"Solution: {' '.join(solution)}")
    assert solver.get_phase3_state(), "Cube should be solved"

    # Test Case 3: Double-layer turns
    print("\nTest Case 3: Double-layer turns")
    double_turns = ["U2", "D2", "R2", "L2", "F2", "B2"]
    for move in double_turns:
        cube.move(move)
    solution = solver.solve_phase(3)
    print(f"Scramble: {' '.join(double_turns)}")
    print(f"Solution: {' '.join(solution)}")
    assert solver.get_phase3_state(), "Cube should be solved"

if __name__ == "__main__":
    test_phase3_specific()
