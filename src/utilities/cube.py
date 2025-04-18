class RubiksCube:
    def __init__(self):
        # Initialize the cube with 6 faces, each a 3x3 array
        # Each face is represented by a single character for its color
        self.faces = {
            'U': [['W'] * 3 for _ in range(3)],  # Up (White)
            'D': [['Y'] * 3 for _ in range(3)],  # Down (Yellow)
            'F': [['G'] * 3 for _ in range(3)],  # Front (Green)
            'B': [['B'] * 3 for _ in range(3)],  # Back (Blue)
            'L': [['O'] * 3 for _ in range(3)],  # Left (Orange)
            'R': [['R'] * 3 for _ in range(3)]   # Right (Red)
        }

    def load_from_cube_data(self, cube_data):
        """
        Load cube_data (with keys 'top', 'right', 'front', 'bottom', 'left', 'back')
        into this RubiksCube object, mapping to faces 'U', 'R', 'F', 'D', 'L', 'B'
        using the same orientation logic as create_cube in kociembaSolver.py.
        """
        face_map = {
            'top': 'U',
            'right': 'R',
            'front': 'F',
            'bottom': 'D',
            'left': 'L',
            'back': 'B'
        }

        for face_name, face_key in face_map.items():
            face_data = cube_data[face_name]
            if face_name == 'top':
                self.faces[face_key] = [row[:] for row in face_data]
            elif face_name == 'right':
                # columns top-bottom, right-left
                self.faces[face_key] = [[face_data[j][2] for j in range(3)] for i in range(3)]
            elif face_name == 'front':
                self.faces[face_key] = [row[:] for row in face_data]
            elif face_name == 'bottom':
                # rows left-right, bottom-top
                self.faces[face_key] = [row[:] for row in face_data]
            elif face_name == 'left':
                # columns top-bottom, left-right
                self.faces[face_key] = [[face_data[j][0] for j in range(3)] for i in range(3)]
            elif face_name == 'back':
                # rows right-left, bottom-top
                self.faces[face_key] = [[face_data[i][2-j] for j in range(3)] for i in range(3)]

    def rotate_face_clockwise(self, face):
        # Rotate a single face 90 degrees clockwise
        self.faces[face] = [list(row) for row in zip(*self.faces[face][::-1])]

    def rotate_face_counterclockwise(self, face):
        # Rotate a single face 90 degrees counterclockwise
        self.faces[face] = [list(row) for row in zip(*self.faces[face])][::-1]

    def move(self, move):
        # Perform a move on the cube
        if move == "U":
            self.rotate_face_clockwise('U')
            temp = [self.faces['F'][0][i] for i in range(3)]
            
            # Move right to front (with rotation)
            for i in range(3):
                self.faces['F'][0][i] = self.faces['R'][0][i]
            
            # Move back to right (with rotation)
            for i in range(3):
                self.faces['R'][0][i] = self.faces['B'][0][i]
            
            # Move left to back
            for i in range(3):
                self.faces['B'][0][i] = self.faces['L'][0][i]
            
            # Move temp (original up) to front
            for i in range(3):
                self.faces['L'][0][i] = temp[i]
        elif move == "U'":
            self.rotate_face_counterclockwise('U')
            temp = [self.faces['L'][0][i] for i in range(3)]
            
            # Move back to left (with rotation)
            for i in range(3):
                self.faces['L'][0][i] = self.faces['B'][0][i]
            
            # Move right to back (with rotation)
            for i in range(3):
                self.faces['B'][0][i] = self.faces['R'][0][i]
            
            # Move left to back
            for i in range(3):
                self.faces['R'][0][i] = self.faces['F'][0][i]
            
            # Move temp (original up) to front
            for i in range(3):
                self.faces['F'][0][i] = temp[i]
        elif move == "U2":
            self.move("U")
            self.move("U")
        elif move == "D":
            self.rotate_face_clockwise('D')
            self._cycle_edges(['F', 'L', 'B', 'R'], 2, reverse=False, vertical=False)
        elif move == "D'":
            self.rotate_face_counterclockwise('D')
            self._cycle_edges(['F', 'R', 'B', 'L'], 2, reverse=False, vertical=False)
        elif move == "D2":
            self.move("D")
            self.move("D")
        elif move == "F":
            self.rotate_face_clockwise('F')
            # Store the original top edge
            temp = self.faces['U'][2].copy()
            
            # Move left edge to top (with rotation)
            self.faces['U'][2][0] = self.faces['L'][2][2]
            self.faces['U'][2][1] = self.faces['L'][1][2]
            self.faces['U'][2][2] = self.faces['L'][0][2]
            
            # Move bottom edge to left (with rotation)
            self.faces['L'][0][2] = self.faces['D'][0][0]
            self.faces['L'][1][2] = self.faces['D'][0][1]
            self.faces['L'][2][2] = self.faces['D'][0][2]
            
            # Move right edge to bottom (with rotation)
            self.faces['D'][0][0] = self.faces['R'][2][0]
            self.faces['D'][0][1] = self.faces['R'][1][0]
            self.faces['D'][0][2] = self.faces['R'][0][0]
            
            # Move stored top edge to right (with rotation)
            self.faces['R'][0][0] = temp[0]
            self.faces['R'][1][0] = temp[1]
            self.faces['R'][2][0] = temp[2]

        elif move == "F'":
            self.rotate_face_counterclockwise('F')
            # Store the original top edge
            temp = self.faces['U'][2].copy()
            
            # Move right edge to top (with rotation)
            self.faces['U'][2][0] = self.faces['R'][0][0]
            self.faces['U'][2][1] = self.faces['R'][1][0]
            self.faces['U'][2][2] = self.faces['R'][2][0]
            
            # Move bottom edge to right (with rotation)
            self.faces['R'][0][0] = self.faces['D'][0][2]
            self.faces['R'][1][0] = self.faces['D'][0][1]
            self.faces['R'][2][0] = self.faces['D'][0][0]
            
            # Move left edge to bottom (with rotation)
            self.faces['D'][0][0] = self.faces['L'][2][2]
            self.faces['D'][0][1] = self.faces['L'][1][2]
            self.faces['D'][0][2] = self.faces['L'][0][2]
            
            # Move stored top edge to left (with rotation)
            self.faces['L'][0][2] = temp[2]
            self.faces['L'][1][2] = temp[1]
            self.faces['L'][2][2] = temp[0]

        elif move == "F2":
            self.move("F")
            self.move("F")
        elif move == "B":
            self.rotate_face_clockwise('B')
            # Store the original top edge
            temp = self.faces['U'][0].copy()
            # Move right edge to top (with rotation) 
            self.faces['U'][0][0] = self.faces['R'][0][2]
            self.faces['U'][0][1] = self.faces['R'][1][2]
            self.faces['U'][0][2] = self.faces['R'][2][2]
            # Move bottom edge to right (with rotation)
            self.faces['R'][0][2] = self.faces['D'][2][2]
            self.faces['R'][1][2] = self.faces['D'][2][1]
            self.faces['R'][2][2] = self.faces['D'][2][0]
            # Move left edge to bottom (with rotation)
            self.faces['D'][2][0] = self.faces['L'][0][0]
            self.faces['D'][2][1] = self.faces['L'][1][0]
            self.faces['D'][2][2] = self.faces['L'][2][0]
            # Move stored top edge to left (with rotation)
            self.faces['L'][0][0] = temp[2]
            self.faces['L'][1][0] = temp[1]
            self.faces['L'][2][0] = temp[0]
        elif move == "B'":
            self.rotate_face_counterclockwise('B')
            # Store the original top edge
            temp = self.faces['U'][0].copy()
            # Move left edge to top (with rotation)
            self.faces['U'][0][2] = self.faces['L'][0][0]
            self.faces['U'][0][1] = self.faces['L'][1][0]
            self.faces['U'][0][0] = self.faces['L'][2][0]
            # Move bottom edge to left (with rotation)
            self.faces['L'][0][0] = self.faces['D'][2][2]
            self.faces['L'][1][0] = self.faces['D'][2][1]
            self.faces['L'][2][0] = self.faces['D'][2][0]
            # Move right edge to bottom (with rotation)
            self.faces['D'][2][0] = self.faces['R'][2][2]
            self.faces['D'][2][1] = self.faces['R'][1][2]
            self.faces['D'][2][2] = self.faces['R'][0][2]
            # Move stored top edge to right (with rotation)
            self.faces['R'][0][2] = temp[2]
            self.faces['R'][1][2] = temp[1]
            self.faces['R'][2][2] = temp[0]
        elif move == "B2":
            self.move("B")
            self.move("B")
        elif move == "L":
            self.rotate_face_clockwise('L')
            temp = [self.faces['U'][i][0] for i in range(3)]
            
            # Move back to up (with rotation)
            for i in range(3):
                self.faces['U'][i][0] = self.faces['B'][2-i][2]
            
            # Move down to back (with rotation)
            for i in range(3):
                self.faces['B'][i][2] = self.faces['D'][2-i][0]
            
            # Move front to down
            for i in range(3):
                self.faces['D'][i][0] = self.faces['F'][i][0]
            
            # Move temp (original up) to front
            for i in range(3):
                self.faces['F'][i][0] = temp[i]

        elif move == "L'":
            self.rotate_face_counterclockwise('L')
            temp = [self.faces['U'][i][0] for i in range(3)]
            
            # Move front to up
            for i in range(3):
                self.faces['U'][i][0] = self.faces['F'][i][0]
            
            # Move down to front
            for i in range(3):
                self.faces['F'][i][0] = self.faces['D'][i][0]
            
            # Move back to down (with rotation)
            for i in range(3):
                self.faces['D'][i][0] = self.faces['B'][2-i][2]
            
            # Move temp (original up) to back (with rotation)
            for i in range(3):
                self.faces['B'][i][2] = temp[i]

        elif move == "L2":
            self.move("L")
            self.move("L")
        elif move == "R":
            self.rotate_face_clockwise("R")
            temp = [self.faces['U'][i][2] for i in range(3)]
            
            # Move front to up (with rotation)
            for i in range(3):
                self.faces['U'][i][2] = self.faces['F'][i][2]
            
            # Move down to front (with rotation)
            for i in range(3):
                self.faces['F'][i][2] = self.faces['D'][i][2]
            
            # Move front to down
            for i in range(3):
                self.faces['D'][i][2] = self.faces['B'][2-i][0]
            
            # Move temp (original up) to front
            for i in range(3):
                self.faces['B'][2-i][0] = temp[i]

        elif move == "R'":
            self.rotate_face_counterclockwise('R')
            temp = [self.faces['U'][i][2] for i in range(3)]
            
            # Move back to up
            for i in range(3):
                self.faces['U'][i][2] = self.faces['B'][2-i][0]
            
            # Move down to back
            for i in range(3):
                self.faces['B'][i][0] = self.faces['D'][2-i][2]
            
            # Move front to down
            for i in range(3):
                self.faces['D'][i][2] = self.faces['F'][i][2]
            
            # Move temp (original up) to front
            for i in range(3):
                self.faces['F'][i][2] = temp[i]

        elif move == "R2":
            self.move("R")
            self.move("R")

        elif move == "S":
            temp = [self.faces['U'][1][i] for i in range(3)]
            for i in range(3):
                self.faces['U'][1][i] = self.faces['L'][2-i][1]
            for i in range(3):
                self.faces['L'][i][1] = self.faces['D'][1][i]
            for i in range(3):
                self.faces['D'][1][i] = self.faces['R'][2-i][1]
            for i in range(3):
                self.faces['R'][i][1] = temp[i]
        elif move == "S2":
            self.move("S")
            self.move("S")
        elif move == "S'": 
            temp = [self.faces['U'][1][i] for i in range(3)]
            for i in range(3):
                self.faces['U'][1][i] = self.faces['R'][i][1]
            for i in range(3):
                self.faces['R'][i][1] = self.faces['D'][1][2-i]
            for i in range(3):
                self.faces['D'][1][i] = self.faces['L'][i][1]
            for i in range(3):
                self.faces['L'][2-i][1] = temp[i]
        elif move == "E'":
            temp = [self.faces['F'][1][i] for i in range(3)]
            
            # Move right to front (with rotation)
            for i in range(3):
                self.faces['F'][1][i] = self.faces['R'][1][i]
            
            # Move back to right (with rotation)
            for i in range(3):
                self.faces['R'][1][i] = self.faces['B'][1][i]
            
            # Move left to back
            for i in range(3):
                self.faces['B'][1][i] = self.faces['L'][1][i]
            
            # Move temp (original up) to front
            for i in range(3):
                self.faces['L'][1][i] = temp[i]
        elif move == "E":
            temp = [self.faces['L'][0][i] for i in range(3)]
            
            # Move back to left (with rotation)
            for i in range(3):
                self.faces['L'][1][i] = self.faces['B'][1][i]
            
            # Move right to back (with rotation)
            for i in range(3):
                self.faces['B'][1][i] = self.faces['R'][1][i]
            
            # Move left to back
            for i in range(3):
                self.faces['R'][1][i] = self.faces['F'][1][i]
            
            # Move temp (original up) to front
            for i in range(3):
                self.faces['F'][1][i] = temp[i]
        elif move == "E2":
            self.move("E")
            self.move("E")

        elif move == "M":
            temp = [self.faces['U'][i][1] for i in range(3)]
            
            # Move right to front (with rotation)
            for i in range(3):
                self.faces['U'][i][1] = self.faces['B'][i][1]
            
            # Move back to right (with rotation)
            for i in range(3):
                self.faces['B'][i][1] = self.faces['D'][2-i][1]
            
            # Move left to back
            for i in range(3):
                self.faces['D'][i][1] = self.faces['F'][i][1]
            
            # Move temp (original up) to front
            for i in range(3):
                self.faces['F'][i][1] = temp[i]
        elif move == "M'":
            temp = [self.faces['U'][i][1] for i in range(3)]
            
            # Move back to left (with rotation)
            for i in range(3):
                self.faces['U'][i][1] = self.faces['F'][i][1]
            
            # Move right to back (with rotation)
            for i in range(3):
                self.faces['F'][i][1] = self.faces['D'][i][1]
            
            # Move left to back
            for i in range(3):
                self.faces['D'][i][1] = self.faces['B'][2-i][1]
            
            # Move temp (original up) to front
            for i in range(3):
                self.faces['B'][2-i][1] = temp[i]
        elif move == "M2":
            self.move("M")
            self.move("M")

    def edges_orientation_heuristic(self):
        """Calculate the number of incorrectly oriented edges."""
        incorrect_edges = 0

        # Define the edges and their correct orientation
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

        for edge in edges:
            face1, row1, col1, face2, row2, col2 = edge
            color1 = self.faces[face1][row1][col1]
            color2 = self.faces[face2][row2][col2]

            # Check if the edge is oriented correctly
            if not self.is_edge_oriented(color1, color2):
                incorrect_edges += 1

        return incorrect_edges

    def is_edge_oriented(self, color1, color2):
        """Check if an edge is oriented correctly based on its colors."""
        # Define the correct orientation for each color pair
        # Assuming White ('W') and Yellow ('Y') are the Up and Down colors
        return (color1 in ['W', 'Y'] or color2 in ['W', 'Y'])

    def _cycle_edges(self, faces, index, reverse=False, vertical=False):
        """
        Cycles the edges of the cube based on the given parameters.
        :param faces: List of face keys to cycle.
        :param index: Row or column index to cycle.
        :param reverse: Whether to cycle in reverse order.
        :param vertical: Whether the cycle is vertical (columns) or horizontal (rows).
        """
        # Helper function to cycle the edges of the cube
        if vertical:
            # Store the original values for vertical cycling (L/R moves)
            temp = [self.faces[faces[0]][i][index] for i in range(3)]
            
            # Cycle edges in the correct order based on reverse flag
            if not reverse:
                # Normal direction: U -> F -> D -> B -> U
                for i in range(3):
                    self.faces[faces[0]][i][index] = self.faces[faces[1]][i][index]
                    self.faces[faces[1]][i][index] = self.faces[faces[2]][i][index]
                    self.faces[faces[2]][i][index] = self.faces[faces[3]][i][index]
                    self.faces[faces[3]][i][index] = temp[i]
            else:
                # Reverse direction: U -> B -> D -> F -> U
                for i in range(3):
                    self.faces[faces[0]][i][index] = self.faces[faces[3]][i][index]
                    self.faces[faces[3]][i][index] = self.faces[faces[2]][i][index]
                    self.faces[faces[2]][i][index] = self.faces[faces[1]][i][index]
                    self.faces[faces[1]][i][index] = temp[i]
        else:
            # Store the original values for horizontal cycling (U/D moves)
            temp = self.faces[faces[0]][index].copy()
            
            # Cycle edges in the correct order based on reverse flag
            if not reverse:
                # Normal direction: F -> R -> B -> L -> F
                for i in range(len(faces) - 1):
                    self.faces[faces[i]][index] = self.faces[faces[i + 1]][index]
                self.faces[faces[-1]][index] = temp
            else:
                # Reverse direction: F -> L -> B -> R -> F
                for i in range(len(faces) - 1, 0, -1):
                    self.faces[faces[i]][index] = self.faces[faces[i - 1]][index]
                self.faces[faces[0]][index] = temp

    def print_cube(self):
        """
        Prints the cube in a flat layout:
            U
          L F R B
            D
        """
        # Define spacing for alignment
        space = " " * 6

        # Print Up face
        for row in self.faces['U']:
            print(f"{space}{''.join(row)}")
        
        # Print middle layer (Left, Front, Right, Back)
        for i in range(3):
            row = []
            for face in ['L', 'F', 'R', 'B']:
                row.extend(self.faces[face][i])
                row.append(' ')  # Add space between faces
            print(''.join(row))
        
        # Print Down face
        for row in self.faces['D']:
            print(f"{space}{''.join(row)}")

    def __str__(self):
        """Makes the cube printable using print(cube)"""
        self.print_cube()
        return ""  # Return empty string since print_cube handles the output

    def is_top_cross_solved(self):
        # Check if all edges on top face match the center
        center = self.faces['U'][1][1]
        return (self.faces['U'][0][1] == center and 
                self.faces['U'][1][0] == center and 
                self.faces['U'][1][2] == center and 
                self.faces['U'][2][1] == center)

    def is_top_cross_line(self):
        # Check if top cross forms a line
        center = self.faces['U'][1][1]
        return ((self.faces['U'][0][1] == center and self.faces['U'][2][1] == center) or 
                (self.faces['U'][1][0] == center and self.faces['U'][1][2] == center))

    def is_top_cross_L(self):
        # Check if top cross forms an L shape
        center = self.faces['U'][1][1]
        return ((self.faces['U'][0][1] == center and self.faces['U'][1][0] == center) or
                (self.faces['U'][0][1] == center and self.faces['U'][1][2] == center) or
                (self.faces['U'][2][1] == center and self.faces['U'][1][0] == center) or
                (self.faces['U'][2][1] == center and self.faces['U'][1][2] == center))

    def is_top_cross_dot(self):
        # Check if only center is the correct color (dot shape)
        center = self.faces['U'][1][1]
        edges = [self.faces['U'][0][1], self.faces['U'][1][0], 
                self.faces['U'][1][2], self.faces['U'][2][1]]
        return all(edge != center for edge in edges)

    def is_f2l_corner_solved(self):
        # Check if the front-right corner is correctly solved
        front_center = self.faces['F'][1][1]
        right_center = self.faces['R'][1][1]
        down_center = self.faces['D'][1][1]
        
        corner_front = self.faces['F'][2][2]
        corner_right = self.faces['R'][2][0]
        corner_down = self.faces['D'][0][2]
        
        return (corner_front == front_center and 
                corner_right == right_center and 
                corner_down == down_center)

    def is_f2l_edge_solved(self):
        # Check if the front-right edge is correctly solved
        front_center = self.faces['F'][1][1]
        right_center = self.faces['R'][1][1]
        
        edge_front = self.faces['F'][1][2]
        edge_right = self.faces['R'][1][0]
        
        return edge_front == front_center and edge_right == right_center

    def get_top_edge_top(self):
        return self.faces['U'][2][1]

    def get_top_edge_front(self):
        return self.faces['F'][0][1]

    def get_back_edge_top(self):
        return self.faces['U'][0][1]

    def get_back_edge_back(self):
        return self.faces['B'][0][1]

    def get_front_center(self):
        return self.faces['F'][1][1]

    def get_right_center(self):
        return self.faces['R'][1][1]

    def get_back_center(self):
        return self.faces['B'][1][1]

    def get_left_center(self):
        return self.faces['L'][1][1]

    def get_top_center(self):
        return self.faces['U'][1][1]

    def get_bottom_center(self):
        return self.faces['D'][1][1]

    def get_front_color(self):
        return self.faces['F'][2][1]

    def get_right_color(self):
        return self.faces['R'][1][2]

    def get_left_color(self):
        return self.faces['L'][1][0]

    def get_back_color(self):
        return self.faces['B'][0][1]

    def get_bottom_color(self):
        return self.faces['D'][0][1]

    def is_f2l_edge_on_top(self):
        # Check if target edge piece is on top layer
        front_center = self.faces['F'][1][1]
        right_center = self.faces['R'][1][1]
        edge_colors = {self.faces['U'][2][1], self.faces['F'][0][1]}
        return front_center in edge_colors or right_center in edge_colors

    def is_f2l_corner_on_top(self):
        # Check if target corner piece is on top layer
        front_center = self.faces['F'][1][1]
        right_center = self.faces['R'][1][1]
        down_center = self.faces['D'][1][1]
        corner_colors = {
            self.faces['U'][2][2],
            self.faces['F'][0][2],
            self.faces['R'][0][0]
        }
        return (front_center in corner_colors or 
                right_center in corner_colors or 
                down_center in corner_colors)

    def is_f2l_edge_inserted(self):
        # Check if edge is inserted (may not be oriented correctly)
        front_center = self.faces['F'][1][1]
        right_center = self.faces['R'][1][1]
        edge_colors = {self.faces['F'][1][2], self.faces['R'][1][0]}
        return front_center in edge_colors and right_center in edge_colors

    def is_f2l_corner_inserted(self):
        # Check if corner is inserted (may not be oriented correctly)
        front_center = self.faces['F'][1][1]
        right_center = self.faces['R'][1][1]
        down_center = self.faces['D'][1][1]
        corner_colors = {
            self.faces['F'][2][2],
            self.faces['R'][2][0],
            self.faces['D'][0][2]
        }
        return (front_center in corner_colors and 
                right_center in corner_colors and 
                down_center in corner_colors)

    def is_f2l_done(self):
        # Check if all F2L pairs are solved
        centers = {
            'F': self.faces['F'][1][1],
            'R': self.faces['R'][1][1],
            'B': self.faces['B'][1][1],
            'L': self.faces['L'][1][1],
            'D': self.faces['D'][1][1]
        }
        
        # Check all edges
        edges_solved = (
            self.faces['F'][1][2] == centers['F'] and self.faces['R'][1][0] == centers['R'] and
            self.faces['R'][1][2] == centers['R'] and self.faces['B'][1][0] == centers['B'] and
            self.faces['B'][1][2] == centers['B'] and self.faces['L'][1][0] == centers['L'] and
            self.faces['L'][1][2] == centers['L'] and self.faces['F'][1][0] == centers['F']
        )
        
        # Check all corners
        corners_solved = (
            self.faces['F'][2][2] == centers['F'] and self.faces['R'][2][0] == centers['R'] and
            self.faces['R'][2][2] == centers['R'] and self.faces['B'][2][0] == centers['B'] and
            self.faces['B'][2][2] == centers['B'] and self.faces['L'][2][0] == centers['L'] and
            self.faces['L'][2][2] == centers['L'] and self.faces['F'][2][0] == centers['F']
        )
        
        return edges_solved and corners_solved

    def is_solved(self):
        # Check if entire cube is solved
        for face in self.faces:
            center = self.faces[face][1][1]
            for row in self.faces[face]:
                for cell in row:
                    if cell != center:
                        return False
        return True


