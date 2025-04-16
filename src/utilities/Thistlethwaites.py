from cube import RubiksCube

class ThistlethwaiteSolver:
    def __init__(self, cube: RubiksCube):
        self.cube = cube if cube else RubiksCube()
        # Define move groups for each phase
        self.phase_moves = [
            # Phase 0: Any move
            ["U", "U'", "U2", "D", "D'", "D2", 
             "L", "L'", "L2", "R", "R'", "R2", 
             "F", "F'", "F2", "B", "B'", "B2"],
            
            # Phase 1: Quarter turns of U/D, half turns of others
            ["U", "U'", "U2", "D", "D'", "D2", 
             "R", "R'", "R2", "L2", 
             "F2", "B2"],
            
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
        An edge is oriented if:
        - For edges involving U or D: the U/D color is on the U or D face
        - For edges involving F or B: the F/B color is on the F or B face
        """
        face_colors = {'U': 'W', 'D': 'Y', 'F': 'G', 'B': 'B', 'L': 'O', 'R': 'R'}
        edges = [
            ('U', (0,1), 'B', (0,1)),  # UB
            ('U', (1,2), 'R', (0,1)),  # UR
            ('U', (2,1), 'F', (0,1)),  # UF
            ('U', (1,0), 'L', (0,1)),  # UL
            ('F', (1,0), 'L', (1,2)),  # FL
            ('F', (1,2), 'R', (1,0)),  # FR
            ('B', (1,0), 'L', (1,0)),  # BL
            ('B', (1,2), 'R', (1,2)),  # BR
            ('D', (0,1), 'F', (2,1)),  # DF
            ('D', (1,2), 'R', (2,1)),  # DR
            ('D', (2,1), 'B', (2,1)),  # DB
            ('D', (1,0), 'L', (2,1)),  # DL
        ]
        misoriented = 0
        for f1, pos1, f2, pos2 in edges:
            s1 = self.cube.faces[f1][pos1[0]][pos1[1]]
            s2 = self.cube.faces[f2][pos2[0]][pos2[1]]
            if f1 in ['U', 'D']:
                if s1 != face_colors[f1] and s2 != face_colors[f1]:
                    misoriented += 1
            elif f2 in ['U', 'D']:
                if s2 != face_colors[f2] and s1 != face_colors[f2]:
                    misoriented += 1
            elif f1 in ['F', 'B']:
                if s1 != face_colors[f1] and s2 != face_colors[f1]:
                    misoriented += 1
            elif f2 in ['F', 'B']:
                if s2 != face_colors[f2] and s1 != face_colors[f2]:
                    misoriented += 1
        print(f"Total misoriented edges: {misoriented}")
        return misoriented == 0

    def get_phase1_state(self):
        """Check corner orientation - all corners must be oriented correctly.
        In Phase 1, corners are correctly oriented when their U/D colored sticker
        is on the U or D face."""
        u_corners = [
            ('U', 0, 0),  # ULB
            ('U', 0, 2),  # UBR
            ('U', 2, 0),  # UFL
            ('U', 2, 2),  # URF
        ]
        d_corners = [
            ('D', 0, 0),  # DFL
            ('D', 0, 2),  # DRF
            ('D', 2, 0),  # DLB
            ('D', 2, 2),  # DBR
        ]
        misoriented = 0
        for face, i, j in u_corners + d_corners:
            sticker = self.cube.faces[face][i][j]
            if sticker not in ['W', 'Y']:
                print(f"Misoriented corner: {face} {i},{j} sticker: {sticker}")
                misoriented += 1
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
        face_colors = {'U': 'W', 'D': 'Y', 'F': 'G', 'B': 'B', 'L': 'O', 'R': 'R'}
        score = 0
        max_score = 54  # 9 stickers per face * 6 faces
        
        for face in face_colors:
            center = self.cube.faces[face][1][1]
            target = face_colors[face]
            
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
        score = self._evaluate_phase3_state()
        if score < 1.0:
            print(f"Cube completion: {score*100:.1f}%")
            faces = ['U', 'D', 'F', 'B', 'L', 'R']
            face_colors = {'U': 'W', 'D': 'Y', 'F': 'G', 'B': 'B', 'L': 'O', 'R': 'R'}
            
            print("Cube is NOT fully solved:")
            for face in faces:
                center = self.cube.faces[face][1][1]
                target = face_colors[face]
                for i in range(3):
                    for j in range(3):
                        if self.cube.faces[face][i][j] != target:
                            print(f"- Face {face} position ({i},{j}): {self.cube.faces[face][i][j]} != {target}")
            return False
        return True

    def get_state_hash(self, phase):
        """Create a hash of the current cube state relevant to the given phase"""
        if phase == 0:
            # For phase 0, track edge orientations
            edge_state = []
            # Up layer edges
            edge_state.extend([
                self.cube.faces['U'][0][1] + self.cube.faces['B'][0][1],  # UB
                self.cube.faces['U'][1][2] + self.cube.faces['R'][0][1],  # UR
                self.cube.faces['U'][2][1] + self.cube.faces['F'][0][1],  # UF
                self.cube.faces['U'][1][0] + self.cube.faces['L'][0][1],  # UL
            ])
            # Middle layer edges
            edge_state.extend([
                self.cube.faces['F'][1][0] + self.cube.faces['L'][1][2],  # FL
                self.cube.faces['F'][1][2] + self.cube.faces['R'][1][0],  # FR
                self.cube.faces['B'][1][0] + self.cube.faces['L'][1][0],  # BL
                self.cube.faces['B'][1][2] + self.cube.faces['R'][1][2],  # BR
            ])
            # Down layer edges
            edge_state.extend([
                self.cube.faces['D'][0][1] + self.cube.faces['F'][2][1],  # DF
                self.cube.faces['D'][1][2] + self.cube.faces['R'][2][1],  # DR
                self.cube.faces['D'][2][1] + self.cube.faces['B'][2][1],  # DB
                self.cube.faces['D'][1][0] + self.cube.faces['L'][2][1],  # DL
            ])
            return ''.join(edge_state)

        elif phase == 1:
            # For phase 1, track corner orientations
            corner_state = []
            bad_corners = 0
            
            def check_corner(face, i, j):
                nonlocal bad_corners
                sticker = self.cube.faces[face][i][j]
                if sticker not in ['W', 'Y']:
                    bad_corners += 1
                return sticker
            
            # Track full corner states and bad corner count
            # Up corners
            corner_state.extend([
                check_corner('U', 0, 0),  # ULB
                check_corner('U', 0, 2),  # UBR
                check_corner('U', 2, 0),  # UFL
                check_corner('U', 2, 2),  # URF
            ])
            # Down corners
            corner_state.extend([
                check_corner('D', 0, 0),  # DFL
                check_corner('D', 0, 2),  # DRF
                check_corner('D', 2, 0),  # DLB
                check_corner('D', 2, 2),  # DBR
            ])
            
            return f"{bad_corners}{''.join(corner_state)}"
            
        elif phase == 2:
            # For phase 2, we need to track which edges are in wrong slices
            bad_edges = 0
            edge_state = []
            
            def check_edge_slice(face1, pos1, face2, pos2, expected_colors):
                """Check if an edge belongs in its slice and return its state"""
                nonlocal bad_edges
                sticker1 = self.cube.faces[face1][pos1[0]][pos1[1]]
                sticker2 = self.cube.faces[face2][pos2[0]][pos2[1]]
                if not set([sticker1, sticker2]).issubset(set(expected_colors)):
                    bad_edges += 1
                return sticker1 + sticker2
            
            # E slice edges (should only have F/B/L/R colors)
            e_slice_colors = ['G', 'B', 'O', 'R']
            for edge in [
                ('F', (1,0), 'L', (1,2)),  # FL
                ('F', (1,2), 'R', (1,0)),  # FR
                ('B', (1,0), 'L', (1,0)),  # BL
                ('B', (1,2), 'R', (1,2)),  # BR
            ]:
                edge_state.append(check_edge_slice(*edge, e_slice_colors))
            
            # M slice edges (should have one U/D color)
            m_slice_colors = ['W', 'Y', 'G', 'B']
            for edge in [
                ('U', (1,0), 'L', (0,1)),  # UL
                ('D', (1,0), 'L', (2,1)),  # DL
                ('U', (1,2), 'R', (0,1)),  # UR
                ('D', (1,2), 'R', (2,1)),  # DR
            ]:
                edge_state.append(check_edge_slice(*edge, m_slice_colors))
            
            # S slice edges (should have one U/D color)
            s_slice_colors = ['W', 'Y', 'O', 'R']
            for edge in [
                ('U', (2,1), 'F', (0,1)),  # UF
                ('D', (0,1), 'F', (2,1)),  # DF
                ('U', (0,1), 'B', (0,1)),  # UB
                ('D', (2,1), 'B', (2,1)),  # DB
            ]:
                edge_state.append(check_edge_slice(*edge, s_slice_colors))
            
            return f"{bad_edges}{''.join(edge_state)}"
        elif phase == 3:
            # Use the full sticker layout for all faces
            state = []
            for face in ['U', 'D', 'F', 'B', 'L', 'R']:
                for row in self.cube.faces[face]:
                    state.extend(row)
            return ''.join(state)
        return str(self.cube.faces)
    
    def _count_matching_stickers(self):
            matches = 0
            for face in ['U', 'D', 'F', 'B', 'L', 'R']:
                center = self.cube.faces[face][1][1]
                matches += sum(sticker == center for row in self.cube.faces[face] 
                            for sticker in row)
            return matches
            
    def solve_phase(self, phase):
        """Solve a specific phase of the cube using iterative deepening"""
        max_moves = [12, 10, 13, 22]  # Maximum moves per phase
        current_moves = []
        visited_states = set()
        recursion_limit = 1000  # Limit for recursion depth
        recursion_count = 0
        best_state = None
        best_score = 0
        
        def evaluate_position():
            """Evaluate current position for Phase 3"""
            if phase != 3:
                return 0
                
            solved_faces = 0
            for face in ['U', 'D', 'F', 'B', 'L', 'R']:
                center = self.cube.faces[face][1][1]
                center = self.cube.faces[face][1][1]
                if all(self.cube.faces[face][i][j] == center for i in range(3) for j in range(3)):
                    solved_faces += 1
                
            return solved_faces
        
        def try_moves(depth, max_depth, last_move=None):
            nonlocal best_state, best_score, current_moves
            
            # Check if we're at max depth
            if depth == max_depth:
                # For phase 3, keep track of best incomplete solution
                if phase == 3:
                    score = evaluate_position()
                    if score > best_score:
                        best_score = score
                        best_state = current_moves[:]
                return False
                
            # First check if current state solves the phase
            if ((phase == 0 and self.get_phase0_state()) or
                (phase == 1 and self.get_phase1_state()) or
                (phase == 2 and self.get_phase2_state()) or
                (phase == 3 and self.get_phase3_state())):
                return True
                
            # Get state hash and check if we've seen this state
            state_hash = self.get_state_hash(phase)
            if state_hash in visited_states:
                return False
            visited_states.add(state_hash)
            
            # For phase 3, prioritize moves that keep partial progress
            moves = self.phase_moves[phase]
            if phase == 3:
                # Start with moves that are most likely to help
                current_score = evaluate_position()
                scored_moves = []
                
                for move in moves:
                    # Try move
                    self.cube.move(move)
                    new_score = evaluate_position()
                    self.cube.move(self.inverse_move(move))
                    
                    # Score is change in position quality
                    scored_moves.append((new_score - current_score, move))
                    
                # Sort moves by score, best first
                scored_moves.sort(reverse=True)
                moves = [m for _, m in scored_moves]
            
            # Try each move
            for move in moves:
                # Skip moves that undo the last move
                if last_move:
                    if (move.startswith(last_move[0]) or  # Same face
                        (len(move) > 1 and move[1] == "'" and move[0] == last_move[0])):  # Inverse
                        continue
                        
                self.cube.move(move)
                current_moves.append(move)
                
                if try_moves(depth + 1, max_depth, move):
                    return True
                    
                self.cube.move(self.inverse_move(move))
                current_moves.pop()
                
            return False

        # Try increasingly deeper searches
        for depth in range(1, max_moves[phase] + 1):
            visited_states.clear()
            current_moves.clear()
            best_state = None
            best_score = 0
            
            if try_moves(0, depth):
                return current_moves
                
            # For phase 3, if we have a good partial solution, try extending it
            if phase == 3 and best_state:
                # Apply the best partial solution
                current_moves = best_state[:]
                for move in current_moves:
                    self.cube.move(move)
                    
                # Try to complete from this position
                remaining_depth = depth - len(current_moves)
                if remaining_depth > 0:
                    visited_states.clear()
                    if try_moves(0, remaining_depth):
                        return current_moves
                        
                # Undo the partial solution
                for move in reversed(current_moves):
                    self.cube.move(self.inverse_move(move))
                current_moves.clear()
                
        # If we reach here and it's phase 3, return best partial solution
        if phase == 3 and best_state:
            return best_state
            
        return current_moves

    def inverse_move(self, move):
        """Return the inverse of a move"""
        if len(move) == 1:  # Single move like "U" becomes "U'"
            return move + "'"
        elif move.endswith("'"): # Prime move like "U'" becomes "U"
            return move[0]
        elif move.endswith("2"): # Double move like "U2" stays "U2"
            return move
        return move