import random
import numpy as np
from collections import deque

class RubiksCube:
    # Color mapping: 0:White, 1:Yellow, 2:Green, 3:Blue, 4:Red, 5:Orange
    def __init__(self, state=None):
        # Initialize a solved cube if no state is provided
        if state is None:
            # Create a solved cube with each face having one color
            self.state = np.array([
                [[0, 0, 0], [0, 0, 0], [0, 0, 0]],  # Up (White)
                [[1, 1, 1], [1, 1, 1], [1, 1, 1]],  # Down (Yellow)
                [[2, 2, 2], [2, 2, 2], [2, 2, 2]],  # Front (Green)
                [[3, 3, 3], [3, 3, 3], [3, 3, 3]],  # Back (Blue)
                [[4, 4, 4], [4, 4, 4], [4, 4, 4]],  # Left (Red)
                [[5, 5, 5], [5, 5, 5], [5, 5, 5]]   # Right (Orange)
            ])
        else:
            self.state = np.array(state)
        
        # Define the center pieces (since they never move)
        self.centers = {
            0: 'White',
            1: 'Yellow',
            2: 'Green',
            3: 'Blue',
            4: 'Red',
            5: 'Orange'
        }
        
        # Define the moves
        self.moves = {
            'U': self.U, 'U\'': self.U_prime, 'U2': self.U2,
            'D': self.D, 'D\'': self.D_prime, 'D2': self.D2,
            'F': self.F, 'F\'': self.F_prime, 'F2': self.F2,
            'B': self.B, 'B\'': self.B_prime, 'B2': self.B2,
            'L': self.L, 'L\'': self.L_prime, 'L2': self.L2,
            'R': self.R, 'R\'': self.R_prime, 'R2': self.R2,
            # Wide moves
            'u': self.u, 'u\'': self.u_prime, 'u2': self.u2,
            'd': self.d, 'd\'': self.d_prime, 'd2': self.d2,
            'f': self.f, 'f\'': self.f_prime, 'f2': self.f2,
            'b': self.b, 'b\'': self.b_prime, 'b2': self.b2,
            'l': self.l, 'l\'': self.l_prime, 'l2': self.l2,
            'r': self.r, 'r\'': self.r_prime, 'r2': self.r2,
            # Slice moves
            'M': self.M, 'M\'': self.M_prime, 'M2': self.M2,
            'E': self.E, 'E\'': self.E_prime, 'E2': self.E2,
            'S': self.S, 'S\'': self.S_prime, 'S2': self.S2,
            # Rotations
            'x': self.x, 'x\'': self.x_prime, 'x2': self.x2,
            'y': self.y, 'y\'': self.y_prime, 'y2': self.y2,
            'z': self.z, 'z\'': self.z_prime, 'z2': self.z2
        }
    @staticmethod
    def convert_cube_data(cube_data):
        color_map = {
            'W': 0, 'Y': 1, 'G': 2,
            'B': 3, 'R': 4, 'O': 5
        }

        face_order = ['top', 'bottom', 'front', 'back', 'left', 'right']
        state = []

        for face in face_order:
            face_matrix = [
                [color_map[color] for color in row]
                for row in cube_data[face]
            ]
            state.append(face_matrix)

        return np.array(state)
    
    def copy(self):
        """Create a copy of the current cube state"""
        return RubiksCube(self.state.copy())
    
    def is_solved(self):
        """Check if the cube is solved"""
        for face in range(6):
            color = self.state[face, 0, 0]
            for i in range(3):
                for j in range(3):
                    if self.state[face, i, j] != color:
                        return False
        return True
    
    def _rotate_face_clockwise(self, face):
        """Rotate a face clockwise"""
        self.state[face] = np.rot90(self.state[face], k=3)
    
    def _rotate_face_counterclockwise(self, face):
        """Rotate a face counterclockwise"""
        self.state[face] = np.rot90(self.state[face], k=1)
    
    def _rotate_face_180(self, face):
        """Rotate a face 180 degrees"""
        self.state[face] = np.rot90(self.state[face], k=2)
    
    # Basic moves
    def U(self):
        """Up face clockwise rotation"""
        self._rotate_face_clockwise(0)
        # Rotate the top row of the surrounding faces
        temp = self.state[2, 0, :].copy()
        self.state[2, 0, :] = self.state[5, 0, :]
        self.state[5, 0, :] = self.state[3, 0, :]
        self.state[3, 0, :] = self.state[4, 0, :]
        self.state[4, 0, :] = temp
        return self
    
    def U_prime(self):
        """Up face counterclockwise rotation"""
        self._rotate_face_counterclockwise(0)
        # Rotate the top row of the surrounding faces
        temp = self.state[2, 0, :].copy()
        self.state[2, 0, :] = self.state[4, 0, :]
        self.state[4, 0, :] = self.state[3, 0, :]
        self.state[3, 0, :] = self.state[5, 0, :]
        self.state[5, 0, :] = temp
        return self
    
    def U2(self):
        """Up face double rotation"""
        self._rotate_face_180(0)
        # Swap the top rows of the surrounding faces
        self.state[2, 0, :], self.state[3, 0, :] = self.state[3, 0, :].copy(), self.state[2, 0, :].copy()
        self.state[4, 0, :], self.state[5, 0, :] = self.state[5, 0, :].copy(), self.state[4, 0, :].copy()
        return self
    
    def D(self):
        """Down face clockwise rotation"""
        self._rotate_face_clockwise(1)
        # Rotate the bottom row of the surrounding faces
        temp = self.state[2, 2, :].copy()
        self.state[2, 2, :] = self.state[4, 2, :]
        self.state[4, 2, :] = self.state[3, 2, :]
        self.state[3, 2, :] = self.state[5, 2, :]
        self.state[5, 2, :] = temp
        return self
    
    def D_prime(self):
        """Down face counterclockwise rotation"""
        self._rotate_face_counterclockwise(1)
        # Rotate the bottom row of the surrounding faces
        temp = self.state[2, 2, :].copy()
        self.state[2, 2, :] = self.state[5, 2, :]
        self.state[5, 2, :] = self.state[3, 2, :]
        self.state[3, 2, :] = self.state[4, 2, :]
        self.state[4, 2, :] = temp
        return self
    
    def D2(self):
        """Down face double rotation"""
        self._rotate_face_180(1)
        # Swap the bottom rows of the surrounding faces
        self.state[2, 2, :], self.state[3, 2, :] = self.state[3, 2, :].copy(), self.state[2, 2, :].copy()
        self.state[4, 2, :], self.state[5, 2, :] = self.state[5, 2, :].copy(), self.state[4, 2, :].copy()
        return self
    
    def F(self):
        """Front face clockwise rotation"""
        self._rotate_face_clockwise(2)
        # Rotate the front pieces of the surrounding faces
        temp = self.state[0, 2, :].copy()
        self.state[0, 2, :] = np.flip(self.state[4, :, 2].copy())
        self.state[4, :, 2] = self.state[1, 0, :].copy()
        self.state[1, 0, :] = np.flip(self.state[5, :, 0].copy())
        self.state[5, :, 0] = temp
        return self
    
    def F_prime(self):
        """Front face counterclockwise rotation"""
        self._rotate_face_counterclockwise(2)
        # Rotate the front pieces of the surrounding faces
        temp = self.state[0, 2, :].copy()
        self.state[0, 2, :] = self.state[5, :, 0].copy()
        self.state[5, :, 0] = np.flip(self.state[1, 0, :].copy())
        self.state[1, 0, :] = self.state[4, :, 2].copy()
        self.state[4, :, 2] = np.flip(temp)
        return self
    
    def F2(self):
        """Front face double rotation"""
        self._rotate_face_180(2)
        # Swap pieces of the surrounding faces
        self.state[0, 2, :], self.state[1, 0, :] = np.flip(self.state[1, 0, :].copy()), np.flip(self.state[0, 2, :].copy())
        self.state[4, :, 2], self.state[5, :, 0] = np.flip(self.state[5, :, 0].copy()), np.flip(self.state[4, :, 2].copy())
        return self
    
    def B(self):
        """Back face clockwise rotation"""
        self._rotate_face_clockwise(3)
        # Rotate the back pieces of the surrounding faces
        temp = self.state[0, 0, :].copy()
        self.state[0, 0, :] = self.state[5, :, 2].copy()
        self.state[5, :, 2] = np.flip(self.state[1, 2, :].copy())
        self.state[1, 2, :] = self.state[4, :, 0].copy()
        self.state[4, :, 0] = np.flip(temp)
        return self
    
    def B_prime(self):
        """Back face counterclockwise rotation"""
        self._rotate_face_counterclockwise(3)
        # Rotate the back pieces of the surrounding faces
        temp = self.state[0, 0, :].copy()
        self.state[0, 0, :] = np.flip(self.state[4, :, 0].copy())
        self.state[4, :, 0] = self.state[1, 2, :].copy()
        self.state[1, 2, :] = np.flip(self.state[5, :, 2].copy())
        self.state[5, :, 2] = temp
        return self
    
    def B2(self):
        """Back face double rotation"""
        self._rotate_face_180(3)
        # Swap pieces of the surrounding faces
        self.state[0, 0, :], self.state[1, 2, :] = np.flip(self.state[1, 2, :].copy()), np.flip(self.state[0, 0, :].copy())
        self.state[4, :, 0], self.state[5, :, 2] = np.flip(self.state[5, :, 2].copy()), np.flip(self.state[4, :, 0].copy())
        return self
    
    def L(self):
        """Left face clockwise rotation"""
        self._rotate_face_clockwise(4)
        # Rotate the left pieces of the surrounding faces
        temp = self.state[0, :, 0].copy()
        self.state[0, :, 0] = self.state[3, :, 2].copy()
        self.state[3, :, 2] = np.flip(self.state[1, :, 0].copy())
        self.state[1, :, 0] = self.state[2, :, 0].copy()
        self.state[2, :, 0] = temp
        return self
    
    def L_prime(self):
        """Left face counterclockwise rotation"""
        self._rotate_face_counterclockwise(4)
        # Rotate the left pieces of the surrounding faces
        temp = self.state[0, :, 0].copy()
        self.state[0, :, 0] = self.state[2, :, 0].copy()
        self.state[2, :, 0] = self.state[1, :, 0].copy()
        self.state[1, :, 0] = np.flip(self.state[3, :, 2].copy())
        self.state[3, :, 2] = temp
        return self
    
    def L2(self):
        """Left face double rotation"""
        self._rotate_face_180(4)
        # Swap pieces of the surrounding faces
        self.state[0, :, 0], self.state[1, :, 0] = self.state[1, :, 0].copy(), self.state[0, :, 0].copy()
        self.state[2, :, 0], self.state[3, :, 2] = np.flip(self.state[3, :, 2].copy()), np.flip(self.state[2, :, 0].copy())
        return self
    
    def R(self):
        """Right face clockwise rotation"""
        self._rotate_face_clockwise(5)
        # Rotate the right pieces of the surrounding faces
        temp = self.state[0, :, 2].copy()
        self.state[0, :, 2] = self.state[2, :, 2].copy()
        self.state[2, :, 2] = self.state[1, :, 2].copy()
        self.state[1, :, 2] = np.flip(self.state[3, :, 0].copy())
        self.state[3, :, 0] = temp
        return self
    
    def R_prime(self):
        """Right face counterclockwise rotation"""
        self._rotate_face_counterclockwise(5)
        # Rotate the right pieces of the surrounding faces
        temp = self.state[0, :, 2].copy()
        self.state[0, :, 2] = self.state[3, :, 0].copy()
        self.state[3, :, 0] = np.flip(self.state[1, :, 2].copy())
        self.state[1, :, 2] = self.state[2, :, 2].copy()
        self.state[2, :, 2] = temp
        return self
    
    def R2(self):
        """Right face double rotation"""
        self._rotate_face_180(5)
        # Swap pieces of the surrounding faces
        self.state[0, :, 2], self.state[1, :, 2] = self.state[1, :, 2].copy(), self.state[0, :, 2].copy()
        self.state[2, :, 2], self.state[3, :, 0] = np.flip(self.state[3, :, 0].copy()), np.flip(self.state[2, :, 2].copy())
        return self
    
    # Wide moves (two layers)
    def u(self):
        """Top two layers clockwise"""
        self.U()
        # Move the middle layer same as U
        temp = self.state[2, 1, :].copy()
        self.state[2, 1, :] = self.state[5, 1, :]
        self.state[5, 1, :] = self.state[3, 1, :]
        self.state[3, 1, :] = self.state[4, 1, :]
        self.state[4, 1, :] = temp
        return self
    
    def u_prime(self):
        """Top two layers counterclockwise"""
        self.U_prime()
        # Move the middle layer same as U'
        temp = self.state[2, 1, :].copy()
        self.state[2, 1, :] = self.state[4, 1, :]
        self.state[4, 1, :] = self.state[3, 1, :]
        self.state[3, 1, :] = self.state[5, 1, :]
        self.state[5, 1, :] = temp
        return self
    
    def u2(self):
        """Top two layers double rotation"""
        self.U2()
        # Move the middle layer same as U2
        self.state[2, 1, :], self.state[3, 1, :] = self.state[3, 1, :].copy(), self.state[2, 1, :].copy()
        self.state[4, 1, :], self.state[5, 1, :] = self.state[5, 1, :].copy(), self.state[4, 1, :].copy()
        return self
    
    def d(self):
        """Bottom two layers clockwise"""
        self.D()
        # Move the middle layer same as D
        temp = self.state[2, 1, :].copy()
        self.state[2, 1, :] = self.state[4, 1, :]
        self.state[4, 1, :] = self.state[3, 1, :]
        self.state[3, 1, :] = self.state[5, 1, :]
        self.state[5, 1, :] = temp
        return self
    
    def d_prime(self):
        """Bottom two layers counterclockwise"""
        self.D_prime()
        # Move the middle layer same as D'
        temp = self.state[2, 1, :].copy()
        self.state[2, 1, :] = self.state[5, 1, :]
        self.state[5, 1, :] = self.state[3, 1, :]
        self.state[3, 1, :] = self.state[4, 1, :]
        self.state[4, 1, :] = temp
        return self
    
    def d2(self):
        """Bottom two layers double rotation"""
        self.D2()
        # Move the middle layer same as D2
        self.state[2, 1, :], self.state[3, 1, :] = self.state[3, 1, :].copy(), self.state[2, 1, :].copy()
        self.state[4, 1, :], self.state[5, 1, :] = self.state[5, 1, :].copy(), self.state[4, 1, :].copy()
        return self
    
    def f(self):
        """Front two layers clockwise"""
        self.F()
        # Move the middle layer same as F
        temp = self.state[0, 1, :].copy()
        self.state[0, 1, :] = np.flip(self.state[4, :, 1].copy())
        self.state[4, :, 1] = self.state[1, 1, :].copy()
        self.state[1, 1, :] = np.flip(self.state[5, :, 1].copy())
        self.state[5, :, 1] = temp
        return self
    
    def f_prime(self):
        """Front two layers counterclockwise"""
        self.F_prime()
        # Move the middle layer same as F'
        temp = self.state[0, 1, :].copy()
        self.state[0, 1, :] = self.state[5, :, 1].copy()
        self.state[5, :, 1] = np.flip(self.state[1, 1, :].copy())
        self.state[1, 1, :] = self.state[4, :, 1].copy()
        self.state[4, :, 1] = np.flip(temp)
        return self
    
    def f2(self):
        """Front two layers double rotation"""
        self.F2()
        # Move the middle layer same as F2
        self.state[0, 1, :], self.state[1, 1, :] = np.flip(self.state[1, 1, :].copy()), np.flip(self.state[0, 1, :].copy())
        self.state[4, :, 1], self.state[5, :, 1] = np.flip(self.state[5, :, 1].copy()), np.flip(self.state[4, :, 1].copy())
        return self
    
    def b(self):
        """Back two layers clockwise"""
        self.B()
        # Move the middle layer same as B
        temp = self.state[0, 1, :].copy()
        self.state[0, 1, :] = self.state[5, :, 1].copy()
        self.state[5, :, 1] = np.flip(self.state[1, 1, :].copy())
        self.state[1, 1, :] = self.state[4, :, 1].copy()
        self.state[4, :, 1] = np.flip(temp)
        return self
    
    def b_prime(self):
        """Back two layers counterclockwise"""
        self.B_prime()
        # Move the middle layer same as B'
        temp = self.state[0, 1, :].copy()
        self.state[0, 1, :] = np.flip(self.state[4, :, 1].copy())
        self.state[4, :, 1] = self.state[1, 1, :].copy()
        self.state[1, 1, :] = np.flip(self.state[5, :, 1].copy())
        self.state[5, :, 1] = temp
        return self
    
    def b2(self):
        """Back two layers double rotation"""
        self.B2()
        # Move the middle layer same as B2
        self.state[0, 1, :], self.state[1, 1, :] = np.flip(self.state[1, 1, :].copy()), np.flip(self.state[0, 1, :].copy())
        self.state[4, :, 1], self.state[5, :, 1] = np.flip(self.state[5, :, 1].copy()), np.flip(self.state[4, :, 1].copy())
        return self
    
    def l(self):
        """Left two layers clockwise"""
        self.L()
        # Move the middle layer same as L
        temp = self.state[0, :, 1].copy()
        self.state[0, :, 1] = self.state[3, :, 1].copy()
        self.state[3, :, 1] = np.flip(self.state[1, :, 1].copy())
        self.state[1, :, 1] = self.state[2, :, 1].copy()
        self.state[2, :, 1] = temp
        return self
    
    def l_prime(self):
        """Left two layers counterclockwise"""
        self.L_prime()
        # Move the middle layer same as L'
        temp = self.state[0, :, 1].copy()
        self.state[0, :, 1] = self.state[2, :, 1].copy()
        self.state[2, :, 1] = self.state[1, :, 1].copy()
        self.state[1, :, 1] = np.flip(self.state[3, :, 1].copy())
        self.state[3, :, 1] = temp
        return self
    
    def l2(self):
        """Left two layers double rotation"""
        self.L2()
        # Move the middle layer same as L2
        self.state[0, :, 1], self.state[1, :, 1] = self.state[1, :, 1].copy(), self.state[0, :, 1].copy()
        self.state[2, :, 1], self.state[3, :, 1] = np.flip(self.state[3, :, 1].copy()), np.flip(self.state[2, :, 1].copy())
        return self
    
    def r(self):
        """Right two layers clockwise"""
        self.R()
        # Move the middle layer same as R
        temp = self.state[0, :, 1].copy()
        self.state[0, :, 1] = self.state[2, :, 1].copy()
        self.state[2, :, 1] = self.state[1, :, 1].copy()
        self.state[1, :, 1] = np.flip(self.state[3, :, 1].copy())
        self.state[3, :, 1] = temp
        return self
    
    def r_prime(self):
        """Right two layers counterclockwise"""
        self.R_prime()
        # Move the middle layer same as R'
        temp = self.state[0, :, 1].copy()
        self.state[0, :, 1] = self.state[3, :, 1].copy()
        self.state[3, :, 1] = np.flip(self.state[1, :, 1].copy())
        self.state[1, :, 1] = self.state[2, :, 1].copy()
        self.state[2, :, 1] = temp
        return self
    
    def r2(self):
        """Right two layers double rotation"""
        self.R2()
        # Move the middle layer same as R2
        self.state[0, :, 1], self.state[1, :, 1] = self.state[1, :, 1].copy(), self.state[0, :, 1].copy()
        self.state[2, :, 1], self.state[3, :, 1] = np.flip(self.state[3, :, 1].copy()), np.flip(self.state[2, :, 1].copy())
        return self
    
    # Slice moves (middle layer only)
    def M(self):
        """Middle slice clockwise (same direction as L)"""
        # Move the middle layer same as L
        temp = self.state[0, :, 1].copy()
        self.state[0, :, 1] = self.state[3, :, 1].copy()
        self.state[3, :, 1] = np.flip(self.state[1, :, 1].copy())
        self.state[1, :, 1] = self.state[2, :, 1].copy()
        self.state[2, :, 1] = temp
        return self
    
    def M_prime(self):
        """Middle slice counterclockwise (same direction as L')"""
        # Move the middle layer same as L'
        temp = self.state[0, :, 1].copy()
        self.state[0, :, 1] = self.state[2, :, 1].copy()
        self.state[2, :, 1] = self.state[1, :, 1].copy()
        self.state[1, :, 1] = np.flip(self.state[3, :, 1].copy())
        self.state[3, :, 1] = temp
        return self
    
    def M2(self):
        """Middle slice double rotation"""
        # Move the middle layer same as L2
        self.state[0, :, 1], self.state[1, :, 1] = self.state[1, :, 1].copy(), self.state[0, :, 1].copy()
        self.state[2, :, 1], self.state[3, :, 1] = np.flip(self.state[3, :, 1].copy()), np.flip(self.state[2, :, 1].copy())
        return self
    
    def E(self):
        """Equator slice clockwise (same direction as D)"""
        # Move the middle layer same as D
        temp = self.state[2, 1, :].copy()
        self.state[2, 1, :] = self.state[4, 1, :]
        self.state[4, 1, :] = self.state[3, 1, :]
        self.state[3, 1, :] = self.state[5, 1, :]
        self.state[5, 1, :] = temp
        return self
    
    def E_prime(self):
        """Equator slice counterclockwise (same direction as D')"""
        # Move the middle layer same as D'
        temp = self.state[2, 1, :].copy()
        self.state[2, 1, :] = self.state[5, 1, :]
        self.state[5, 1, :] = self.state[3, 1, :]
        self.state[3, 1, :] = self.state[4, 1, :]
        self.state[4, 1, :] = temp
        return self
    
    def E2(self):
        """Equator slice double rotation"""
        # Move the middle layer same as D2
        self.state[2, 1, :], self.state[3, 1, :] = self.state[3, 1, :].copy(), self.state[2, 1, :].copy()
        self.state[4, 1, :], self.state[5, 1, :] = self.state[5, 1, :].copy(), self.state[4, 1, :].copy()
        return self
    
    def S(self):
        """Standing slice clockwise (same direction as F)"""
        # Move the middle layer same as F
        temp = self.state[0, 1, :].copy()
        self.state[0, 1, :] = np.flip(self.state[4, :, 1].copy())
        self.state[4, :, 1] = self.state[1, 1, :].copy()
        self.state[1, 1, :] = np.flip(self.state[5, :, 1].copy())
        self.state[5, :, 1] = temp
        return self
    
    def S_prime(self):
        """Standing slice counterclockwise (same direction as F')"""
        # Move the middle layer same as F'
        temp = self.state[0, 1, :].copy()
        self.state[0, 1, :] = self.state[5, :, 1].copy()
        self.state[5, :, 1] = np.flip(self.state[1, 1, :].copy())
        self.state[1, 1, :] = self.state[4, :, 1].copy()
        self.state[4, :, 1] = np.flip(temp)
        return self
    
    def S2(self):
        """Standing slice double rotation"""
        # Move the middle layer same as F2
        self.state[0, 1, :], self.state[1, 1, :] = np.flip(self.state[1, 1, :].copy()), np.flip(self.state[0, 1, :].copy())
        self.state[4, :, 1], self.state[5, :, 1] = np.flip(self.state[5, :, 1].copy()), np.flip(self.state[4, :, 1].copy())
        return self
    
    # Cube rotations
    def x(self):
        """Rotate entire cube on R axis (as if doing R)"""
        # Store current state
        current = self.state.copy()
        
        # Up face becomes Front face
        self.state[2] = current[0]
        # Front face becomes Down face
        self.state[1] = current[2]
        # Down face becomes Back face (rotated 180)
        self.state[3] = np.rot90(current[1], k=2)
        # Back face becomes Up face (rotated 180)
        self.state[0] = np.rot90(current[3], k=2)
        
        # Left face rotated 90 counterclockwise
        self.state[4] = np.rot90(current[4], k=1)
        # Right face rotated 90 clockwise
        self.state[5] = np.rot90(current[5], k=3)
        
        return self
    
    def x_prime(self):
        """Rotate entire cube on R axis counterclockwise (as if doing R')"""
        # Store current state
        current = self.state.copy()
        
        # Front face becomes Up face
        self.state[0] = current[2]
        # Down face becomes Front face
        self.state[2] = current[1]
        # Back face becomes Down face (rotated 180)
        self.state[1] = np.rot90(current[3], k=2)
        # Up face becomes Back face (rotated 180)
        self.state[3] = np.rot90(current[0], k=2)
        
        # Left face rotated 90 clockwise
        self.state[4] = np.rot90(current[4], k=3)
        # Right face rotated 90 counterclockwise
        self.state[5] = np.rot90(current[5], k=1)
        
        return self
        
    def x2(self):
        """Rotate entire cube on R axis twice"""
        return self.x().x()
        
    def y(self):
        """Rotate entire cube on U axis clockwise"""
        # Store current state
        current = self.state.copy()
        
        # Front becomes Right
        self.state[5] = current[2]
        # Right becomes Back
        self.state[3] = current[5]
        # Back becomes Left
        self.state[4] = current[3]
        # Left becomes Front
        self.state[2] = current[4]
        
        # Up face rotated 90 clockwise
        self.state[0] = np.rot90(current[0], k=3)
        # Down face rotated 90 counterclockwise
        self.state[1] = np.rot90(current[1], k=1)
        
        return self
    
    def y_prime(self):
        """Rotate entire cube on U axis counterclockwise"""
        # Store current state
        current = self.state.copy()
        
        # Front becomes Left
        self.state[4] = current[2]
        # Right becomes Front
        self.state[2] = current[5]
        # Back becomes Right
        self.state[5] = current[3]
        # Left becomes Back
        self.state[3] = current[4]
        
        # Up face rotated 90 counterclockwise
        self.state[0] = np.rot90(current[0], k=1)
        # Down face rotated 90 clockwise
        self.state[1] = np.rot90(current[1], k=3)
        
        return self
    
    def y2(self):
        """Rotate entire cube on U axis twice"""
        return self.y().y()
    
    def z(self):
        """Rotate entire cube on F axis clockwise"""
        # Store current state
        current = self.state.copy()
        
        # Up becomes Left (rotated clockwise)
        self.state[4] = np.rot90(current[0], k=3)
        # Right becomes Up (rotated counterclockwise)
        self.state[0] = np.rot90(current[5], k=1)
        # Down becomes Right (rotated clockwise)
        self.state[5] = np.rot90(current[1], k=3)
        # Left becomes Down (rotated counterclockwise)
        self.state[1] = np.rot90(current[4], k=1)
        
        # Front face rotated 90 clockwise
        self.state[2] = np.rot90(current[2], k=3)
        # Back face rotated 90 counterclockwise
        self.state[3] = np.rot90(current[3], k=1)
        
        return self
    
    def z_prime(self):
        """Rotate entire cube on F axis counterclockwise"""
        # Store current state
        current = self.state.copy()
        
        # Up becomes Right (rotated clockwise)
        self.state[5] = np.rot90(current[0], k=3)
        # Right becomes Down (rotated counterclockwise)
        self.state[1] = np.rot90(current[5], k=1)
        # Down becomes Left (rotated clockwise)
        self.state[4] = np.rot90(current[1], k=3)
        # Left becomes Up (rotated counterclockwise)
        self.state[0] = np.rot90(current[4], k=1)
        
        # Front face rotated 90 counterclockwise
        self.state[2] = np.rot90(current[2], k=1)
        # Back face rotated 90 clockwise
        self.state[3] = np.rot90(current[3], k=3)
        
        return self
    
    def z2(self):
        """Rotate entire cube on F axis twice"""
        return self.z().z()
    
    def apply_moves(self, moves_str):
        """Apply a sequence of moves"""
        if not moves_str:
            return self
            
        moves_list = moves_str.split()
        for move in moves_list:
            if move in self.moves:
                self.moves[move]()
            else:
                raise ValueError(f"Unknown move: {move}")
        return self
    
    def shuffle(self, num_moves=20):
        """Shuffle the cube with random moves"""
        available_moves = ['U', 'U\'', 'U2', 'D', 'D\'', 'D2', 
                        'F', 'F\'', 'F2', 'B', 'B\'', 'B2', 
                        'L', 'L\'', 'L2', 'R', 'R\'', 'R2']
        
        moves = []
        prev_face = None
        
        for _ in range(num_moves):
            # Avoid repeated moves on the same face
            while True:
                move = random.choice(available_moves)
                face = move[0]
                if face != prev_face:
                    break
            
            moves.append(move)
            prev_face = move[0]
            self.moves[move]()
        
        return ' '.join(moves)
    
    def get_color_name(self, color_id):
        """Get the color name from the color ID"""
        colors = {
            0: 'White',
            1: 'Yellow',
            2: 'Green',
            3: 'Blue',
            4: 'Red',
            5: 'Orange'
        }
        return colors.get(color_id, 'Unknown')
    
    def print_cube(self):
        """Print the current state of the cube in a readable format"""
        face_names = ['Up (White)', 'Down (Yellow)', 'Front (Green)', 
                    'Back (Blue)', 'Left (Red)', 'Right (Orange)']
        
        for i, face in enumerate(self.state):
            print(f"\n{face_names[i]}:")
            for row in face:
                row_colors = [self.get_color_name(c)[0] for c in row]
                print(' '.join(row_colors))
    
    def find_piece(self, *colors):
        """Find the position of a specific piece (edge or corner) by its colors"""
        colors = sorted(colors)
        
        # Dictionary to store piece locations and their colors
        pieces = {}
        
        # Centers
        centers = [(0, 1, 1), (1, 1, 1), (2, 1, 1), (3, 1, 1), (4, 1, 1), (5, 1, 1)]
        for face, i, j in centers:
            pieces[(face, i, j)] = [self.state[face, i, j]]
        
        # Edges
        edges = [
            # Up face edges
            (0, 0, 1), (0, 1, 0), (0, 1, 2), (0, 2, 1),
            # Down face edges
            (1, 0, 1), (1, 1, 0), (1, 1, 2), (1, 2, 1),
            # Middle layer edges
            (2, 1, 0), (2, 1, 2), (3, 1, 0), (3, 1, 2)
        ]
        
        edge_neighbors = {
            (0, 0, 1): (3, 0, 1), (0, 1, 0): (4, 0, 1), (0, 1, 2): (5, 0, 1), (0, 2, 1): (2, 0, 1),
            (1, 0, 1): (2, 2, 1), (1, 1, 0): (4, 2, 1), (1, 1, 2): (5, 2, 1), (1, 2, 1): (3, 2, 1),
            (2, 1, 0): (4, 1, 2), (2, 1, 2): (5, 1, 0), (3, 1, 0): (5, 1, 2), (3, 1, 2): (4, 1, 0)
        }
        
        for pos in edges:
            neighbor_pos = edge_neighbors[pos]
            color1 = self.state[pos]
            color2 = self.state[neighbor_pos]
            piece_colors = sorted([color1, color2])
            pieces[pos] = piece_colors
        
        # Corners
        corners = [
            (0, 0, 0), (0, 0, 2), (0, 2, 0), (0, 2, 2),
            (1, 0, 0), (1, 0, 2), (1, 2, 0), (1, 2, 2)
        ]
        
        corner_neighbors = {
            (0, 0, 0): [(3, 0, 2), (4, 0, 0)], (0, 0, 2): [(3, 0, 0), (5, 0, 2)],
            (0, 2, 0): [(2, 0, 0), (4, 0, 2)], (0, 2, 2): [(2, 0, 2), (5, 0, 0)],
            (1, 0, 0): [(2, 2, 0), (4, 2, 2)], (1, 0, 2): [(2, 2, 2), (5, 2, 0)],
            (1, 2, 0): [(3, 2, 2), (4, 2, 0)], (1, 2, 2): [(3, 2, 0), (5, 2, 2)]
        }
        
        for pos in corners:
            neighbor_pos = corner_neighbors[pos]
            color1 = self.state[pos]
            color2 = self.state[neighbor_pos[0]]
            color3 = self.state[neighbor_pos[1]]
            piece_colors = sorted([color1, color2, color3])
            pieces[pos] = piece_colors
        
        # Find the piece with the specified colors
        for pos, piece_colors in pieces.items():
            if piece_colors == colors:
                return pos
        
        return None


class CFOPSolver:
    def __init__(self, cube=None):
        if cube is None:
            self.cube = RubiksCube()
        else:
            self.cube = cube
        
        # OLL algorithms
        self.oll_algorithms = {
            # Cross cases (All edges oriented correctly)
            'OLL 1': "R U2 R2 F R F' U2 R' F R F'",  # Dot
            'OLL 2': "F R U R' U' F' f R U R' U' f'",  # Awkward shape
            'OLL 3': "f R U R' U' f' U' F R U R' U' F'",  # Awkward shape
            'OLL 4': "f R U R' U' f'",  # P shape
            'OLL 5': "R U R' U R U' R' U R U2 R'",  # T shape
            'OLL 6': "R U2 R' U' R U' R'",  # C shape
            'OLL 7': "R U R' U R U2 R'",  # Sune
            'OLL 8': "R U2 R' U' R U R' U' R U' R'",  # Anti-Sune
            'OLL 9': "R U R' U' R' F R2 U R' U' F'",  # Kite
            'OLL 10': "R U R' U R' F R F' R U2 R'",  # Awkward shape
            'OLL 11': "r U R' U R U2 r'",  # Small lightning bolt
            'OLL 12': "F R U R' U' F'",  # Small lightning bolt
            'OLL 13': "F U R U' R' F'",  # Knight move shape
            'OLL 14': "R' F R U R' F' R F U' F'",  # Knight move shape
            'OLL 15': "r' U' r R' U' R U r' U r",  # Box shape
            'OLL 16': "r U r' R U R' U' r U' r'",  # Box shape
            'OLL 17': "R U R' U R' F R F' U2 R' F R F'",  # Dot
            'OLL 18': "r U R' U R U2 r'",  # Fish shape
            'OLL 19': "r' U2 R U R' U r",  # Fish shape
            'OLL 20': "r U R' U' r' F R F'",  # W shape
            'OLL 21': "R U2 R' U' R U R' U' R U' R'",  # H shape
            'OLL 22': "R U2 R2 U' R2 U' R2 U2 R",  # Pi shape
            'OLL 23': "R2 D' R U2 R' D R U2 R",  # L shape
            'OLL 24': "r U R' U' r' F R F'",  # T shape
            'OLL 25': "F' r U R' U' r' F R",  # C shape
            'OLL 26': "R U2 R' U' R U' R'",  # P shape
            'OLL 27': "R U R' U R U2 R'",  # Fish shape
            'OLL 28': "r U R' U' M U R U' R'",  # W shape
            'OLL 29': "R U R' U' R U' R' F' U' F R U R'",  # Fish shape
            'OLL 30': "F R U R' U' F'",  # P shape
            'OLL 31': "R' U' F U R U' R' F' R",  # L shape
            'OLL 32': "L U F' U' L' U L F L'",  # Knight move shape
            'OLL 33': "R U R' U' R' F R F'",  # T shape
            'OLL 34': "R U R2 U' R' F R U R U' F'",  # C shape
            'OLL 35': "R U2 R2 F R F' R U2 R'",  # Fish shape
            'OLL 36': "L' U' L U' L' U L U L F' L' F",  # W shape
            'OLL 37': "F R U' R' U' R U R' F'",  # Fish shape
            'OLL 38': "R U R' U R U' R' U' R' F R F'",  # W shape
            'OLL 39': "L F' L' U' L U F U' L'",  # Fish shape
            'OLL 40': "R' F R U R' U' F' U R",  # Knight move shape
            'OLL 41': "R U R' U R U2 R' F R U R' U' F'",  # Awkward shape
            'OLL 42': "R' U' R U' R' U2 R F R U R' U' F'",  # Awkward shape
            'OLL 43': "R' U' F' U F R",  # Small lightning bolt
            'OLL 44': "F U R U' R' F'",  # Small lightning bolt
            'OLL 45': "F R U R' U' F'",  # Cross
            'OLL 46': "R' U' R' F R F' U R",  # Cross
            'OLL 47': "F' L' U' L U L' U' L U F",  # Cross
            'OLL 48': "F R U R' U' R U R' U' F'",  # Cross
            'OLL 49': "r U' r2 U r2 U r2 U' r",  # Box shape
            'OLL 50': "r' U r2 U' r2 U' r2 U r'",  # Box shape
            'OLL 51': "F U R U' R' U R U' R' F'",  # Cross
            'OLL 52': "R U R' U R U' B U' B' R'",  # Cross
            'OLL 53': "r' U' R U' R' U R U' R' U2 r",  # L shape
            'OLL 54': "r U R' U R U' R' U R U2 r'",  # L shape
            'OLL 55': "R' F R U R U' R2 F' R2 U' R' U R U R'",  # Pi shape
            'OLL 56': "r' U' r U' R' U R U' R' U M' U r",  # H shape
            'OLL 57': "R U R' U' M' U R U' r'"  # Cross
        }
        
        # PLL algorithms
        self.pll_algorithms = {
            # Edge permutation
            'Ua': "R U' R U R U R U' R' U' R2",  # U-perm a
            'Ub': "R2 U R U R' U' R' U' R' U R'",  # U-perm b
            'Z': "M2 U M2 U M' U2 M2 U2 M'",  # Z-perm
            'H': "M2 U M2 U2 M2 U M2",  # H-perm
            # Corner permutation
            'Aa': "x L2 D2 L' U' L D2 L' U L' x'",  # A-perm a
            'Ab': "x L' U L' D2 L U' L' D2 L2 x'",  # A-perm b
            'E': "x' L' U L D' L' U' L D L' U' L D' L' U L D x",  # E-perm
            # Corner + Edge permutation
            'F': "R' U' F' R U R' U' R' F R2 U' R' U' R U R' U R",  # F-perm
            'Ga': "R2 U R' U R' U' R U' R2 D U' R' U R D'",  # G-perm a
            'Gb': "R' U' R U D' R2 U R' U R U' R U' R2 D",  # G-perm b
            'Gc': "R2 U' R U' R U R' U R2 D' U R U' R' D",  # G-perm c
            'Gd': "R U R' U' D R2 U' R U' R' U R' U R2 D'",  # G-perm d
            'Ja': "x R2 F R F' R U2 r' U r U2 x'",  # J-perm a
            'Jb': "R U R' F' R U R' U' R' F R2 U' R'",  # J-perm b
            'Na': "L U' R U2 L' U R' L U' R U2 L' U R'",  # N-perm a
            'Nb': "R' U L' U2 R U' L R' U L' U2 R U' L",  # N-perm b
            'Ra': "L U2 L' U2 L F' L' U' L U L F L2",  # R-perm a
            'Rb': "R' U2 R U2 R' F R U R' U' R' F' R2",  # R-perm b
            'T': "R U R' U' R' F R2 U' R' U' R U R' F'",  # T-perm
            'V': "R' U R' d' R' F' R2 U' R' U R' F R F",  # V-perm
            'Y': "F R U' R' U' R U R' F' R U R' U' R' F R F'"  # Y-perm
        }
        
    def solve(self):
        """Solve the cube using CFOP method"""
        # Store solution steps
        solution = []
        
        # Step 1: Cross
        cross_solution = self.solve_cross()
        solution.append(("Cross", cross_solution))
        
        # Step 2: F2L (First Two Layers)
        f2l_solution = self.solve_f2l()
        solution.append(("F2L", f2l_solution))
        
        # Step 3: OLL (Orientation of Last Layer)
        oll_solution = self.solve_oll()
        solution.append(("OLL", oll_solution))
        
        # Step 4: PLL (Permutation of Last Layer)
        pll_solution = self.solve_pll()
        solution.append(("PLL", pll_solution))
        
        return solution
    
    def solve_cross(self):
        """Solve the white cross on the bottom face"""
        # For simplicity, we'll solve the white cross on the bottom face (Down face)
        # First, make sure white is on bottom
        solution_steps = []
        
        # Rotate the cube to put white face on the bottom
        while self.cube.state[1, 1, 1] != 0:  # White center
            solution_steps.append("x")
            self.cube.x()
        
        # Find and solve each white edge piece
        for target_face in [2, 5, 3, 4]:  # Front, Right, Back, Left
            # Find white edge piece
            target_color = self.cube.state[target_face, 1, 1]
            edge_solved = False
            
            # Check if the edge is already solved
            if (self.cube.state[1, 0, 1] == 0 and self.cube.state[2, 2, 1] == target_color and target_face == 2):
                edge_solved = True
            elif (self.cube.state[1, 1, 2] == 0 and self.cube.state[5, 2, 1] == target_color and target_face == 5):
                edge_solved = True
            elif (self.cube.state[1, 2, 1] == 0 and self.cube.state[3, 2, 1] == target_color and target_face == 3):
                edge_solved = True
            elif (self.cube.state[1, 1, 0] == 0 and self.cube.state[4, 2, 1] == target_color and target_face == 4):
                edge_solved = True
            
            if edge_solved:
                continue
            
            # Search for white edge piece
            white_edge_found = False
            
            # Check top layer edges
            if self.cube.state[0, 0, 1] == 0:
                if self.cube.state[3, 0, 1] == target_color:
                    solution_steps.append("B2")
                    self.cube.B2()
                    white_edge_found = True
            
            if not white_edge_found and self.cube.state[0, 1, 0] == 0:
                if self.cube.state[4, 0, 1] == target_color:
                    solution_steps.append("L2")
                    self.cube.L2()
                    white_edge_found = True
            
            if not white_edge_found and self.cube.state[0, 1, 2] == 0:
                if self.cube.state[5, 0, 1] == target_color:
                    solution_steps.append("R2")
                    self.cube.R2()
                    white_edge_found = True
            
            if not white_edge_found and self.cube.state[0, 2, 1] == 0:
                if self.cube.state[2, 0, 1] == target_color:
                    solution_steps.append("F2")
                    self.cube.F2()
                    white_edge_found = True
            
            # Check middle layer edges
            if not white_edge_found and self.cube.state[2, 1, 0] == 0:
                solution_steps.append("L' D' L")
                self.cube.apply_moves("L' D' L")
                white_edge_found = True
            
            if not white_edge_found and self.cube.state[2, 1, 2] == 0:
                solution_steps.append("R D R'")
                self.cube.apply_moves("R D R'")
                white_edge_found = True
            
            if not white_edge_found and self.cube.state[3, 1, 0] == 0:
                solution_steps.append("R' D' R")
                self.cube.apply_moves("R' D' R")
                white_edge_found = True
            
            if not white_edge_found and self.cube.state[3, 1, 2] == 0:
                solution_steps.append("L D L'")
                self.cube.apply_moves("L D L'")
                white_edge_found = True
            
            if not white_edge_found and self.cube.state[4, 1, 0] == 0:
                solution_steps.append("B' D' B")
                self.cube.apply_moves("B' D' B")
                white_edge_found = True
            
            if not white_edge_found and self.cube.state[4, 1, 2] == 0:
                solution_steps.append("F D F'")
                self.cube.apply_moves("F D F'")
                white_edge_found = True
            
            if not white_edge_found and self.cube.state[5, 1, 0] == 0:
                solution_steps.append("F' D' F")
                self.cube.apply_moves("F' D' F")
                white_edge_found = True
            
            if not white_edge_found and self.cube.state[5, 1, 2] == 0:
                solution_steps.append("B D B'")
                self.cube.apply_moves("B D B'")
                white_edge_found = True
            
            # Check bottom layer edges, but flipped
            if not white_edge_found and self.cube.state[2, 2, 1] == 0:
                solution_steps.append("F' D2 F")
                self.cube.apply_moves("F' D2 F")
                white_edge_found = True
            
            if not white_edge_found and self.cube.state[3, 2, 1] == 0:
                solution_steps.append("B' D2 B")
                self.cube.apply_moves("B' D2 B")
                white_edge_found = True
            
            if not white_edge_found and self.cube.state[4, 2, 1] == 0:
                solution_steps.append("L' D2 L")
                self.cube.apply_moves("L' D2 L")
                white_edge_found = True
            
            if not white_edge_found and self.cube.state[5, 2, 1] == 0:
                solution_steps.append("R' D2 R")
                self.cube.apply_moves("R' D2 R")
                white_edge_found = True
            
            # Rotate to bring edge piece to target face
            while target_face != 2:  # Rotate until target face is front
                solution_steps.append("y")
                self.cube.y()
                target_face = (target_face - 1) % 4 + 2  # Adjust target face
            
            # Insert edge piece to solve the cross
            if self.cube.state[1, 0, 1] == 0 and self.cube.state[2, 2, 1] == self.cube.state[2, 1, 1]:
                # Edge already solved
                pass
            else:
                # Bring edge to correct position
                solution_steps.append("F2")
                self.cube.F2()
        
        return " ".join(solution_steps)

    def solve_f2l(self):
        """Solve the First Two Layers"""
        solution_steps = []
        
        # Solve each F2L corner-edge pair
        for _ in range(4):
            # Find the corner and edge pieces for this slot
            front_color = self.cube.state[2, 1, 1]  # Front center color
            right_color = self.cube.state[5, 1, 1]  # Right center color
            
            # Find the corresponding corner and edge pieces
            corner_solved = False
            edge_solved = False
            
            # Check if corner is already solved
            if (self.cube.state[1, 0, 2] == 0 and 
                self.cube.state[2, 2, 2] == front_color and 
                self.cube.state[5, 2, 0] == right_color):
                corner_solved = True
            
            # Check if edge is already solved
            if (self.cube.state[2, 1, 2] == front_color and 
                self.cube.state[5, 1, 0] == right_color):
                edge_solved = True
            
            # If both pieces are solved, move to next slot
            if corner_solved and edge_solved:
                solution_steps.append("y")
                self.cube.y()
                continue
            
            # Find and solve corner piece if not solved
            if not corner_solved:
                # Look for white-front-right corner
                
                # 1. Check if corner is in top layer
                corner_in_top = False
                
                # Check each corner position in top layer
                for corner_pos in [(0, 0, 0), (0, 0, 2), (0, 2, 0), (0, 2, 2)]:
                    colors = []
                    colors.append(self.cube.state[corner_pos])
                    
                    # Calculate adjacent faces for this corner
                    face1, face2 = None, None
                    if corner_pos == (0, 0, 0):  # Back-Left-Up
                        face1, face2 = (3, 0, 2), (4, 0, 0)
                    elif corner_pos == (0, 0, 2):  # Back-Right-Up
                        face1, face2 = (3, 0, 0), (5, 0, 2)
                    elif corner_pos == (0, 2, 0):  # Front-Left-Up
                        face1, face2 = (2, 0, 0), (4, 0, 2)
                    elif corner_pos == (0, 2, 2):  # Front-Right-Up
                        face1, face2 = (2, 0, 2), (5, 0, 0)
                    
                    colors.append(self.cube.state[face1])
                    colors.append(self.cube.state[face2])
                    
                    # Check if this corner contains the colors we're looking for
                    if 0 in colors and front_color in colors and right_color in colors:
                        # Position corner over its slot
                        while corner_pos[2] != 2 or corner_pos[1] != 2:  # Not Front-Right-Up
                            solution_steps.append("U")
                            self.cube.U()
                            # Recalculate corner_pos after rotation
                            if corner_pos == (0, 0, 0):
                                corner_pos = (0, 0, 2)
                            elif corner_pos == (0, 0, 2):
                                corner_pos = (0, 2, 2)
                            elif corner_pos == (0, 2, 2):
                                corner_pos = (0, 2, 0)
                            elif corner_pos == (0, 2, 0):
                                corner_pos = (0, 0, 0)
                        
                        corner_in_top = True
                        break
                
                # 2. Check if corner is in its slot but wrongly oriented
                if not corner_in_top and not corner_solved:
                    # If corner is in position but wrong orientation, take it out
                    if (0 in [self.cube.state[1, 0, 2], self.cube.state[2, 2, 2], self.cube.state[5, 2, 0]] and
                        front_color in [self.cube.state[1, 0, 2], self.cube.state[2, 2, 2], self.cube.state[5, 2, 0]] and
                        right_color in [self.cube.state[1, 0, 2], self.cube.state[2, 2, 2], self.cube.state[5, 2, 0]]):
                        
                        # Use a common algorithm to take out the corner to the top layer
                        solution_steps.append("R U R'")
                        self.cube.apply_moves("R U R'")
                        corner_in_top = True
                
                # 3. Check corners in other slots (remaining F2L positions)
                if not corner_in_top and not corner_solved:
                    # Look in other F2L slots and move to top layer if found
                    for i in range(3):  # Check other 3 slots
                        solution_steps.append("y")
                        self.cube.y()
                        
                        # Check if our corner is in this slot
                        if (0 in [self.cube.state[1, 0, 2], self.cube.state[2, 2, 2], self.cube.state[5, 2, 0]] and
                            front_color in [self.cube.state[1, 0, 2], self.cube.state[2, 2, 2], self.cube.state[5, 2, 0]] and
                            right_color in [self.cube.state[1, 0, 2], self.cube.state[2, 2, 2], self.cube.state[5, 2, 0]]):
                            
                            # Take it out to top layer
                            solution_steps.append("R U R'")
                            self.cube.apply_moves("R U R'")
                            corner_in_top = True
                            break
                    
                    # Return to original position
                    for _ in range(i + 1):
                        solution_steps.append("y'")
                        self.cube.y_prime()
                
                # Insert corner - basic insertion based on corner orientation
                if corner_in_top:
                    # Get corner orientation (which face has the white sticker)
                    white_on_top = self.cube.state[0, 2, 2] == 0
                    white_on_front = self.cube.state[2, 0, 2] == 0
                    white_on_right = self.cube.state[5, 0, 0] == 0
                    
                    # Apply appropriate algorithm based on orientation
                    if white_on_top:
                        solution_steps.append("R U2 R' U' R U R'")
                        self.cube.apply_moves("R U2 R' U' R U R'")
                    elif white_on_front:
                        solution_steps.append("R U R'")
                        self.cube.apply_moves("R U R'")
                    elif white_on_right:
                        solution_steps.append("U' R' U R")
                        self.cube.apply_moves("U' R' U R")
            
            # Find and solve edge piece if not solved
            if not edge_solved:
                # Look for front-right edge
                
                # 1. Check if edge is in top layer
                edge_in_top = False
                
                # Check each edge position in top layer
                for edge_pos in [(0, 0, 1), (0, 1, 0), (0, 1, 2), (0, 2, 1)]:
                    colors = []
                    colors.append(self.cube.state[edge_pos])
                    
                    # Calculate adjacent face for this edge
                    adjacent_face = None
                    if edge_pos == (0, 0, 1):  # Back-Up
                        adjacent_face = (3, 0, 1)
                    elif edge_pos == (0, 1, 0):  # Left-Up
                        adjacent_face = (4, 0, 1)
                    elif edge_pos == (0, 1, 2):  # Right-Up
                        adjacent_face = (5, 0, 1)
                    elif edge_pos == (0, 2, 1):  # Front-Up
                        adjacent_face = (2, 0, 1)
                    
                    colors.append(self.cube.state[adjacent_face])
                    
                    # Check if this edge contains the colors we're looking for
                    if front_color in colors and right_color in colors:
                        # Position edge over its slot (Front-Right)
                        while edge_pos != (0, 2, 1) and edge_pos != (0, 1, 2):
                            solution_steps.append("U")
                            self.cube.U()
                            # Recalculate edge_pos after rotation
                            if edge_pos == (0, 0, 1):
                                edge_pos = (0, 1, 0)
                            elif edge_pos == (0, 1, 0):
                                edge_pos = (0, 2, 1)
                            elif edge_pos == (0, 2, 1):
                                edge_pos = (0, 1, 2)
                            elif edge_pos == (0, 1, 2):
                                edge_pos = (0, 0, 1)
                        
                        edge_in_top = True
                        break
                
                # 2. Check if edge is in other slots
                if not edge_in_top and not edge_solved:
                    # Look in other F2L edge positions
                    for i in range(3):  # Check other 3 slots
                        solution_steps.append("y")
                        self.cube.y()
                        
                        # If our edge is in this slot, take it out
                        if (front_color in [self.cube.state[2, 1, 2], self.cube.state[5, 1, 0]] and
                            right_color in [self.cube.state[2, 1, 2], self.cube.state[5, 1, 0]]):
                            
                            # Take it out to top layer
                            solution_steps.append("R U' R' U")
                            self.cube.apply_moves("R U' R' U")
                            edge_in_top = True
                            break
                    
                    # Return to original position
                    for _ in range(i + 1):
                        solution_steps.append("y'")
                        self.cube.y_prime()
                
                # Insert edge - basic insertion based on edge orientation
                if edge_in_top:
                    # Determine the orientation
                    if edge_pos == (0, 2, 1):  # Edge is at Front-Up
                        if self.cube.state[0, 2, 1] == front_color:  # Front color on top
                            solution_steps.append("U R U' R' U' F' U F")
                            self.cube.apply_moves("U R U' R' U' F' U F")
                        else:  # Right color on top
                            solution_steps.append("U' F' U F")
                            self.cube.apply_moves("U' F' U F")
                    elif edge_pos == (0, 1, 2):  # Edge is at Right-Up
                        if self.cube.state[0, 1, 2] == front_color:  # Front color on top
                            solution_steps.append("F' U' F")
                            self.cube.apply_moves("F' U' F")
                        else:  # Right color on top
                            solution_steps.append("R U R'")
                            self.cube.apply_moves("R U R'")
            
            # Move to next slot
            solution_steps.append("y")
            self.cube.y()
        
        return " ".join(solution_steps)

    def _get_oll_case(self):
        """Identify the OLL case based on the orientation of last layer pieces"""
        # Simplified implementation - this would typically analyze the top face
        # to determine which specific OLL case we have
        
        # For this implementation, we'll just use a random OLL algorithm
        # In a complete solver, you would detect the pattern and return the correct case
        
        # Check if cross is already formed (all edges oriented correctly)
        edges_oriented = (self.cube.state[0, 0, 1] == self.cube.state[0, 1, 1] and
                        self.cube.state[0, 1, 0] == self.cube.state[0, 1, 1] and
                        self.cube.state[0, 1, 2] == self.cube.state[0, 1, 1] and
                        self.cube.state[0, 2, 1] == self.cube.state[0, 1, 1])
        
        # Count correctly oriented corners
        corners_oriented = 0
        if self.cube.state[0, 0, 0] == self.cube.state[0, 1, 1]:
            corners_oriented += 1
        if self.cube.state[0, 0, 2] == self.cube.state[0, 1, 1]:
            corners_oriented += 1
        if self.cube.state[0, 2, 0] == self.cube.state[0, 1, 1]:
            corners_oriented += 1
        if self.cube.state[0, 2, 2] == self.cube.state[0, 1, 1]:
            corners_oriented += 1
        
        # Simplified case detection based on edges and corners
        if edges_oriented:
            if corners_oriented == 4:  # All oriented
                return None  # OLL already solved
            elif corners_oriented == 0:  # No corners oriented
                return 'OLL 21'  # H shape
            elif corners_oriented == 1:  # One corner oriented
                return 'OLL 22'  # Pi shape
            elif corners_oriented == 2:  # Two corners oriented
                if self.cube.state[0, 0, 0] == self.cube.state[0, 1, 1] and self.cube.state[0, 0, 2] == self.cube.state[0, 1, 1]:
                    return 'OLL 23'  # L shape
                else:
                    return 'OLL 24'  # T shape
        else:
            # Just a few common cases for demonstration
            if corners_oriented == 0:
                return 'OLL 1'  # Dot
            elif corners_oriented == 1:
                return 'OLL 2'  # Awkward shape
            elif corners_oriented == 2:
                return 'OLL 3'  # Awkward shape
            elif corners_oriented == 4:
                return 'OLL 45'  # Cross
        
        # Default case if nothing matches
        return 'OLL 7'  # Sune (common case)

    def solve_oll(self):
        """Solve the Orientation of Last Layer"""
        solution_steps = []
        
        # Detect the OLL case
        oll_case = self._get_oll_case()
        
        # If OLL is already solved, return empty solution
        if oll_case is None:
            return ""
        
        # Apply the algorithm for the detected case
        algorithm = self.oll_algorithms.get(oll_case)
        if algorithm:
            solution_steps.append(algorithm)
            self.cube.apply_moves(algorithm)
        
        return " ".join(solution_steps)

    def _get_pll_case(self):
        """Identify the PLL case based on the permutation of last layer pieces"""
        # Simplified implementation - this would typically analyze the pattern
        # of colors on the top layer to determine which PLL case we have
        
        # For this implementation, we'll use a simple approach
        # Check if corners are permuted correctly
        corners_permuted = True
        # Sample corner check (not comprehensive)
        if (self.cube.state[2, 0, 0] != self.cube.state[2, 0, 2] or
            self.cube.state[3, 0, 0] != self.cube.state[3, 0, 2] or
            self.cube.state[4, 0, 0] != self.cube.state[4, 0, 2] or
            self.cube.state[5, 0, 0] != self.cube.state[5, 0, 2]):
            corners_permuted = False
        
        # Check if edges are permuted correctly
        edges_permuted = True
        # Sample edge check (not comprehensive)
        if (self.cube.state[2, 0, 1] != self.cube.state[2, 1, 1] or
            self.cube.state[3, 0, 1] != self.cube.state[3, 1, 1] or
            self.cube.state[4, 0, 1] != self.cube.state[4, 1, 1] or
            self.cube.state[5, 0, 1] != self.cube.state[5, 1, 1]):
            edges_permuted = False
        
        # Simplified case detection
        if corners_permuted and edges_permuted:
            return None  # PLL already solved
        elif corners_permuted and not edges_permuted:
            # Edge cycles - U perms, H perm, Z perm
            return 'Ua'  # U-perm a (common case)
        elif not corners_permuted and edges_permuted:
            # Corner cycles - A perms, E perm
            return 'Aa'  # A-perm a (common case)
        else:
            # Both corners and edges need permutation
            # G perms, F perm, etc.
            return 'T'  # T-perm (common case)

    def solve_pll(self):
        """Solve the Permutation of Last Layer"""
        solution_steps = []
        
        # Detect the PLL case
        pll_case = self._get_pll_case()
        
        # If PLL is already solved, return empty solution
        if pll_case is None:
            return ""
        
        # Try different cube rotations (AUF - Adjust U Face) to find the correct case
        for _ in range(4):
            pll_case = self._get_pll_case()
            if pll_case is None:
                break
                
            # Apply the algorithm for the detected case
            algorithm = self.pll_algorithms.get(pll_case)
            if algorithm:
                solution_steps.append(algorithm)
                self.cube.apply_moves(algorithm)
                
                # Check if PLL is now solved
                pll_case = self._get_pll_case()
                if pll_case is None:
                    break
            
            # Rotate U and try again if not solved
            solution_steps.append("U")
            self.cube.U()
        
        # Final AUF to align the top layer
        # Check which U face rotation aligns with centers
        for i in range(4):
            if (self.cube.state[2, 0, 1] == self.cube.state[2, 1, 1] and
                self.cube.state[3, 0, 1] == self.cube.state[3, 1, 1] and
                self.cube.state[4, 0, 1] == self.cube.state[4, 1, 1] and
                self.cube.state[5, 0, 1] == self.cube.state[5, 1, 1]):
                break
            
            solution_steps.append("U")
            self.cube.U()
        
        return " ".join(solution_steps)
    
if __name__ == "__main__":
    cube_data = {
        'top': [['B', 'Y', 'Y'],
                ['B', 'W', 'B'],
                ['B', 'W', 'R']],

        'front': [['Y', 'R', 'G'],
                  ['R', 'G', 'W'],
                  ['W', 'G', 'G']],

        'right': [['Y', 'Y', 'G'],
                  ['B', 'R', 'R'],
                  ['W', 'W', 'W']],

        'left': [['R', 'R', 'R'],
                 ['G', 'O', 'G'],
                 ['O', 'O', 'B']],

        'bottom': [['O', 'Y', 'R'],
                   ['W', 'Y', 'G'],
                   ['Y', 'B', 'O']],

        'back': [['O', 'O', 'W'],
                 ['Y', 'B', 'O'],
                 ['G', 'O', 'B']]
    }

    # Convert and create cube
    converted_state = RubiksCube.convert_cube_data(cube_data)
    cube = RubiksCube(state=converted_state)

    # Print to verify
    cube.print_cube()
    solver = CFOPSolver(cube)
    solution = solver.solve_cross()
    cube.print_cube()
