from utilities.cube import RubiksCube

class ThistlethwaiteSolver:
    def __init__(self, cube: RubiksCube):
        self.cube = cube if cube else RubiksCube()
        self.SLICE_MOVE_THRESHOLD = 45
        # Define standard face colors
        self.face_colors = {'U': 'W', 'D': 'Y', 'F': 'G', 'B': 'B', 'L': 'O', 'R': 'R'}
        # Define move groups for each phase
        self.phase_moves = [
            # Phase 0: Any move (including slice moves for full edge orientation)
            ["U", "U'", "U2", "D", "D'", "D2", 
             "L", "L'", "L2", "R", "R'", "R2", 
             "F", "F'", "F2", "B", "B'", "B2",
             "M", "M'", "M2","E","E'","E2","S","S'","S2"],  # Added slice moves for Phase 0
            
            # Phase 1: Quarter turns of U/D, half turns of others
            ["U", "U'", "U2", "D", "D'", "D2", 
             "R2", "L2", "F2", "B2"],
            
            # Phase 2: All moves needed to fix R U R' case
            # After R U R', we need either U' R' to undo or R U to complete
            ["R", "R'", "U", "U'",  # Quarter turns needed to fix the case
             "R2", "U2", "D2",      # Half turns for general edge slice positioning
             "F2", "B2", "L2"],     # Additional half turns if needed
            
            # Phase 3: Allow quarter turns of U/D and half turns of others
            # Include more moves to handle parity cases
            ["U", "U'", "U2", "D", "D'", "D2",  # U/D moves
             "R2", "L2", "F2", "B2",            # Half turns
             "M2", "E2", "S2"]                  # Slice moves for parity
        ]
        
    def get_phase0_state(self):
        """
        Check edge orientations according to Thistlethwaite's rules:
        1. For edges with U/D color (W/Y): oriented if the W/Y sticker is on a U/D face
        2. For edges without U/D color: oriented if the F/B color (G/B) is on an F/B face
        """
        edges = [
            # Top layer edges
            ('U', (0, 1), 'B', (0, 1)),  # UB
            ('U', (1, 2), 'R', (0, 1)),  # UR 
            ('U', (2, 1), 'F', (0, 1)),  # UF
            ('U', (1, 0), 'L', (0, 1)),  # UL
            # Middle layer edges
            ('F', (1, 0), 'L', (1, 2)),  # FL
            ('F', (1, 2), 'R', (1, 0)),  # FR
            ('B', (1, 0), 'L', (1, 0)),  # BL
            ('B', (1, 2), 'R', (1, 2)),  # BR
            # Bottom layer edges
            ('D', (0, 1), 'F', (2, 1)),  # DF
            ('D', (1, 2), 'R', (2, 1)),  # DR
            ('D', (2, 1), 'B', (2, 1)),  # DB
            ('D', (1, 0), 'L', (2, 1)),  # DL
        ]

        misoriented = 0
        for f1, pos1, f2, pos2 in edges:
            s1 = self.cube.faces[f1][pos1[0]][pos1[1]]
            s2 = self.cube.faces[f2][pos2[0]][pos2[1]]
            # Determine the colors of the stickers
            stickers = [s1, s2]
            faces = [f1, f2]
            # Check if this edge has a U/D color (W/Y)
            if 'W' in stickers or 'Y' in stickers:
                # Find which sticker is W/Y
                if s1 in ['W', 'Y']:
                    is_oriented = f1 in ['U', 'D']
                else:
                    is_oriented = f2 in ['U', 'D']
                if not is_oriented:
                    print(f"Misoriented U/D edge: {f1}({pos1[0]}, {pos1[1]})-{f2}({pos2[0]}, {pos2[1]}) with stickers {s1}-{s2}")
                    misoriented += 1
            else:
                # No U/D color, check if G/B is on F/B face
                if s1 in ['G', 'B']:
                    is_oriented = f1 in ['F', 'B']
                elif s2 in ['G', 'B']:
                    is_oriented = f2 in ['F', 'B']
                else:
                    # Edge with only L/R colors is always oriented
                    is_oriented = True
                if not is_oriented:
                    print(f"Misoriented F/B edge: {f1}({pos1[0]}, {pos1[1]})-{f2}({pos2[0]}, {pos2[1]}) with stickers {s1}-{s2}")
                    misoriented += 1
        print(f"Total misoriented edges in Phase 0: {misoriented}")
        return misoriented == 0

    def get_phase1_state(self):
        """Check corner orientation - all corners must be oriented correctly.
        In Phase 1, corners are correctly oriented when their U/D colored sticker
        is on the U or D face."""
        corners = [
            # Format: (face, i, j, adjacent_faces_and_positions)
            ('U', 0, 0, [('L', 0, 0), ('B', 0, 2)]),  # ULB
            ('U', 0, 2, [('B', 0, 0), ('R', 0, 2)]),  # UBR
            ('U', 2, 0, [('F', 0, 0), ('L', 0, 2)]),  # UFL
            ('U', 2, 2, [('R', 0, 0), ('F', 0, 2)]),  # URF
            ('D', 0, 0, [('F', 2, 0), ('L', 2, 2)]),  # DFL
            ('D', 0, 2, [('R', 2, 0), ('F', 2, 2)]),  # DRF
            ('D', 2, 0, [('B', 2, 2), ('L', 2, 0)]),  # DLB
            ('D', 2, 2, [('R', 2, 2), ('B', 2, 0)]),  # DBR
        ]
        
        misoriented = 0
        for face, i, j, adj_positions in corners:
            stickers = [self.cube.faces[face][i][j]]
            for f, x, y in adj_positions:
                stickers.append(self.cube.faces[f][x][y])
            
            ud_sticker_found = False
            for idx, sticker in enumerate(stickers):
                if sticker in ['W', 'Y']:
                    ud_sticker_found = True
                    if idx != 0:  # U/D sticker not on U/D face
                        misoriented += 1
                        print(f"Misoriented corner: {face}[{i},{j}] with stickers {stickers}")
                    break  # Stop after first U/D sticker
            if not ud_sticker_found:
                misoriented += 1
                print(f"No U/D sticker found on corner: {face}[{i},{j}] with stickers {stickers}")
        
        print(f"Total misoriented corners: {misoriented}")
        return misoriented == 0

    def get_phase2_state(self):
        """Check edge positions - edges must be in their correct slice.
        In Phase 2:
        - E slice edges (middle layer) must only have F/B/L/R colors
        - M slice edges must have at least one U/D color
        - S slice edges must have at least one U/D color"""
        def check_edge_colors(face1, pos1, face2, pos2, allowed_colors, label):
            sticker1 = self.cube.faces[face1][pos1[0]][pos1[1]]
            sticker2 = self.cube.faces[face2][pos2[0]][pos2[1]]
            if not set([sticker1, sticker2]).issubset(set(allowed_colors)):
                print(f"Misoriented {label} edge: {face1}{pos1}-{face2}{pos2} stickers: {sticker1}, {sticker2}")
                return False
            return True
        def has_ud_color(face1, pos1, face2, pos2, label):
            sticker1 = self.cube.faces[face1][pos1[0]][pos1[1]]
            sticker2 = self.cube.faces[face2][pos2[0]][pos2[1]]
            if not (sticker1 in ['W', 'Y'] or sticker2 in ['W', 'Y']):
                print(f"Misoriented {label} edge: {face1}{pos1}-{face2}{pos2} stickers: {sticker1}, {sticker2}")
                return False
            return True
        # E slice edges (middle layer)
        e_slice_colors = ['G', 'B', 'O', 'R']
        e_slice = [
            ('F', (1,0), 'L', (1,2)),  # FL
            ('F', (1,2), 'R', (1,0)),  # FR
            ('B', (1,0), 'L', (1,0)),  # BL
            ('B', (1,2), 'R', (1,2)),  # BR
        ]
        e_mis = 0
        for edge in e_slice:
            if not check_edge_colors(*edge, e_slice_colors, label='E-slice'):
                e_mis += 1
        # M slice edges (must have U/D color)
        m_slice = [
            ('U', (1,0), 'L', (0,1)),  # UL
            ('D', (1,0), 'L', (2,1)),  # DL
            ('U', (1,2), 'R', (0,1)),  # UR
            ('D', (1,2), 'R', (2,1)),  # DR
        ]
        m_mis = 0
        for edge in m_slice:
            if not has_ud_color(*edge, label='M-slice'):
                m_mis += 1
        # S slice edges (must have U/D color)
        s_slice = [
            ('U', (2,1), 'F', (0,1)),  # UF
            ('D', (0,1), 'F', (2,1)),  # DF
            ('U', (0,1), 'B', (0,1)),  # UB
            ('D', (2,1), 'B', (2,1)),  # DB
        ]
        s_mis = 0
        for edge in s_slice:
            if not has_ud_color(*edge, label='S-slice'):
                s_mis += 1
        total_mis = e_mis + m_mis + s_mis
        print(f"Total misoriented phase 2 edges: {total_mis}")
        return total_mis == 0

    def _evaluate_phase3_state(self):
        """Evaluate Phase 3 state with detailed metrics"""
        score = 0
        max_score = 54  # 9 stickers per face * 6 faces
        
        for face in self.face_colors:
            center = self.cube.faces[face][1][1]
            target = self.face_colors[face]
            
            # Check if center matches target color
            if center != target:
                return 0  # Invalid state if centers don't match
                
            # Count matching stickers
            for i in range(3):
                for j in range(3):
                    if self.cube.faces[face][i][j] == target:
                        score += 1
                        
        return score / max_score  # Return percentage complete
        
    def get_phase3_state(self):
        """Check if cube is solved - each face should be a single color"""
        # Check each face for a single color
        for face, target_color in self.face_colors.items():
            center_color = self.cube.faces[face][1][1]
            # First verify that center matches expected color
            if center_color != target_color:
                print(f"Center of face {face} is {center_color}, expected {target_color}")
                return False
                
            # Then check that all stickers match the center
            for i in range(3):
                for j in range(3):
                    if self.cube.faces[face][i][j] != target_color:
                        print(f"Mismatch on face {face} at ({i},{j}): {self.cube.faces[face][i][j]} != {target_color}")
                        return False
        
        return True

    def get_phase0_edge_orientations(self):
        # Define the 12 edge cubies by their home colors (fixed order)
        edge_cubies = [
            (('U', 'F'), ['W', 'G']),  # UF
            (('U', 'R'), ['W', 'R']),  # UR
            (('U', 'B'), ['W', 'B']),  # UB
            (('U', 'L'), ['W', 'O']),  # UL
            (('F', 'R'), ['G', 'R']),  # FR
            (('F', 'L'), ['G', 'O']),  # FL
            (('B', 'L'), ['B', 'O']),  # BL
            (('B', 'R'), ['B', 'R']),  # BR
            (('D', 'F'), ['Y', 'G']),  # DF
            (('D', 'R'), ['Y', 'R']),  # DR
            (('D', 'B'), ['Y', 'B']),  # DB
            (('D', 'L'), ['Y', 'O']),  # DL
        ]
        # All possible edge positions (face, (i, j)) pairs
        edge_positions = [
            (('U', (2, 1)), ('F', (0, 1))),  # UF
            (('U', (1, 2)), ('R', (0, 1))),  # UR
            (('U', (0, 1)), ('B', (0, 1))),  # UB
            (('U', (1, 0)), ('L', (0, 1))),  # UL
            (('F', (1, 2)), ('R', (1, 0))),  # FR
            (('F', (1, 0)), ('L', (1, 2))),  # FL
            (('B', (1, 0)), ('L', (1, 0))),  # BL
            (('B', (1, 2)), ('R', (1, 2))),  # BR
            (('D', (0, 1)), ('F', (2, 1))),  # DF
            (('D', (1, 2)), ('R', (2, 1))),  # DR
            (('D', (2, 1)), ('B', (2, 1))),  # DB
            (('D', (1, 0)), ('L', (2, 1))),  # DL
        ]
        orientations = []
        for home, colors in edge_cubies:
            found = False
            # Search all edge positions for this cubie
            for (f1, p1), (f2, p2) in edge_positions:
                s1 = self.cube.faces[f1][p1[0]][p1[1]]
                s2 = self.cube.faces[f2][p2[0]][p2[1]]
                # Check if these stickers match the cubie's colors (in either order)
                if sorted([s1, s2]) == sorted(colors):
                    # Determine orientation
                    # For edges with W/Y, oriented if W/Y is on U/D face
                    if 'W' in colors or 'Y' in colors:
                        if (s1 in ['W', 'Y'] and f1 in ['U', 'D']) or (s2 in ['W', 'Y'] and f2 in ['U', 'D']):
                            orientations.append('0')
                        else:
                            orientations.append('1')
                    else:
                        # For others, oriented if G/B is on F/B face
                        if (s1 in ['G', 'B'] and f1 in ['F', 'B']) or (s2 in ['G', 'B'] and f2 in ['F', 'B']):
                            orientations.append('0')
                        else:
                            orientations.append('1')
                    found = True
                    break
            if not found:
                # Should not happen on a valid cube, but mark as misoriented
                orientations.append('1')
        return ''.join(orientations)

    def get_state_hash(self, phase):
        """Create a hash of the current cube state relevant to the given phase"""
        if phase == 0:
            # Combine orientation bits with slice-position signature to avoid over-pruning
            orient = self.get_phase0_edge_orientations()
            # Define edge positions as in orientation check
            edge_positions = [
                (('U', (2, 1)), ('F', (0, 1))),  # UF -> S-slice
                (('U', (1, 2)), ('R', (0, 1))),  # UR -> M-slice
                (('U', (0, 1)), ('B', (0, 1))),  # UB -> S-slice
                (('U', (1, 0)), ('L', (0, 1))),  # UL -> M-slice
                (('F', (1, 2)), ('R', (1, 0))),  # FR -> E-slice
                (('F', (1, 0)), ('L', (1, 2))),  # FL -> E-slice
                (('B', (1, 0)), ('L', (1, 0))),  # BL -> E-slice
                (('B', (1, 2)), ('R', (1, 2))),  # BR -> E-slice
                (('D', (0, 1)), ('F', (2, 1))),  # DF -> S-slice
                (('D', (1, 2)), ('R', (2, 1))),  # DR -> M-slice
                (('D', (2, 1)), ('B', (2, 1))),  # DB -> S-slice
                (('D', (1, 0)), ('L', (2, 1))),  # DL -> M-slice
            ]
            slice_code = []
            for (f1, _), (f2, _) in edge_positions:
                if {f1, f2} <= {'F', 'B'}:
                    slice_code.append('E')
                elif {f1, f2} <= {'U', 'D'}:
                    slice_code.append('S')
                else:
                    slice_code.append('M')
            return orient + ''.join(slice_code)
        elif phase == 1:
            # For phase 1, encode corner orientations explicitly
            # Orientation: 0 if U/D color is on U/D face, 1 or 2 otherwise
            # Corner order: ULB, UBR, UFL, URF, DFL, DRF, DLB, DBR
            corner_cubies = [
            ('ULB', ['W', 'B', 'O']),
            ('UBR', ['W', 'B', 'R']),
            ('UFL', ['W', 'G', 'O']),
            ('URF', ['W', 'G', 'R']),
            ('DFL', ['Y', 'G', 'O']),
            ('DRF', ['Y', 'G', 'R']),
            ('DLB', ['Y', 'B', 'O']),
            ('DBR', ['Y', 'B', 'R']),
        ]
        
            orientation_str = []
            for name, colors in corner_cubies:
                # Find the cubie's current location and stickers
                location = self.find_corner(colors)
                orientation = self.get_corner_orientation(location, colors)
                orientation_str.append(str(orientation))
            
            return ''.join(orientation_str)

        elif phase == 2:
            # For phase 2, encode slice edge positions (0 if in correct slice, 1 otherwise)
            # E slice edges (should only have F/B/L/R colors)
            e_slice_colors = ['G', 'B', 'O', 'R']
            e_edges = [
                ('F', (1,0), 'L', (1,2)),  # FL
                ('F', (1,2), 'R', (1,0)),  # FR
                ('B', (1,0), 'L', (1,0)),  # BL
                ('B', (1,2), 'R', (1,2)),  # BR
            ]
            e_slice = []
            for face1, pos1, face2, pos2 in e_edges:
                s1 = self.cube.faces[face1][pos1[0]][pos1[1]]
                s2 = self.cube.faces[face2][pos2[0]][pos2[1]]
                e_slice.append('0' if s1 in e_slice_colors and s2 in e_slice_colors else '1')
            # M slice edges (should have one U/D color)
            m_slice = [
                ('U', (1,0), 'L', (0,1)),  # UL
                ('D', (1,0), 'L', (2,1)),  # DL
                ('U', (1,2), 'R', (0,1)),  # UR
                ('D', (1,2), 'R', (2,1)),  # DR
            ]
            m_slice_bits = []
            for face1, pos1, face2, pos2 in m_slice:
                s1 = self.cube.faces[face1][pos1[0]][pos1[1]]
                s2 = self.cube.faces[face2][pos2[0]][pos2[1]]
                m_slice_bits.append('0' if (s1 in ['W','Y'] or s2 in ['W','Y']) else '1')
            # S slice edges (should have one U/D color)
            s_slice = [
                ('U', (2,1), 'F', (0,1)),  # UF
                ('D', (0,1), 'F', (2,1)),  # DF
                ('U', (0,1), 'B', (0,1)),  # UB
                ('D', (2,1), 'B', (2,1)),  # DB
            ]
            s_slice_bits = []
            for face1, pos1, face2, pos2 in s_slice:
                s1 = self.cube.faces[face1][pos1[0]][pos1[1]]
                s2 = self.cube.faces[face2][pos2[0]][pos2[1]]
                s_slice_bits.append('0' if (s1 in ['W','Y'] or s2 in ['W','Y']) else '1')
            return ''.join(e_slice + m_slice_bits + s_slice_bits)
        else:
            # For phase 3, create a more compact hash that captures essential state
            # but allows for some symmetries
            state = []
            
            # Hash only the non-center stickers, relative to their centers
            for face in ['U', 'D', 'F', 'B', 'L', 'R']:
                center = self.cube.faces[face][1][1]
                for i in range(3):
                    for j in range(3):
                        if i != 1 or j != 1:  # Skip centers
                            # Store if sticker matches its center
                            state.append('1' if self.cube.faces[face][i][j] == center else '0')
            
            return ''.join(state)
        return str(self.cube.faces)
    
    def find_corner(self, target_colors):
        # Search all corners to find the one with the target colors
        corners = [ 
            ('U', 0, 0, [('L', 0, 0), ('B', 0, 2)]),  # ULB
            ('U', 0, 2, [('B', 0, 0), ('R', 0, 2)]),  # UBR
            ('U', 2, 0, [('F', 0, 0), ('L', 0, 2)]),  # UFL
            ('U', 2, 2, [('R', 0, 0), ('F', 0, 2)]),  # URF
            ('D', 0, 0, [('F', 2, 0), ('L', 2, 2)]),  # DFL
            ('D', 0, 2, [('F', 2, 2), ('R', 2, 0)]),  # DRF
            ('D', 2, 0, [('B', 2, 2), ('L', 2, 0)]),  # DLB
            ('D', 2, 2, [('B', 2, 0), ('R', 2, 2)]),  # DBR
        ]  # Same as in get_phase1_state()
        for face, i, j, adj in corners:
            stickers = [self.cube.faces[face][i][j]]
            for f2, x2, y2 in adj:
                stickers.append(self.cube.faces[f2][x2][y2])
            if sorted(stickers) == sorted(target_colors):
                return (face, i, j, adj)
        return None

    def get_corner_orientation(self, location, solved_colors):
        if location is None:
            # should not happen on a valid cube
            return 0
        face, i, j, adj = location
        stickers = [self.cube.faces[face][i][j]]
        for f2, x2, y2 in adj:
            stickers.append(self.cube.faces[f2][x2][y2])

        # Find which of the three positions holds the U or Y sticker
        for idx, s in enumerate(stickers):
            if s in ('W','Y'):
                return idx  # 0 = correct orientation, 1 or 2 = twisted
        return 0
    
    def _count_matching_stickers(self):
            matches = 0
            for face in ['U', 'D', 'F', 'B', 'L', 'R']:
                center = self.cube.faces[face][1][1]
                matches += sum(sticker == center for row in self.cube.faces[face] 
                            for sticker in row)
            return matches
    
    def is_redundant_move(self, move, last_move):
        """Check if a move is redundant based on the last move made"""
        if not last_move:
            return False
            
        # Get base move (without prime/2)
        base_move = move[0]
        last_base = last_move[0]
        
        # Skip moves on same face
        if base_move == last_base:
            return True
            
        # Skip opposite face moves in wrong order (e.g., U after D)
        opposites = {'U':'D', 'D':'U', 'F':'B', 'B':'F', 'L':'R', 'R':'L', 
                    'M':'S', 'S':'M', 'E':'M'}
        if base_move in opposites and last_base == opposites[base_move]:
            # For opposite faces, we can allow different move types
            # e.g., allow U' after D2 but not U after D
            if last_move.endswith("2") or move.endswith("2"):
                return False
            return True
            
        # Special handling for slice moves
        slice_moves = {'M':['L','R'], 'E':['U','D'], 'S':['F','B']}
        if base_move in slice_moves and last_base in slice_moves[base_move]:
            return True
        
        return False
            
    def _phase3_heuristic(self):
        """Simpler, more permissive heuristic for phase 3"""
        misplaced = 0
        
        # First check centers
        for face in self.face_colors:
            if self.cube.faces[face][1][1] != self.face_colors[face]:
                return float('inf')
        
        # Count misplaced stickers with reduced weight
        for face in self.face_colors:
            target = self.face_colors[face]
            for i in range(3):
                for j in range(3):
                    if self.cube.faces[face][i][j] != target:
                        if (i in [0,2] and j in [0,2]):  # corners
                            misplaced += 2
                        else:  # edges
                            misplaced += 1
        
        # More permissive estimate
        return max(1, misplaced // 12)  # At least 1 move if any stickers wrong

    def solve_phase(self, phase):
        """Solve a specific phase of the Thistlethwaite algorithm using iterative deepening with improved state tracking"""
        max_moves = [15, 10, 13, 18]  # Maximum moves per phase
        max_depth = max_moves[phase]
        current_moves = []
        solution_found = False
        best_solution = []
        visited_states = {}

        def get_valid_moves(last_move):
            valid_moves = []
            for move in self.phase_moves[phase]:
            # skip same‑face / opposite / slice redundancies immediately
                if not last_move or not self._are_moves_redundant(move, last_move):
                    valid_moves.append(move)
            return valid_moves

        def check_phase_solved():
            if phase == 0:
                return self.get_phase0_state()
            elif phase == 1:
                return self.get_phase1_state()
            elif phase == 2:
                return self.get_phase2_state()
            else:
                
                return self.get_phase3_state()

        def solve_at_depth(depth, state_hash, last_move=None):
            nonlocal solution_found, best_solution
            
            if solution_found:
                return True
                
            if check_phase_solved():
                solution_found = True
                best_solution = current_moves.copy()
                return True
                
            if depth == 0:
                return False

            valid_moves = get_valid_moves(last_move)
            for move in valid_moves:
                if solution_found:
                    break
                    
                current_moves.append(move)
                self.cube.move(move)
                
                new_hash = self.get_state_hash(phase)
                if new_hash not in visited_states or len(current_moves) < visited_states[new_hash]:
                    visited_states[new_hash] = len(current_moves)
                    print(f"Trying move: {move} at depth {max_depth - depth + 1}")
                    if solve_at_depth(depth - 1, new_hash, move):
                        return True
                
                self.cube.move(self.inverse_move(move))
                current_moves.pop()
            
            return False

        # Try increasingly deeper searches
        for d in range(1, max_depth + 1):
            print(f"\nStarting depth {d} search")
            visited_states.clear()
            visited_states[self.get_state_hash(phase)] = 0
            current_moves.clear()
            solution_found = False
            
            if solve_at_depth(d, self.get_state_hash(phase)):
                return best_solution

        print("No solution found within the maximum depth")
        return []

    def _are_moves_redundant(self, move1, move2):
        """Check if two moves are redundant (cancel each other or same/slice face)"""
        if not move1 or not move2:
            return False
        face1, face2 = move1[0], move2[0]

        # Skip moves on the same face
        if face1 == face2:
            return True

        # Skip opposite face moves in wrong order (e.g., U after D)
        opposites = {
            'U': 'D', 'D': 'U',
            'F': 'B', 'B': 'F',
            'L': 'R', 'R': 'L',
        }
        if face1 in opposites and face2 == opposites[face1]:
            # allow if either is a double-turn
            if move1.endswith('2') or move2.endswith('2'):
                return False
            return True

        # Skip slice vs adjacent face redundancies
        slice_map = {
            'M': ['L', 'R'],   # M is between L/R
            'E': ['U', 'D'],   # E is between U/D
            'S': ['F', 'B'],   # S is between F/B
        }
        if face1 in slice_map and face2 in slice_map[face1]:
            return True
        if face2 in slice_map and face1 in slice_map[face2]:
            return True

        return False

    def inverse_move(self, move):
        """Return the inverse of a move"""
        if len(move) == 1:  # Single move like "U" becomes "U'"
            return move + "'"
        elif move.endswith("'"): # Prime move like "U'" becomes "U"
            return move[0]
        elif move.endswith("2"): # Double move like "U2" stays "U2"
            return move
        return move