import itertools
from collections import deque
import numpy as np

# --- Corrected move tables for standard Rubik's Cube facelet model ---
# Facelet indices: U=0..8, R=9..17, F=18..26, D=27..35, L=36..44, B=45..53
# U (Up face 90° clockwise)
U = [
    6, 3, 0, 7, 4, 1, 8, 5, 2,  # U face rotates clockwise
    45, 46, 47, 12, 13, 14, 15, 16, 17,  # Front three cubies become right
    11, 10, 9, 21, 22, 23, 24, 25, 26,  # Right three cubies become back
    48, 49, 50, 30, 31, 32, 33, 34, 35,  # Back three cubies become left
    38, 37, 36, 39, 40, 41, 42, 43, 44,  # Left three cubies become front
    45, 46, 47, 48, 49, 50, 51, 52, 53
]

# U' (Up face 90° counterclockwise)
U_PRIME = [
    2, 5, 8, 1, 4, 7, 0, 3, 6,  # U face rotates counterclockwise
    38, 37, 36, 12, 13, 14, 15, 16, 17,  # Front three cubies become left
    20, 19, 18, 21, 22, 23, 24, 25, 26,  # Right three cubies become front
    48, 49, 50, 30, 31, 32, 33, 34, 35,  # Back three cubies become right
    45, 46, 47, 39, 40, 41, 42, 43, 44,  # Left three cubies become back
    45, 46, 47, 48, 49, 50, 51, 52, 53
]

# U2 (Up face 180°)
U2 = [8,7,6,5,4,3,2,1,0,  9,10,11,12,13,14,15,16,17,  18,19,20,21,22,23,24,25,26,  27,28,29,30,31,32,33,34,35,  36,37,38,39,40,41,42,43,44,  45,46,47,48,49,50,51,52,53]
# D (Down face 90° clockwise)
D = [
    0, 1, 2, 3, 4, 5, 6, 7, 8,  # U face stays
    9, 10, 11, 12, 13, 14, 24, 25, 26,  # R face: bottom row becomes front
    18, 19, 20, 21, 22, 23, 42, 43, 44,  # F face: bottom row becomes left
    33, 30, 27, 34, 31, 28, 35, 32, 29,  # D face rotates clockwise
    36, 37, 38, 39, 40, 41, 15, 16, 17,  # L face: bottom row becomes right
    45, 46, 47, 48, 49, 50, 51, 52, 53   # B face stays
]

# D' (Down face 90° counterclockwise)
D_PRIME = [
    0, 1, 2, 3, 4, 5, 6, 7, 8,  # U face stays
    9, 10, 11, 12, 13, 14, 42, 43, 44,  # R face: bottom row becomes left
    18, 19, 20, 21, 22, 23, 15, 16, 17,  # F face: bottom row becomes right
    29, 32, 35, 28, 31, 34, 27, 30, 33,  # D face rotates counterclockwise
    36, 37, 38, 39, 40, 41, 24, 25, 26,  # L face: bottom row becomes front
    45, 46, 47, 48, 49, 50, 51, 52, 53   # B face stays
]

# D2 (Down face 180°)
D2 = [0,1,2,3,4,5,6,7,8,  9,10,11,12,13,14,15,16,17,  18,19,20,21,22,23,24,25,26,  35,27,28,29,30,31,32,33,34,  36,37,38,39,40,41,42,43,44,  45,46,47,48,49,50,51,52,53]
L = [44,1,2,41,4,5,38,7,8,  9,10,11,12,13,14,15,16,17,  18,19,20,21,22,23,24,25,26,  27,28,29,30,31,32,33,34,35,  42,39,36,43,40,37,6,3,0,  45,46,47,48,49,50,51,52,53]
L_PRIME = [44,1,2,41,4,5,38,7,8,  9,10,11,12,13,14,15,16,17,  18,19,20,21,22,23,24,25,26,  27,28,29,30,31,32,33,34,35,  6,3,0,39,40,41,42,43,36,  45,46,47,48,49,50,51,52,53]
L2 = [38,1,2,44,4,5,42,7,8,  9,10,11,12,13,14,15,16,17,  18,19,20,21,22,23,24,25,26,  27,28,29,30,31,32,33,34,35,  36,39,42,37,40,43,44,41,38,  45,46,47,48,49,50,51,52,53]
# R (Right face 90° clockwise)
R = [
    0, 1, 20, 3, 4, 23, 6, 7, 26,  # U face: right column becomes front
    11, 14, 17, 10, 13, 16, 9, 12, 15,  # R face rotates clockwise
    18, 19, 51, 21, 22, 48, 24, 25, 45,  # F face: right column becomes back
    27, 28, 29, 30, 31, 32, 33, 34, 35,  # D face stays
    36, 37, 38, 39, 40, 41, 42, 43, 44,  # L face stays
    2, 46, 47, 5, 49, 50, 8, 52, 53   # B face: left column becomes up
]

# R' (Right face 90° counterclockwise)
R_PRIME = [
    0, 1, 45, 3, 4, 48, 6, 7, 51,  # U face: right column becomes back
    15, 12, 9, 16, 13, 10, 17, 14, 11,  # R face rotates counterclockwise
    18, 19, 2, 21, 22, 5, 24, 25, 8,  # F face: right column becomes up
    27, 28, 29, 30, 31, 32, 33, 34, 35,  # D face stays
    36, 37, 38, 39, 40, 41, 42, 43, 44,  # L face stays
    20, 46, 47, 23, 49, 50, 26, 52, 53   # B face: left column becomes front
]

# R2 (Right face 180°)
R2 = [0,1,2,3,4,5,6,7,8,  17,16,15,14,13,12,11,10,9,  18,19,20,21,22,23,24,25,26,  27,28,29,30,31,32,33,34,35,  36,37,38,39,40,41,42,43,44,  45,46,47,48,49,50,51,52,53]
# F (Front face 90° clockwise)
F = [
    0, 1, 2, 3, 4, 5, 42, 43, 44,  # U face: bottom row becomes left
    9, 10, 11, 12, 13, 14, 15, 16, 17,  # R face stays
    20, 23, 26, 19, 22, 25, 18, 21, 24,  # F face rotates clockwise
    6, 7, 8, 30, 31, 32, 33, 34, 35,  # D face: top row becomes right
    36, 37, 38, 39, 40, 41, 27, 28, 29,  # L face: right column becomes down
    45, 46, 47, 48, 49, 50, 51, 52, 53   # B face stays
]

# F' (Front face 90° counterclockwise)
F_PRIME = [
    0, 1, 2, 3, 4, 5, 27, 28, 29,  # U face: bottom row becomes down
    9, 10, 11, 12, 13, 14, 15, 16, 17,  # R face stays
    24, 21, 18, 25, 22, 19, 26, 23, 20,  # F face rotates counterclockwise
    42, 43, 44, 30, 31, 32, 33, 34, 35,  # D face: top row becomes left
    36, 37, 38, 39, 40, 41, 6, 7, 8,  # L face: right column becomes up
    45, 46, 47, 48, 49, 50, 51, 52, 53   # B face stays
]

# F2 (Front face 180°)
F2 = [
    0, 1, 2, 3, 4, 5, 29, 28, 27,  # U face
    9, 10, 11, 12, 13, 14, 15, 16, 17,  # R face unchanged
    26, 25, 24, 23, 22, 21, 20, 19, 18,  # F face rotated 180°
    44, 43, 42, 30, 31, 32, 33, 34, 35,  # D face: top corners swap with L corners
    36, 37, 38, 39, 40, 41, 8, 7, 6,     # L face: swap with U face corners
    45, 46, 47, 48, 49, 50, 51, 52, 53   # B face unchanged
]

# B (Back face 90° clockwise)
B = [
    44, 43, 42, 3, 4, 5, 6, 7, 8,  # U face: top row becomes right
    9, 10, 11, 12, 13, 14, 15, 16, 17,  # R face stays
    18, 19, 20, 21, 22, 23, 24, 25, 26,  # F face stays
    27, 28, 29, 30, 31, 32, 2, 1, 0,  # D face: bottom row becomes left
    36, 37, 38, 39, 40, 41, 42, 43, 44,  # L face stays
    47, 50, 53, 46, 49, 52, 45, 48, 51   # B face rotates clockwise
]

# B' (Back face 90° counterclockwise)
B_PRIME = [
    35, 34, 33, 3, 4, 5, 6, 7, 8,  # U face: top row becomes down
    9, 10, 11, 12, 13, 14, 15, 16, 17,  # R face stays
    18, 19, 20, 21, 22, 23, 24, 25, 26,  # F face stays
    27, 28, 29, 30, 31, 32, 44, 43, 42,  # D face: bottom row becomes right
    36, 37, 38, 39, 40, 41, 42, 43, 44,  # L face stays
    51, 48, 45, 52, 49, 46, 53, 50, 47   # B face rotates counterclockwise
]

# B2 (Back face 180°)
B2 = [
    35, 34, 33, 3, 4, 5, 6, 7, 8,        # U face: top corners swap with D corners
    9, 10, 11, 12, 13, 14, 15, 16, 17,   # R face unchanged 
    18, 19, 20, 21, 22, 23, 24, 25, 26,  # F face unchanged
    27, 28, 29, 30, 31, 32, 2, 1, 0,     # D face: bottom corners swap with U corners
    36, 37, 38, 39, 40, 41, 42, 43, 44,  # L face unchanged
    53, 52, 51, 50, 49, 48, 47, 46, 45   # B face rotated 180°
]
MOVE_TABLES = {
    'U': U,
    "U'": U_PRIME,
    'U2': U2,
    'D': D,
    "D'": D_PRIME,
    'D2': D2,
    'L': L,
    "L'": L_PRIME,
    'L2': L2,
    'R': R,
    "R'": R_PRIME,
    'R2': R2,
    'F': F,
    "F'": F_PRIME,
    'F2': F2,
    'B': B,
    "B'": B_PRIME,
    'B2': B2
}

# --- Phase move restrictions ---
PHASE_MOVES = [
    ["U", "U'", "U2", "R", "R'", "R2", "F", "F'", "F2", "D", "D'", "D2", "L", "L'", "L2", "B", "B'", "B2"], # Phase 1: all moves
    ["U", "U'", "U2", "R", "R'", "R2", "F2", "D", "D'", "D2", "L2", "B2"], # Phase 2: only half turns on F, L, B
    ["U", "U'", "U2", "R2", "F2", "D", "D'", "D2", "L2", "B2"], # Phase 3: only half turns on R, F, L, B
    ["U", "U'", "U2", "R2", "F2", "D", "D'", "D2", "L2", "B2"]  # Phase 4: same as phase 3
]

# --- Piece definitions for standard facelet mapping ---
# Edge positions: (U-F, U-R, U-B, U-L, D-F, D-R, D-B, D-L, F-R, F-L, B-R, B-L)
EDGE_POSITIONS = [
    (1, 19),   # UF
    (5, 10),   # UR
    (7, 46),   # UB
    (3, 37),   # UL
    (31, 25),  # DF
    (35, 16),  # DR
    (33, 50),  # DB
    (27, 43),  # DL
    (21, 12),  # FR
    (23, 41),  # FL
    (48, 14),  # BR
    (52, 39),  # BL
]
EDGE_COLORS = [
    ('U','F'), ('U','R'), ('U','B'), ('U','L'),
    ('D','F'), ('D','R'), ('D','B'), ('D','L'),
    ('F','R'), ('F','L'), ('B','R'), ('B','L')
]
# Corner positions (UFR, URB, UBL, ULF, DFR, DRB, DBL, DLF)
CORNER_POSITIONS = [
    (2, 9, 20),    # UFR: Up-Front-Right corner
    (8, 15, 45),   # URB: Up-Right-Back corner  
    (6, 47, 44),   # UBL: Up-Back-Left corner
    (0, 18, 38),   # ULF: Up-Left-Front corner
    (26, 35, 24),  # DFR: Down-Front-Right corner
    (32, 53, 17),  # DRB: Down-Right-Back corner
    (30, 51, 42),  # DBL: Down-Back-Left corner
    (28, 21, 36)   # DLF: Down-Left-Front corner
]

# Colors for each corner in the solved state
CORNER_COLORS = [
    ('U','R','F'), ('U','B','R'), ('U','L','B'), ('U','F','L'),
    ('D','R','F'), ('D','B','R'), ('D','L','B'), ('D','L','F')
]

def get_edge_permutation_and_orientation(state):
    """
    Returns a list of (piece_index, orientation) for each edge position.
    piece_index: which edge piece is in this position (0-11)
    orientation: 0 if oriented, 1 if flipped
    """
    result = [(None, None)] * 12  # Initialize empty result list
    used_pieces = set()
    
    # First pass: find unique matches
    for pos_idx, (pos, pos_colors) in enumerate(zip(EDGE_POSITIONS, EDGE_COLORS)):
        stickers = (state[pos[0]], state[pos[1]])
        for piece_idx, target_colors in enumerate(EDGE_COLORS):
            if piece_idx in used_pieces:
                continue
            # Check both orientations
            if stickers == target_colors:
                result[pos_idx] = (piece_idx, 0)
                used_pieces.add(piece_idx)
                break
            elif stickers == (target_colors[1], target_colors[0]):
                result[pos_idx] = (piece_idx, 1)
                used_pieces.add(piece_idx)
                break
    
    # Fill in any remaining positions with (-1, -1)
    for i in range(12):
        if result[i][0] is None:
            result[i] = (-1, -1)
            
    return result

def get_corner_permutation_and_orientation(state):
    """
    Returns a list of (piece_index, orientation) for each corner position.
    piece_index: which corner piece is in this position (0-7)
    orientation: 0=solved, 1=clockwise twist, 2=counterclockwise twist
    """
    result = []
    for pos_idx, (pos, target_colors) in enumerate(zip(CORNER_POSITIONS, CORNER_COLORS)):
        stickers = tuple(state[i] for i in pos)
        found = False
        
        for piece_idx, corner_colors in enumerate(CORNER_COLORS):
            # Try all possible orientations
            for orient in range(3):
                rotated_colors = corner_colors[orient:] + corner_colors[:orient]
                if set(stickers) == set(rotated_colors):
                    # Found matching corner, now determine orientation
                    if stickers == rotated_colors:
                        result.append((piece_idx, orient))
                        found = True
                        break
            if found:
                break
                
        if not found:
            # No matching corner found - should never happen in valid cube state
            result.append((-1, -1))
            
    return result

class RubiksCube:
    def __init__(self, state=None):
        self.solved_state = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
        self.state = state if state else self.solved_state

    def is_solved(self):
        return self.state == self.solved_state

    def apply_move(self, move):
        if move not in MOVE_TABLES:
            raise NotImplementedError(f"Move {move} not implemented in MOVE_TABLES.")
        perm = MOVE_TABLES[move]
        # Debug: check for out-of-range indices
        for idx in perm:
            if idx < 0 or idx > 53:
                print(f"Invalid index {idx} in move table for move {move}")
                print(f"Move table: {perm}")
                raise IndexError(f"Invalid index {idx} in move table for move {move}")
        if len(perm) != 54:
            print(f"Move table for {move} has incorrect length: {len(perm)}")
            print(f"Move table: {perm}")
            raise IndexError(f"Move table for {move} has incorrect length: {len(perm)}")
        self.state = ''.join(self.state[i] for i in perm)

    def copy(self):
        return RubiksCube(self.state)

    def generate_moves(self, allowed_moves):
        return allowed_moves

class ThistlethwaitesSolver:
    def __init__(self, cube):
        self.cube = cube

    def print_phase_debug(self, cube, phase):
        print(f"\n[DEBUG] After phase {phase}:")
        print(f"Cube state: {cube.state}")
        edges = get_edge_permutation_and_orientation(cube.state)
        corners = get_corner_permutation_and_orientation(cube.state)
        print(f"Edges (piece, orient): {edges}")
        print(f"Corners (piece, orient): {corners}")

    def solve(self):
        solution = []
        current_cube = self.cube.copy()
        for phase in range(4):
            print(f"Solving phase {phase+1}...")
            moves = self.solve_phase(current_cube, phase)
            for move in moves:
                current_cube.apply_move(move)
            solution += moves
            self.print_phase_debug(current_cube, phase+1)
        return solution

    def ida_star(self, start_cube, is_goal, allowed_moves, heuristic, max_depth=12):
        """
        IDA* search with improved bound handling and cycle detection
        """
        if is_goal(start_cube):
            return []

        # Start with the heuristic estimate
        bound = max(1, heuristic(start_cube))
        path = []
        
        while bound <= max_depth:
            print(f"[IDA*] Starting search with bound: {bound}, path so far: {' '.join(path)}")
            visited = set()  # Clear visited set for each bound
            result = self._ida_search(start_cube.copy(), 0, bound, path, is_goal, allowed_moves, heuristic, visited, max_depth)
            
            if result is True:
                return path
                
            if result == float('inf'):
                print(f"[IDA*] No solution found within bound {bound}")
                if bound >= max_depth:
                    print("[IDA*] Reached maximum depth limit")
                    return []
                bound += 1
                path.clear()  # Clear path for next iteration
                continue
                
            bound = result
        return []

    def _is_redundant_sequence(self, path, new_move):
        """Check if adding this move would create a redundant sequence"""
        if not path:
            return False
            
        last = path[-1]
        
        # Don't allow opposite moves
        if (new_move == "U" and last == "U'") or (new_move == "U'" and last == "U") or \
           (new_move == "D" and last == "D'") or (new_move == "D'" and last == "D") or \
           (new_move == "L" and last == "L'") or (new_move == "L'" and last == "L") or \
           (new_move == "R" and last == "R'") or (new_move == "R'" and last == "R") or \
           (new_move == "F" and last == "F'") or (new_move == "F'" and last == "F") or \
           (new_move == "B" and last == "B'") or (new_move == "B'" and last == "B"):
            return True
            
        # Don't allow sequences like U U or U U'
        if new_move[0] == last[0]:
            return True
            
        if len(path) >= 2:
            # Don't allow sequences that could be replaced by a single move
            # e.g., U D U can be replaced by U D'
            second_last = path[-2]
            if new_move[0] == second_last[0] and last[0] != new_move[0]:
                return True
                
        return False

    def _ida_search(self, node, g, bound, path, is_goal, allowed_moves, heuristic, visited, max_depth):
        """Recursive search with strict depth bound"""
        if g > bound:  # Changed from >= to > to allow reaching bound depth
            return float('inf')
            
        if is_goal(node):
            return True
            
        state_tuple = tuple(node.state)
        if state_tuple in visited:
            return float('inf')
            
        visited.add(state_tuple)
        
        # Try each allowed move
        for move in allowed_moves:
            if self._is_redundant_sequence(path, move):
                continue
                
            next_node = node.copy()
            next_node.apply_move(move)
            
            path.append(move)
            t = self._ida_search(next_node, g + 1, bound, path, is_goal, allowed_moves, heuristic, visited, max_depth)
            
            if t is True:
                return True
                
            path.pop()
            
        visited.remove(state_tuple)
        return float('inf')

    def solve_phase(self, cube, phase):
        """
        Solves a single phase of Thistlethwaite's algorithm with improved depth handling
        """
        allowed_moves = PHASE_MOVES[phase]
        is_phase_goal = self.get_phase_goal_checker(phase)
        heuristic = self.get_phase_heuristic(phase)
        
        # First check if already in goal state
        if is_phase_goal(cube):
            return []
            
        # Use a single increasing depth bound
        depth = 1
        while depth <= 12:  # Max reasonable depth for any phase
            print(f"Searching depth {depth} for phase {phase+1}...")
            path = []
            visited = set()
            result = self._ida_search(cube.copy(), 0, depth, path, is_phase_goal, allowed_moves, heuristic, visited, depth)
            
            if result is True:
                # Verify solution
                test_cube = cube.copy()
                for move in path:
                    test_cube.apply_move(move)
                if is_phase_goal(test_cube):
                    return path
                    
            depth += 1
            
        return []  # No solution found within depth limit

    def _all_corners_oriented_and_slice_group(self, cube):
        """Check if cube meets Phase 3 requirements"""
        # First check corner orientations
        corners = get_corner_permutation_and_orientation(cube.state)
        if not all(orient == 0 for _, orient in corners):
            return False
            
        # Then check E-slice preservation
        edges = get_edge_permutation_and_orientation(cube.state)
        e_slice = {8, 9, 10, 11}  # E-slice edge indices
        
        # Count pieces in and out of slice
        in_slice = 0
        out_of_slice = 0
        
        for idx, (piece, _) in enumerate(edges):
            if idx in e_slice:
                if piece in e_slice:
                    in_slice += 1
            elif piece in e_slice:
                out_of_slice += 1
                
        # All 4 E-slice edges should be in E-slice positions
        return in_slice == 4 and out_of_slice == 0

    def get_phase_goal_checker(self, phase):
        # Phase 1: All edges oriented
        def is_g1(cube):
            # Placeholder: implement edge orientation check
            # Return True if all 12 edges are oriented
            return self._all_edges_oriented(cube)
        # Phase 2: All edges in correct slice (M-slice)
        def is_g2(cube):
            """
            Returns True if and only if:
            - E-slice edges (FR, FL, BR, BL: indices 8,9,10,11) are in E-slice positions (8,9,10,11)
            - No E-slice edge is outside the E-slice positions
            - No non-E-slice edge is in an E-slice position
            """
            edges = get_edge_permutation_and_orientation(cube.state)
            # E-slice indices
            e_slice = {8, 9, 10, 11}
            for idx, (piece, _) in enumerate(edges):
                if idx in e_slice:
                    if piece not in e_slice:
                        return False  # Non-E-slice edge in E-slice position
                else:
                    if piece in e_slice:
                        return False  # E-slice edge outside E-slice
            return self._check_combined_parity(cube)
        # Phase 3: All corners oriented and E-slice group preserved
        def is_g3(cube):
            return self._all_corners_oriented_and_slice_group(cube) and self._check_combined_parity(cube)
        # Phase 4: Solved
        def is_g4(cube):
            return cube.is_solved()
        if phase == 0:
            return is_g1
        elif phase == 1:
            return is_g2
        elif phase == 2:
            return is_g3
        elif phase == 3:
            return is_g4
        else:
            return lambda cube: False

    def _validate_edge_orientation(self, cube):
        """
        Validate edge orientation and return number of flipped edges.
        An edge is properly oriented if:
        - U/D sticker is on U/D face for U/D edges
        - F/B sticker is on F/B face for E-slice edges
        """
        edges = get_edge_permutation_and_orientation(cube.state)
        flip_count = 0
        for idx, (piece, orient) in enumerate(edges):
            if piece == -1:
                return -1  # Invalid piece detected
            if idx < 4:  # U edges
                if orient != 0:
                    flip_count += 1
            elif idx < 8:  # D edges
                if orient != 0:
                    flip_count += 1
            else:  # E-slice edges
                if orient != 0:
                    flip_count += 1
        return flip_count

    def get_phase_heuristic(self, phase):
        if phase == 0:
            def h(cube):
                # Phase 1: Enhanced edge orientation heuristic with pattern matching
                edges = get_edge_permutation_and_orientation(cube.state)
                # Count basic flips
                flip_count = sum(1 for _, orient in edges if orient == 1)
                
                # Add penalty for bad edge patterns
                bad_patterns = 0
                # Check adjacent edges on each face
                faces = [(0,1,2,3), (4,5,6,7), (8,9,10,11)]  # U/D, F/B, M-slice
                for face in faces:
                    flipped_in_face = sum(1 for idx in face if edges[idx][1] == 1)
                    if flipped_in_face % 2 == 1:  # Odd number of flips can't be solved directly
                        bad_patterns += 1
                        
                if flip_count % 2 != 0:  # Must maintain even parity
                    flip_count += 1
                    
                return (flip_count + bad_patterns + 3) // 4
                
        elif phase == 1:
            def h(cube):
                edges = get_edge_permutation_and_orientation(cube.state)
                e_slice = {8, 9, 10, 11}
                misplaced = sum(1 for idx, (piece, _) in enumerate(edges) 
                              if (idx in e_slice) != (piece in e_slice))
                return (misplaced + 3) // 4
                
        elif phase == 2:
            def h(cube):
                corners = get_corner_permutation_and_orientation(cube.state)
                wrong_corners = sum(1 for _, orient in corners if orient != 0)
                edges = get_edge_permutation_and_orientation(cube.state)
                wrong_edges = sum(1 for idx, (piece, _) in enumerate(edges[8:12])
                                if piece not in {8, 9, 10, 11})
                return (wrong_corners + wrong_edges + 2) // 3
                
        else:
            def h(cube):
                if cube.is_solved():
                    return 0
                wrong = 0
                edges = get_edge_permutation_and_orientation(cube.state)
                corners = get_corner_permutation_and_orientation(cube.state)
                for idx, (piece, _) in enumerate(edges + corners):
                    if piece != idx:
                        wrong += 1
                return (wrong + 3) // 4
                
        return h

    # --- Phase goal helper functions ---
    def _all_edges_oriented(self, cube):
        """Check if all edges are properly oriented with valid parity"""
        edges = get_edge_permutation_and_orientation(cube.state)
        
        # Check orientations
        flip_count = 0
        for _, orient in edges:
            if orient == -1:  # Invalid piece
                return False
            flip_count += orient
        
        # Edge flip parity must be even
        if flip_count % 2 != 0:
            return False
            
        # All edges must be oriented
        return all(orient == 0 for _, orient in edges)

    def _all_edges_in_slice_group(self, cube):
        """
        Returns True if and only if:
        - E-slice edges (FR, FL, BR, BL: indices 8,9,10,11) are in E-slice positions (8,9,10,11)
        - No E-slice edge is outside the E-slice positions
        - No non-E-slice edge is in an E-slice position
        """
        edges = get_edge_permutation_and_orientation(cube.state)
        # E-slice indices
        e_slice = {8, 9, 10, 11}
        for idx, (piece, _) in enumerate(edges):
            if idx in e_slice:
                if piece not in e_slice:
                    return False  # Non-E-slice edge in E-slice position
            else:
                if piece in e_slice:
                    return False  # E-slice edge outside E-slice
        return True

    def _all_corners_oriented(self, cube):
        # Use piece-based orientation check
        corners = get_corner_permutation_and_orientation(cube.state)
        return all(orient == 0 for _, orient in corners)

    def _check_edge_parity(self, edges):
        """Check if edge permutation has valid parity"""
        # Count number of transpositions needed
        transpositions = 0
        visited = set()
        
        # Convert to piece locations
        edge_locs = [-1] * 12
        for pos, (piece, _) in enumerate(edges):
            if piece != -1:
                edge_locs[piece] = pos
        
        # Count cycle parities
        for start in range(12):
            if start not in visited and edge_locs[start] != -1:
                cycle_len = 0
                curr = start
                while curr not in visited:
                    visited.add(curr)
                    curr = edge_locs[curr]
                    cycle_len += 1
                transpositions += (cycle_len - 1)
                
        return transpositions % 2 == 0

    def _check_corner_parity(self, corners):
        """Check if corner permutation has valid parity"""
        # Similar to edge parity check
        transpositions = 0
        visited = set()
        
        # Convert to piece locations
        corner_locs = [-1] * 8
        for pos, (piece, _) in enumerate(corners):
            if piece != -1:
                corner_locs[piece] = pos
        
        # Count cycle parities
        for start in range(8):
            if start not in visited and corner_locs[start] != -1:
                cycle_len = 0
                curr = start
                while curr not in visited:
                    visited.add(curr)
                    curr = corner_locs[curr]
                    cycle_len += 1
                transpositions += (cycle_len - 1)
                
        return transpositions % 2 == 0

    def _check_combined_parity(self, cube):
        """Check if edge and corner permutations have matching parity"""
        edges = get_edge_permutation_and_orientation(cube.state)
        corners = get_corner_permutation_and_orientation(cube.state)
        edge_parity = self._check_edge_parity(edges)
        corner_parity = self._check_corner_parity(corners)
        return edge_parity == corner_parity  # Parities must match

# Main function to solve the cube

def test_move_tables():
    print("Testing all moves on solved state:")
    solved = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
    moves = [
        'U', "U'", 'U2', 'D', "D'", 'D2', 'L', "L'", 'L2',
        'R', "R'", 'R2', 'F', "F'", 'F2', 'B', "B'", 'B2'
    ]
    for move in moves:
        cube = RubiksCube(solved)
        cube.apply_move(move)
        print(f"After {move}: {cube.state}")
    print("Done.")

def main():
    cube = RubiksCube()
    # Use a single-move scramble for a quick test
    scramble = ["U", "R", "F", "D", "L", "B"]
    for move in scramble:
        cube.apply_move(move)
        print(f"After {move}: {cube.state}")
    print("Scrambled state:", cube.state)
    print("Phase 1 heuristic:", ThistlethwaitesSolver(cube).get_phase_heuristic(0)(cube))
    print("Phase 1 goal check:", ThistlethwaitesSolver(cube)._all_edges_oriented(cube))
    solver = ThistlethwaitesSolver(cube)
    solution = solver.solve()
    print("Solution:", " ".join(solution))
    # Apply solution to a fresh scrambled cube for verification
    verify_cube = RubiksCube()
    for move in scramble:
        verify_cube.apply_move(move)
    for move in solution:
        verify_cube.apply_move(move)
        print(f"After {move}: {verify_cube.state}")
    print("Cube solved?", verify_cube.is_solved())
    print("Expected solved state:", verify_cube.solved_state)
    print("Final state:", verify_cube.state)

def debug_phase_states(scramble_moves, solution_moves):
    cube = RubiksCube()
    for move in scramble_moves:
        cube.apply_move(move)
    print("\nState after scramble:", cube.state)
    phase = 1
    idx = 0
    for allowed, checker in zip(PHASE_MOVES, [solver.get_phase_goal_checker(i) for i in range(4)]):
        print(f"\n--- Phase {phase} ---")
        phase_moves = []
        while idx < len(solution_moves):
            move = solution_moves[idx]
            if move not in allowed:
                break
            cube.apply_move(move)
            phase_moves.append(move)
            idx += 1
            if checker(cube):
                break
        print(f"After phase {phase} moves ({' '.join(phase_moves)}): {cube.state}")
        phase += 1
    print("\nFinal state after all phases:", cube.state)
    print("Solved?", cube.is_solved())

if __name__ == "__main__":
    test_move_tables()
    print("\n--- Now running main solver test ---\n")
    main()
    cube = RubiksCube()
    # Debug phase-by-phase state
    scramble = ["U"] 
    for move in scramble:
        cube.apply_move(move)
    
    solver = ThistlethwaitesSolver(cube)
    solution = solver.solve()
    debug_phase_states(scramble, solution)