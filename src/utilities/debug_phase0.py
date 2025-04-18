import unittest
from cube import RubiksCube
from Thistlethwaites import ThistlethwaiteSolver

class TestPhase0(unittest.TestCase):
    def setUp(self):
        self.cube = RubiksCube()
        self.solver = ThistlethwaiteSolver(self.cube)

    def test_solved_cube_phase0(self):
        """A solved cube should pass phase 0"""
        self.assertTrue(self.solver.get_phase0_state())

    def test_single_edge_flip(self):
        """Test with a single flipped edge"""
        # Perform R U R' U' to flip the UF edge
        moves = ["R", "U", "R'", "U'"]
        for move in moves:
            self.cube.move(move)
        self.assertFalse(self.solver.get_phase0_state())

    def test_two_edge_flip(self):
        """Test with two flipped edges"""
        # Perform M' U M U to flip UF and UB edges
        moves = ["M'", "U", "M", "U"]
        for move in moves:
            self.cube.move(move)
        self.assertFalse(self.solver.get_phase0_state())

    def test_phase0_solve(self):
        
        moves = ["R", "U", "R'", "U'"]
        for move in moves:
            self.cube.move(move)
        solution = self.solver.solve_phase(0)
        print("Phase 0 solution:", solution)
        self.assertTrue(self.solver.get_phase0_state())
        print(solution)

if __name__ == '__main__':
    unittest.main()