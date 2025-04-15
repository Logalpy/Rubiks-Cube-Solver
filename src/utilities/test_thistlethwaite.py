import unittest
from Thistlethwaites import ThistlethwaitesSolver, RubiksCube

class TestThistlethwaitePhaseCheckers(unittest.TestCase):
    def setUp(self):
        self.solver = ThistlethwaitesSolver(RubiksCube())

    def test_all_edges_oriented(self):
        # Solved state: all edges oriented
        solved_state = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
        cube = RubiksCube(solved_state)
        self.assertTrue(self.solver._all_edges_oriented(cube))
        # One edge flipped: flip UF edge (swap U1 and F19)
        flipped = list(solved_state)
        flipped[1], flipped[19] = flipped[19], flipped[1]
        flipped_state = ''.join(flipped)
        cube = RubiksCube(flipped_state)
        self.assertFalse(self.solver._all_edges_oriented(cube))

    def test_all_edges_in_slice_group(self):
        # Solved state: E-slice edges in E-slice positions
        solved_state = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
        cube = RubiksCube(solved_state)
        self.assertTrue(self.solver._all_edges_in_slice_group(cube))
        # Swap FR (E-slice) with UF (not E-slice)
        swapped = list(solved_state)
        # FR: 21,12; UF: 1,19
        swapped[21], swapped[1] = swapped[1], swapped[21]
        swapped[12], swapped[19] = swapped[19], swapped[12]
        not_in_slice_state = ''.join(swapped)
        cube = RubiksCube(not_in_slice_state)
        self.assertFalse(self.solver._all_edges_in_slice_group(cube))

    def test_all_corners_oriented(self):
        # Solved state: all corners oriented
        solved_state = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
        cube = RubiksCube(solved_state)
        self.assertTrue(self.solver._all_corners_oriented(cube))
        # Twist UFR corner (positions 2,9,18)
        twisted = list(solved_state)
        twisted[2], twisted[9], twisted[18] = twisted[9], twisted[18], twisted[2]
        twisted_state = ''.join(twisted)
        cube = RubiksCube(twisted_state)
        self.assertFalse(self.solver._all_corners_oriented(cube))

if __name__ == '__main__':
    unittest.main()
