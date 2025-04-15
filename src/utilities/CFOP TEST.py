from random import randint
from tkinter import *





class CubeSolver:
    def __init__(self, cube_data):
        self.cube = self.make_cube(cube_data)
        self.moves_list = []
        self.last_scramble = []
        self.f2l_list = []
        self.step_moves_list = [0, 0, 0, 0]
        self.solution_length = 0


    # creates a 3d list representing a solved cube
    def make_cube(self, cube_data):
        self.step_moves_list = [0, 0, 0, 0]
        self.f2l_list = []
        self.moves_list = []
        return [[[cell.upper() for cell in row] for row in cube_data['top']],  # Up/white

                [[cell.upper() for cell in row] for row in cube_data['front']],  # front/green

                [[cell.upper() for cell in row] for row in cube_data['right']],  # right/red

                [[cell.upper() for cell in row] for row in cube_data['left']],  # left/orange

                [[cell.upper() for cell in row] for row in cube_data['bottom']],  # down/yellow

                [[cell.upper() for cell in row] for row in cube_data['back']]]  # back/blue





    # prints a string representation of the cube to the interpreter
    def print_cube(self):
        print('\t\t' + str(self.cube[5][0]) + '\n\t\t' + str(self.cube[5][1]) + '\n\t\t' + str(self.cube[5][2]))
        print(str(self.cube[3][0]) + ' ' + str(self.cube[0][0]) + ' ' + str(self.cube[2][0]))
        print(str(self.cube[3][1]) + ' ' + str(self.cube[0][1]) + ' ' + str(self.cube[2][1]))
        print(str(self.cube[3][2]) + ' ' + str(self.cube[0][2]) + ' ' + str(self.cube[2][2]))
        print('\t\t' + str(self.cube[1][0]) + '\n\t\t' + str(self.cube[1][1]) + '\n\t\t' + str(self.cube[1][2]))
        print('\t\t' + str(self.cube[4][0]) + '\n\t\t' + str(self.cube[4][1]) + '\n\t\t' + str(self.cube[4][2]))


    # simplifies the list of moves and returns a string representation of the moves
    def get_moves(self):
        self.simplify_moves()
        s = ""
        for i in self.moves_list:
            s += str(i) + " "
        s = str.replace(s, "i", "'")[:-1]
        return s



    # helper function: returns True if all elements in a set are equal
    def all_same(items):
        return all(x == items[0] for x in items)


    # Transforms a given move into the corresponding move after a Y-rotation
    def yTransform(self, move):
        if move[0] in ["U", "D"]:
            return move
        if move[0] == "F":
            return "R" + move[1:]
        if move[0] == "R":
            return "B" + move[1:]
        if move[0] == "B":
            return "L" + move[1:]
        if move[0] == "L":
            return "F" + move[1:]
        raise Exception("Invalid move to yTransform: " + move)


    # removes redundancies
    def simplify_moves(self):
        new_list = []
        for move in self.moves_list:
            if new_list and move[0] == new_list[-1][0]:
                if len(move) == 1:  # e.g., R
                    if len(new_list[-1]) == 1:  # e.g., R + R = R2
                        new_list[-1] = move[0] + "2"
                    elif new_list[-1][1] == "2":  # e.g., R2 + R = R'
                        new_list[-1] = move[0] + "i"
                    else:  # e.g., R' + R = (cancel out)
                        new_list.pop()
                elif move[1] == "i":  # e.g., R' + R' = R2
                    if len(new_list[-1]) == 1:
                        new_list[-1] = move[0] + "2"
                    elif new_list[-1][1] == "2":  # e.g., R2 + R' = R
                        new_list[-1] = move[0]
                    else:  # e.g., R' + R' = (cancel out)
                        new_list.pop()
                elif move[1] == "2":  # e.g., R2 + R2 = (cancel out)
                    if len(new_list[-1]) == 1:
                        new_list[-1] = move[0] + "i"
                    elif new_list[-1][1] == "i":
                        new_list[-1] = move[0]
                    else:
                        new_list.pop()
            else:
                new_list.append(move)
        self.moves_list = new_list


    # sets up the cube to perform a move by rotating that face to the top
    def setup(self, face):
        face = str.lower(face)
        if face == "f":
            self.move("X")
        elif face == "r":
            self.move("Zi")
        elif face == "l":
            self.move("Z")
        elif face == "d":
            self.move("X2")
        elif face == "b":
            self.move("Xi")
        else:
            raise Exception("Invalid setup; face: " + face)


    # performs the inverse of setup to restore the cube's previous orientation
    def undo(self, face):
        face = str.lower(face)
        if face == "f":
            self.move("Xi")
        elif face == "r":
            self.move("Z")
        elif face == "l":
            self.move("Zi")
        elif face == "d":
            self.move("X2")
        elif face == "b":
            self.move("X")
        else:
            raise Exception("Invalid undo; face: " + face)


    # Tokenizes a string of moves
    def m(self, s):
        s = str.replace(s, "'", "i")
        k = s.split(' ')
        self.solution_length += len(k)
        for word in k:
            self.moves_list.append(word)
            self.move(word)


    # performs a move by setting up, performing U moves, and undoing the setup
    def move(self, mv):
        mv = str.lower(mv)
        if mv == "u":
            self.U()
        elif mv == "u2":
            self.move("U");
            self.move("U");
        elif mv == "ui":
            self.move("U");
            self.move("U");
            self.move("U");
        elif mv == "f":
            self.setup("F");
            self.U();
            self.undo("F");
        elif mv == "f2":
            self.move("F");
            self.move("F");
        elif mv == "fi":
            self.move("F");
            self.move("F");
            self.move("F");
        elif mv == "r":
            self.setup("R");
            self.U();
            self.undo("R");
        elif mv == "r2":
            self.move("R");
            self.move("R");
        elif mv == "ri":
            self.move("R");
            self.move("R");
            self.move("R");
        elif mv == "l":
            self.setup("L");
            self.U();
            self.undo("L");
        elif mv == "l2":
            self.move("L");
            self.move("L");
        elif mv == "li":
            self.move("L");
            self.move("L");
            self.move("L");
        elif mv == "b":
            self.setup("B");
            self.U();
            self.undo("B");
        elif mv == "b2":
            self.move("B");
            self.move("B");
        elif mv == "bi":
            self.move("B");
            self.move("B");
            self.move("B");
        elif mv == "d":
            self.setup("D");
            self.U();
            self.undo("D");
        elif mv == "d2":
            self.move("D");
            self.move("D");
        elif mv == "di":
            self.move("D");
            self.move("D");
            self.move("D");
        elif mv == "x":
            self.rotate("X")
        elif mv == "x2":
            self.move("X");
            self.move("X");
        elif mv == "xi":
            self.move("X");
            self.move("X");
            self.move("X");
        elif mv == "y":
            self.rotate("Y")
        elif mv == "y2":
            self.move("Y");
            self.move("Y");
        elif mv == "yi":
            self.move("Y");
            self.move("Y");
            self.move("Y");
        elif mv == "z":
            self.rotate("Z")
        elif mv == "z2":
            self.move("Z");
            self.move("Z");
        elif mv == "zi":
            self.move("Z");
            self.move("Z");
            self.move("Z");
        elif mv == "uw":
            self.move("D");
            self.move("Y");
        elif mv == "uw2":
            self.move("UW");
            self.move("UW");
        elif mv == "uwi":
            self.move("UW");
            self.move("UW");
            self.move("UW");
        elif mv == "m":
            self.move("Li");
            self.move("R");
            self.move("Xi");
        elif mv == "mi":
            self.move("M");
            self.move("M");
            self.move("M");
        elif mv == "m2":
            self.move("M");
            self.move("M");
        elif mv == "rw":
            self.move("L");
            self.move("X");
        elif mv == "rwi":
            self.move("RW");
            self.move("RW");
            self.move("RW");
        elif mv == "rw2":
            self.move("RW");
            self.move("RW");
        elif mv == "fw":
            self.move("Bi");
            self.move("Z");
        elif mv == "fwi":
            self.move("FW");
            self.move("FW");
            self.move("FW");
        elif mv == "fw2":
            self.move("FW");
            self.move("FW");
        elif mv == "lw":
            self.move("R");
            self.move("Xi");
        elif mv == "lwi":
            self.move("LW");
            self.move("LW");
            self.move("LW");
        elif mv == "lw2":
            self.move("LW");
            self.move("LW");
        elif mv == "bw":
            self.move("F");
            self.move("Zi");
        elif mv == "bwi":
            self.move("BW");
            self.move("BW");
            self.move("BW");
        elif mv == "bw2":
            self.move("BW");
            self.move("BW");
        elif mv == "dw":
            self.move("U");
            self.move("Yi");
        elif mv == "dwi":
            self.move("DW");
            self.move("DW");
            self.move("DW");
        elif mv == "dw2":
            self.move("DW");
            self.move("DW");
        else:
            raise Exception("Invalid Move: " + str(mv))


    # rotates the entire cube along a particular axis
    def rotate(self, axis):
        axis = str.lower(axis)
        if axis == 'x':  # R
            temp = self.cube[0]
            self.cube[0] = self.cube[1]
            self.cube[1] = self.cube[4]
            self.cube[4] = self.cube[5]
            self.cube[5] = temp
            self.rotate_face_counterclockwise("L")
            self.rotate_face_clockwise("R")
        elif axis == 'y':  # U
            temp = self.cube[1]
            self.cube[1] = self.cube[2]
            self.cube[2] = self.cube[5]
            self.cube[5] = self.cube[3]
            self.cube[3] = temp
            # after swaps,
            self.rotate_face_clockwise("L")
            self.rotate_face_clockwise("F")
            self.rotate_face_clockwise("R")
            self.rotate_face_clockwise("B")
            self.rotate_face_clockwise("U")
            self.rotate_face_counterclockwise("D")
        elif axis == 'z':  # F
            temp = self.cube[0]
            self.cube[0] = self.cube[3]
            self.cube[3] = self.cube[4]
            self.cube[4] = self.cube[2]
            self.cube[2] = temp
            self.rotate_face_clockwise("L");
            self.rotate_face_clockwise("L");
            self.rotate_face_clockwise("D");
            self.rotate_face_clockwise("D");
            self.rotate_face_clockwise("F")
            self.rotate_face_counterclockwise("B")
        else:
            raise Exception("Invalid rotation: " + axis)


    # performs a U move
    def U(self):
        # rotate U face
        temp = self.cube[0][0][0]
        self.cube[0][0][0] = self.cube[0][2][0]
        self.cube[0][2][0] = self.cube[0][2][2]
        self.cube[0][2][2] = self.cube[0][0][2]
        self.cube[0][0][2] = temp
        temp = self.cube[0][0][1]
        self.cube[0][0][1] = self.cube[0][1][0]
        self.cube[0][1][0] = self.cube[0][2][1]
        self.cube[0][2][1] = self.cube[0][1][2]
        self.cube[0][1][2] = temp

        # rotate others
        temp = self.cube[5][2][0]
        self.cube[5][2][0] = self.cube[3][2][2]
        self.cube[3][2][2] = self.cube[1][0][2]
        self.cube[1][0][2] = self.cube[2][0][0]
        self.cube[2][0][0] = temp
        temp = self.cube[5][2][1]
        self.cube[5][2][1] = self.cube[3][1][2]
        self.cube[3][1][2] = self.cube[1][0][1]
        self.cube[1][0][1] = self.cube[2][1][0]
        self.cube[2][1][0] = temp
        temp = self.cube[5][2][2]
        self.cube[5][2][2] = self.cube[3][0][2]
        self.cube[3][0][2] = self.cube[1][0][0]
        self.cube[1][0][0] = self.cube[2][2][0]
        self.cube[2][2][0] = temp


    # Rotates a particular face counter-clockwise
    def rotate_face_counterclockwise(self,face):
        self.rotate_face_clockwise(face)
        self.rotate_face_clockwise(face)
        self.rotate_face_clockwise(face)


    # Rotates a particular face clockwise
    def rotate_face_clockwise(self, face):
        f_id = -1
        face = str.lower(face)
        if face == "u":
            f_id = 0
        elif face == "f":
            f_id = 1
        elif face == "r":
            f_id = 2
        elif face == "l":
            f_id = 3
        elif face == "d":
            f_id = 4
        elif face == "b":
            f_id = 5
        else:
            raise Exception("Invalid face: " + face)
        temp = self.cube[f_id][0][0]
        self.cube[f_id][0][0] = self.cube[f_id][2][0]
        self.cube[f_id][2][0] = self.cube[f_id][2][2]
        self.cube[f_id][2][2] = self.cube[f_id][0][2]
        self.cube[f_id][0][2] = temp
        temp = self.cube[f_id][0][1]
        self.cube[f_id][0][1] = self.cube[f_id][1][0]
        self.cube[f_id][1][0] = self.cube[f_id][2][1]
        self.cube[f_id][2][1] = self.cube[f_id][1][2]
        self.cube[f_id][1][2] = temp


    # Solves the top cross as part of the OLL step
    def topCross(self):
        # if all the edges are all equal to eachother (all being white)
        if self.cube[0][0][1] == self.cube[0][1][0] == self.cube[0][1][2] == self.cube[0][2][1]:
            # print("Cross already done, step skipped")
            return
        # If this is true, we have our cross and we can go onto the next step
        else:
            while self.cube[0][0][1] != "W" or self.cube[0][1][0] != "W" or self.cube[0][1][2] != "W" or self.cube[0][2][1] != "W":
                if self.cube[0][1][0] == self.cube[0][1][2]:
                    # if we have a horizontal line Just do alg
                    self.m("F R U Ri Ui Fi")
                    break  # breaking w/o having to recheck while conditions again, this will give us a cross
                elif self.cube[0][0][1] == self.cube[0][2][1]:
                    # if we have a vertical line, do a U then alg
                    self.m("U F R U Ri Ui Fi")
                    break
                elif self.cube[0][0][1] != "W" and self.cube[0][1][0] != "W" and self.cube[0][1][2] != "W" and self.cube[0][2][1] != "W":
                    # This would mean we have a dot case, so perform
                    self.m("F U R Ui Ri Fi U F R U Ri Ui Fi")
                    break
                elif self.cube[0][1][2] == self.cube[0][2][1] or self.cube[0][0][1] == self.cube[0][1][0]:
                    # If we have an L case in the top left or the bottom right, will give us a line
                    self.m("F R U Ri Ui Fi")
                else:
                    # This is we dont have a line, dot, cross, or L in top left or bottom right
                    self.m("U")


    # returns True if the top is solved
    def isTopSolved(self):
        # determines if the top of the cube is solved.
        if self.cube[0][0][0] == self.cube[0][0][1] == self.cube[0][0][2] == self.cube[0][1][0] == self.cube[0][1][1] == self.cube[0][1][2] == self.cube[0][2][0] == self.cube[0][2][1] == \
                self.cube[0][2][2]:
            return True
        else:
            return False


    # puts a single edge piece in the proper location for the cross
    # Assumes the cross is formed on the bottom and is the yellow face
    # Checks all edges in front/up face, then back-right/left if needed
    def putCrossEdge(self):
        for i in range(3):
            if i == 1:
                self.m("Ri U R F2")  # bring out back-right edge
            elif i == 2:
                self.m("L Ui Li F2")  # bring out back-left edge
            for j in range(4):
                for k in range(4):
                    if "Y" in [self.cube[4][0][1], self.cube[1][2][1]]:
                        return
                    self.m("F")
                self.m("U")


    def cross(self):
        print("Starting cross solve...")
        bottom_center = self.cube[4][1][1]
        face_centers = [self.cube[1][1][1], self.cube[2][1][1], self.cube[5][1][1], self.cube[3][1][1]]
        # Map: F, R, B, L
        max_cycles = 30
        cycles = 0
        while cycles < max_cycles:
            cycles += 1
            solved = 0
            d_edges = [self.cube[4][0][1], self.cube[4][1][2], self.cube[4][2][1], self.cube[4][1][0]]
            side_edges = [self.cube[1][2][1], self.cube[2][2][1], self.cube[5][2][1], self.cube[3][2][1]]
            print(f"Cycle {cycles}: cross edge states:")
            for i in range(4):
                print(f"  Face {i}: D edge={d_edges[i]}, Side edge={side_edges[i]}, Face center={face_centers[i]}, D center={bottom_center}")
                if d_edges[i] == bottom_center and side_edges[i] == face_centers[i]:
                    solved += 1
            if solved == 4:
                print("Cross solved successfully!")
                return True
            # For each cross edge (F, R, B, L)
            for i in range(4):
                # Rotate so this face is in front
                for _ in range(i):
                    self.m("Y")
                # 1. If the cross edge is in D layer but not solved, extract it to U
                if self.cube[4][0][1] == bottom_center and self.cube[1][2][1] != self.cube[1][1][1]:
                    self.m("F U R Ui")
                # 2. If the cross edge is in the middle layer, bring it to U
                elif self.cube[1][1][2] == bottom_center:
                    self.m("R U Ri")
                elif self.cube[1][1][0] == bottom_center:
                    self.m("Li Ui L")
                # 3. If the cross edge is in U layer, align and insert
                for _ in range(4):
                    if self.cube[0][2][1] == bottom_center:
                        # Align with center
                        while self.cube[1][1][1] != self.cube[1][0][1]:
                            self.m("U")
                        self.m("F2")
                        break
                    self.m("U")
                # Rotate back to original orientation
                for _ in range((4 - i) % 4):
                    self.m("Y")
            # End of cycle
        print("Cross solving timed out!")
        return False


    def _handle_wrong_edges(self, bottom_center):
        """Extract any edges that are in wrong positions"""
        for _ in range(4):
            if (self.cube[4][0][1] == bottom_center and 
                self.cube[1][2][1] != self.cube[1][1][1]):
                if self._find_edge_in_u_layer(bottom_center):
                    self._insert_edge_from_u()
                else:
                    self.m("F2")
            self.m("Y")

    def _is_current_edge_solved(self, bottom_center):
        """Check if current front cross edge is solved"""
        return (self.cube[4][0][1] == bottom_center and 
                self.cube[1][2][1] == self.cube[1][1][1])

    def _find_edge_in_u_layer(self, bottom_center):
        """Find a matching edge in U layer"""
        for _ in range(4):
            if (self.cube[0][2][1] == bottom_center or 
                self.cube[1][0][1] == bottom_center):
                return True
            self.m("U")
        return False

    def _insert_edge_from_u(self):
        """Insert edge from U layer with optimal moves"""
        bottom_center = self.cube[4][1][1]
        front_center = self.cube[1][1][1]
        
        if self.cube[0][2][1] == bottom_center:
            if self.cube[1][0][1] == front_center:
                self.m("F2")  # Direct insert
            else:
                self.m("U R F R'")  # Insert with setup
            return True
        elif self.cube[1][0][1] == bottom_center:
            if self.cube[0][2][1] == front_center:
                self.m("F R' F2")  # Insert with setup
            else:
                self.m("F2")  # Direct insert
            return True
        return False

    def _find_edge_in_middle(self):
        """Find a matching edge in middle layer"""
        bottom_center = self.cube[4][1][1]
        return (self.cube[1][1][2] == bottom_center or 
                self.cube[1][1][0] == bottom_center)

    def _insert_edge_from_middle(self):
        """Insert edge from middle layer with optimal moves"""
        bottom_center = self.cube[4][1][1]
        if self.cube[1][1][2] == bottom_center:
            self.m("R F R'")
            return True
        elif self.cube[1][1][0] == bottom_center:
            self.m("L' F' L")
            return True
        return False


    def _extract_wrong_bottom_edges(self, bottom_center):
        """Extract edges in bottom layer that are in wrong positions"""
        for _ in range(4):
            if (self.cube[4][0][1] == bottom_center and 
                self.cube[1][2][1] != self.cube[1][1][1]):
                self.m("F2")
            self.m("Y")

    def _is_cross_edge_solved(self):
        """Check if current cross edge position is solved"""
        bottom_center = self.cube[4][1][1]
        front_center = self.cube[1][1][1]
        return (self.cube[4][0][1] == bottom_center and 
                self.cube[1][2][1] == front_center)

    def _is_matching_edge_in_u(self, bottom_center):
        """Check if there's a matching edge in U layer"""
        return (self.cube[0][2][1] == bottom_center or 
                self.cube[1][0][1] == bottom_center)

    def _insert_edge_from_u(self):
        """Insert edge from U layer"""
        bottom_center = self.cube[4][1][1]
        front_center = self.cube[1][1][1]
        
        if self.cube[0][2][1] == bottom_center:
            if self.cube[1][0][1] == front_center:
                self.m("F2")
            else:
                self.m("U R F R'")
            return True
        elif self.cube[1][0][1] == bottom_center:
            if self.cube[0][2][1] == front_center:
                self.m("F R' F2")
            else:
                self.m("F2")
            return True
        return False

    def _is_edge_in_middle(self):
        """Check if matching edge is in middle layer"""
        bottom_center = self.cube[4][1][1]
        return (self.cube[1][1][2] == bottom_center or 
                self.cube[1][1][0] == bottom_center)

    def _insert_edge_from_middle(self):
        """Insert edge from middle layer"""
        bottom_center = self.cube[4][1][1]
        
        if self.cube[1][1][2] == bottom_center:
            self.m("R F R'")
            return True
        elif self.cube[1][1][0] == bottom_center:
            self.m("L' F' L")
            return True
        return False


    def _check_edge_in_u_layer(self, bottom_center):
        """Check if there's a matching edge in U layer"""
        for _ in range(4):
            if (self.cube[0][2][1] == bottom_center or 
                self.cube[1][0][1] == bottom_center):
                return True
            self.m("U")
        return False

    def _insert_edge_from_u(self, bottom_center):
        """Insert a matching edge from U layer"""
        front_center = self.cube[1][1][1]
        
        # Find optimal insertion point
        for _ in range(4):
            if self.cube[0][2][1] == bottom_center:
                if self.cube[1][0][1] == front_center:
                    self.m("F2")
                    return True
                else:
                    self.m("U R F R'")
                    return True
            elif self.cube[1][0][1] == bottom_center:
                if self.cube[0][2][1] == front_center:
                    self.m("F R' F2")
                    return True
                else:
                    self.m("F2")
                    return True
            self.m("U")
        return False

    def _solve_matching_edge(self, bottom_center, front_center):
        """Find and solve a matching cross edge"""
        # Check U layer first (most efficient)
        if self._insert_edge_from_u(bottom_center):
            return True
            
        # Check middle layer
        if self.cube[1][1][2] == bottom_center:
            self.m("R F R'")
            return True
        elif self.cube[1][1][0] == bottom_center:
            self.m("L' F' L")
            return True
            
        return False

    def _extract_wrong_edges(self):
        """Get edges out of incorrect positions in bottom layer"""
        # corner orientations if in U layer, first letter means the direction that the color is facing
        fCorU = self.cube[1][0][2] == dmid and self.cube[0][2][2] == fmid and self.cube[2][2][0] == rmid
        rCorU = self.cube[2][2][0] == dmid and self.cube[1][0][2] == fmid and self.cube[0][2][2] == rmid
        uCorU = self.cube[0][2][2] == dmid and self.cube[2][2][0] == fmid and self.cube[1][0][2] == rmid
        # Corner orientations for correct location in D layer
        fCorD = self.cube[1][2][2] == dmid and self.cube[2][2][2] == fmid and self.cube[4][0][2] == rmid
        rCorD = self.cube[2][2][2] == dmid and self.cube[4][0][2] == fmid and self.cube[1][2][2] == rmid
        dCorD = self.cube[4][0][2] == dmid and self.cube[1][2][2] == fmid and self.cube[2][2][2] == rmid  # This is solved spot
        # edge orientations on U layer, normal or flipped version based on F face
        norEdgeFU = self.cube[1][0][1] == fmid and self.cube[0][2][1] == rmid
        norEdgeLU = self.cube[3][1][2] == fmid and self.cube[0][1][0] == rmid
        norEdgeBU = self.cube[5][2][1] == fmid and self.cube[0][0][1] == rmid
        norEdgeRU = self.cube[2][1][0] == fmid and self.cube[0][1][2] == rmid
        norEdgeAny = norEdgeFU or norEdgeLU or norEdgeBU or norEdgeRU
        flipEdgeFU = self.cube[0][2][1] == fmid and self.cube[1][0][1] == rmid
        flipEdgeLU = self.cube[0][1][0] == fmid and self.cube[3][1][2] == rmid
        flipEdgeBU = self.cube[0][0][1] == fmid and self.cube[5][2][1] == rmid
        flipEdgeRU = self.cube[0][1][2] == fmid and self.cube[2][1][0] == rmid
        flipEdgeAny = flipEdgeFU or flipEdgeLU or flipEdgeBU or flipEdgeRU
        # edge orientations for normal or flipped insertion into slot
        norEdgeInsert = self.cube[1][1][2] == fmid and self.cube[2][2][1] == rmid  # This is solved spot
        flipEdgeInsert = self.cube[2][2][1] == fmid and self.cube[1][1][2] == rmid
        # these are for if the back right or front left slots are open or not
        backRight = self.cube[4][2][2] == dmid and self.cube[5][1][2] == self.cube[5][0][2] == self.cube[5][1][1] and self.cube[2][0][1] == self.cube[2][0][2] == rmid
        frontLeft = self.cube[4][0][0] == dmid and self.cube[1][1][0] == self.cube[1][2][0] == fmid and self.cube[3][2][0] == self.cube[3][2][1] == self.cube[3][1][1]

        if dCorD and norEdgeInsert:
            return
        # Easy Cases
        elif fCorU and flipEdgeRU:  # Case 1
            self.m("U R Ui Ri")
        elif rCorU and norEdgeFU:  # Case 2
            self.m("F Ri Fi R")
        elif fCorU and norEdgeLU:  # Case 3
            self.m("Fi Ui F")
        elif rCorU and flipEdgeBU:  # Case 4
            self.m("R U Ri")
        # Reposition Edge
        elif fCorU and flipEdgeBU:  # Case 5
            self.m("F2 Li Ui L U F2")
        elif rCorU and norEdgeLU:  # Case 6
            self.m("R2 B U Bi Ui R2")
        elif fCorU and flipEdgeLU:  # Case 7
            self.m("Ui R U2 Ri U2 R Ui Ri")
        elif rCorU and norEdgeBU:  # Case 8
            self.m("U Fi U2 F Ui F Ri Fi R")
        # Reposition edge and Corner Flip
        elif fCorU and norEdgeBU:  # Case 9
            self.m("Ui R Ui Ri U Fi Ui F")
        elif rCorU and flipEdgeLU:  # Case 10
            if not backRight:
                self.m("Ri U R2 U Ri")
            else:
                self.m("Ui R U Ri U R U Ri")
        elif fCorU and norEdgeRU:  # Case 11
            self.m("Ui R U2 Ri U Fi Ui F")
        elif rCorU and flipEdgeFU:  # Case 12
            if not backRight:
                self.m("Ri U2 R2 U Ri")
            else:
                self.m("Ri U2 R2 U R2 U R")
        elif fCorU and norEdgeFU:  # Case 13
            if not backRight:
                self.m("Ri U R Fi Ui F")
            else:
                self.m("U Fi U F Ui Fi Ui F")
        elif rCorU and flipEdgeRU:  # Case 14
            self.m("Ui R Ui Ri U R U Ri")
        # Split Pair by Going Over
        elif fCorU and flipEdgeFU:  # Case 15
            if not backRight:
                self.m("Ui Ri U R Ui R U Ri")
            elif not frontLeft:
                self.m("U R Ui Ri D R Ui Ri Di")
            else:
                self.m("U Ri F R Fi U R U Ri")
        elif rCorU and norEdgeRU:  # Case 16
            self.m("R Ui Ri U2 Fi Ui F")
        elif uCorU and flipEdgeRU:  # Case 17
            self.m("R U2 Ri Ui R U Ri")
        elif uCorU and norEdgeFU:  # Case 18
            self.m("Fi U2 F U Fi Ui F")
        # Pair made on side
        elif uCorU and flipEdgeBU:  # Case 19
            self.m("U R U2 R2 F R Fi")
        elif uCorU and norEdgeLU:  # Case 20
            self.m("Ui Fi U2 F2 Ri Fi R")
        elif uCorU and flipEdgeLU:  # Case 21
            self.m("R B U2 Bi Ri")
        elif uCorU and norEdgeBU:  # Case 22
            self.m("Fi Li U2 L F")
        # Weird Cases
        elif uCorU and flipEdgeFU:  # Case 23
            self.m("U2 R2 U2 Ri Ui R Ui R2")
        elif uCorU and norEdgeRU:  # Case 24
            self.m("U Fi Li U L F R U Ri")
        # Corner in Place, edge in the U face (All these cases also have set-up moves in case the edge is in the wrong orientation
        elif dCorD and flipEdgeAny:  # Case 25
            if flipEdgeBU:
                self.m("U")  # set-up move
            elif flipEdgeLU:
                self.m("U2")  # set-up move
            elif flipEdgeFU:
                self.m("Ui")  # set-up move
            if not backRight:
                self.m("R2 Ui Ri U R2")
            else:
                self.m("Ri Fi R U R Ui Ri F")
        elif dCorD and norEdgeAny:  # Case 26
            if norEdgeRU:
                self.m("U")  # set-up move
            elif norEdgeBU:
                self.m("U2")  # set-up move
            elif norEdgeLU:
                self.m("Ui")  # set-up move
            self.m("U R Ui Ri F Ri Fi R")
        elif fCorD and flipEdgeAny:  # Case 27
            if flipEdgeBU:
                self.m("U")  # set-up move
            elif flipEdgeLU:
                self.m("U2")  # set-up move
            elif flipEdgeFU:
                self.m("Ui")  # set-up move
            self.m("R Ui Ri U R Ui Ri")
        elif rCorD and norEdgeAny:  # Case 28
            if norEdgeRU:
                self.m("U")  # set-up move
            elif norEdgeBU:
                self.m("U2")  # set-up move
            elif norEdgeLU:
                self.m("Ui")  # set-up move
            self.m("R U Ri Ui F Ri Fi R")
        elif fCorD and norEdgeAny:  # Case 29
            if norEdgeRU:
                self.m("U")  # set-up move
            elif norEdgeBU:
                self.m("U2")  # set-up move
            elif norEdgeLU:
                self.m("Ui")  # set-up move
            self.m("U2 R Ui Ri Fi Ui F")
        elif rCorD and flipEdgeAny:  # Case 30
            if flipEdgeBU:
                self.m("U")  # set-up move
            elif flipEdgeLU:
                self.m("U2")  # set-up move
            elif flipEdgeFU:
                self.m("Ui")  # set-up move
            self.m("R U Ri Ui R U Ri")
        # Edge in place, corner in U Face
        elif uCorU and flipEdgeInsert:  # Case 31
            self.m("R U2 Ri Ui F Ri Fi R")
        elif uCorU and norEdgeInsert:  # Case 32
            self.m("R2 U R2 U R2 U2 R2")
        elif fCorU and norEdgeInsert:  # Case 33
            self.m("Ui R Ui Ri U2 R Ui Ri")
        elif rCorU and norEdgeInsert:  # Case 34
            self.m("Ui R U2 Ri U R U Ri")
        elif fCorU and flipEdgeInsert:  # Case 35
            self.m("U2 R Ui Ri Ui Fi Ui F")
        elif rCorU and flipEdgeInsert:  # Case 36
            self.m("U Fi Ui F Ui R U Ri")
        # Edge and Corner in place
        # Case 37 is Lol case, already completed
        elif dCorD and flipEdgeInsert:  # Case 38 (Typical flipped f2l pair case
            self.m("R2 U2 F R2 Fi U2 Ri U Ri")
        elif fCorD and norEdgeInsert:  # Case 39
            self.m("R2 U2 Ri Ui R Ui Ri U2 Ri")
        elif rCorD and norEdgeInsert:  # Case 40
            self.m("R U2 R U Ri U R U2 R2")
        elif fCorD and flipEdgeInsert:  # Case 41
            self.m("F2 Li Ui L U F Ui F")
        elif rCorD and flipEdgeInsert:  # Case 42
            self.m("R Ui Ri Fi Li U2 L F")


    # Returns true if the f2l Corner in FR spot is inserted and oriented correctly
    def f2lCorner(self):
        return self.cube[4][0][2] == self.cube[4][1][1] and self.cube[1][2][2] == self.cube[1][1][1] and self.cube[2][2][2] == self.cube[2][1][1]  # This is solved spot


    # Returns true if the f2l edge in FR spot is inserted and oriented correctly
    def f2lEdge(self):
        return self.cube[1][1][2] == self.cube[1][1][1] and self.cube[2][2][1] == self.cube[2][1][1]  # This is solved spot


    # Returns true if the f2l edge and corner are properly inserted and orientated in the FR position
    def f2lCorrect(self):
        return self.f2lCorner() and self.f2lEdge()


    # returns if the f2l edge is on the top layer at all
    def f2lEdgeOnTop(self):
        rmid = self.cube[2][1][1]
        fmid = self.cube[1][1][1]
        dmid = self.cube[4][1][1]
        # edge orientations on U layer, normal or flipped version based on F face
        norEdgeFU = self.cube[1][0][1] == fmid and self.cube[0][2][1] == rmid
        norEdgeLU = self.cube[3][1][2] == fmid and self.cube[0][1][0] == rmid
        norEdgeBU = self.cube[5][2][1] == fmid and self.cube[0][0][1] == rmid
        norEdgeRU = self.cube[2][1][0] == fmid and self.cube[0][1][2] == rmid
        norEdgeAny = norEdgeFU or norEdgeLU or norEdgeBU or norEdgeRU
        flipEdgeFU = self.cube[0][2][1] == fmid and self.cube[1][0][1] == rmid
        flipEdgeLU = self.cube[0][1][0] == fmid and self.cube[3][1][2] == rmid
        flipEdgeBU = self.cube[0][0][1] == fmid and self.cube[5][2][1] == rmid
        flipEdgeRU = self.cube[0][1][2] == fmid and self.cube[2][1][0] == rmid
        flipEdgeAny = flipEdgeFU or flipEdgeLU or flipEdgeBU or flipEdgeRU
        return norEdgeAny or flipEdgeAny


    # returns true if the f2l edge is inserted. Can be properly orientated, or flipped.
    def f2lEdgeInserted(self):
        rmid = self.cube[2][1][1]
        fmid = self.cube[1][1][1]
        # edge orientations for normal or flipped insertion into slot
        norEdgeInsert = self.cube[1][1][2] == fmid and self.cube[2][2][1] == rmid  # This is solved spot
        flipEdgeInsert = self.cube[2][2][1] == fmid and self.cube[1][1][2] == rmid
        return norEdgeInsert or flipEdgeInsert


    # This is used to determine if the front f2l edge is inserted or not, the parameter is for the requested edge. takes BR, BL, and FL as valid
    def f2lEdgeInserted2(self, p):
        rmid = self.cube[2][1][1]
        fmid = self.cube[1][1][1]
        # edge orientations for normal or flipped insertion into slot
        norEdgeInsert = self.cube[1][1][2] == fmid and self.cube[2][2][1] == rmid  # This is solved spot
        flipEdgeInsert = self.cube[2][2][1] == fmid and self.cube[1][1][2] == rmid
        # Edge orientations in comparison to Front and Right colors
        BR = (self.cube[5][1][2] == fmid and self.cube[2][0][1] == rmid) or (self.cube[5][1][2] == rmid and self.cube[2][0][1] == fmid)
        BL = (self.cube[3][0][1] == fmid and self.cube[5][1][0] == rmid) or (self.cube[3][0][1] == rmid and self.cube[5][1][0] == fmid)
        FL = (self.cube[3][2][1] == fmid and self.cube[1][1][0] == rmid) or (self.cube[3][2][1] == rmid and self.cube[1][1][0] == fmid)

        if p == "BR":
            if BR:
                return True
            else:
                return False
        elif p == "BL":
            if BL:
                return True
            return False
        elif p == "FL":
            if FL:
                return True
            return False
        elif p == "FR":
            if norEdgeInsert or flipEdgeInsert:
                return True
        return False


    def f2lCornerInserted(self):
        rmid = self.cube[2][1][1]
        fmid = self.cube[1][1][1]
        dmid = self.cube[4][1][1]
        fCorD = self.cube[1][2][2] == dmid and self.cube[2][2][2] == fmid and self.cube[4][0][2] == rmid
        rCorD = self.cube[2][2][2] == dmid and self.cube[4][0][2] == fmid and self.cube[1][2][2] == rmid
        dCorD = self.cube[4][0][2] == dmid and self.cube[1][2][2] == fmid and self.cube[2][2][2] == rmid  # This is solved spot
        return fCorD or rCorD or dCorD


   
    def f2lFRCor(self):
        rmid = self.cube[2][1][1]
        fmid = self.cube[1][1][1]
        dmid = self.cube[4][1][1]
        fCorU = self.cube[1][0][2] == dmid and self.cube[0][2][2] == fmid and self.cube[2][2][0] == rmid
        rCorU = self.cube[2][2][0] == dmid and self.cube[1][0][2] == fmid and self.cube[0][2][2] == rmid
        uCorU = self.cube[0][2][2] == dmid and self.cube[2][2][0] == fmid and self.cube[1][0][2] == rmid
        return fCorU or rCorU or uCorU


    
    def f2lFUEdge(self):
        rmid = self.cube[2][1][1]
        fmid = self.cube[1][1][1]
        norEdgeFU = self.cube[1][0][1] == fmid and self.cube[0][2][1] == rmid
        flipEdgeFU = self.cube[0][2][1] == fmid and self.cube[1][0][1] == rmid
        return norEdgeFU or flipEdgeFU


   
    def f2lCornerOnTop(self):
        wasFound = False
        for i in range(4):  
            if self.f2lFRCor():
                wasFound = True
            self.m("U")
        return wasFound


    
    def f2lCornerCheck(self):
        r = "FR"
        count = 0
        while count < 4:
            if count == 0:
                if self.f2lCornerInserted():
                    r = "FR"
            elif count == 1:
                if self.f2lCornerInserted():
                    r = "FL"
            elif count == 2:
                if self.f2lCornerInserted():
                    r = "BL"
            elif count == 3:
                if self.f2lCornerInserted():
                    r = "BR"
            self.m("D")
            count += 1
        return r


    def f2lEdgeCheck(self):
        # Check each position for edge piece
        # Front-Right edge
        if (self.cube[1][1][2] == self.cube[1][1][1] and self.cube[2][2][1] == self.cube[2][1][1]) or \
           (self.cube[1][1][2] == self.cube[2][1][1] and self.cube[2][2][1] == self.cube[1][1][1]):
            return "FR"
        
        # Front-Left edge
        if (self.cube[1][1][0] == self.cube[1][1][1] and self.cube[3][2][1] == self.cube[3][1][1]) or \
           (self.cube[1][1][0] == self.cube[3][1][1] and self.cube[3][2][1] == self.cube[1][1][1]):
            return "FL"
        
        # Back-Left edge
        if (self.cube[5][1][0] == self.cube[5][1][1] and self.cube[3][0][1] == self.cube[3][1][1]) or \
           (self.cube[5][1][0] == self.cube[3][1][1] and self.cube[3][0][1] == self.cube[5][1][1]):
            return "BL"
        
        # Back-Right edge
        if (self.cube[5][1][2] == self.cube[5][1][1] and self.cube[2][0][1] == self.cube[2][1][1]) or \
           (self.cube[5][1][2] == self.cube[2][1][1] and self.cube[2][0][1] == self.cube[5][1][1]):
            return "BR"
            
        # Check if edge is in U layer
        fmid = self.cube[1][1][1]
        rmid = self.cube[2][1][1]
        bmid = self.cube[5][1][1]
        lmid = self.cube[3][1][1]
        
        # Front edge in U layer
        if (self.cube[1][0][1] == fmid or self.cube[0][2][1] == fmid):
            return "FR"  # Default to FR if edge is in U layer
            
        # Right edge in U layer
        if (self.cube[2][1][0] == rmid or self.cube[0][1][2] == rmid):
            return "FR"
            
        # Back edge in U layer
        if (self.cube[5][2][1] == bmid or self.cube[0][0][1] == bmid):
            return "BR"
            
        # Left edge in U layer
        if (self.cube[3][1][2] == lmid or self.cube[0][1][0] == lmid):
            return "FL"
            
        # If we reach here, try to return the position closest to where the edge piece needs to go
        edge_colors = set()
        for face in [1, 2, 3, 5]:  # Front, Right, Left, Back faces
            for i in [0, 1, 2]:
                for j in [0, 1, 2]:
                    if self.cube[face][i][j] in [fmid, rmid]:
                        edge_colors.add(self.cube[face][i][j])
        
        if fmid in edge_colors and rmid in edge_colors:
            return "FR"  # Default to FR if we find matching colors
        
        return "FR"  # Fallback to prevent exception


    
    def f2lEdgeNoCorner(self):
        topEdgeTop = self.cube[0][2][1]
        topEdgeFront = self.cube[1][0][1]
        rmid = self.cube[2][1][1]
        bmid = self.cube[5][1][1]
        lmid = self.cube[3][1][1]
        fmid = self.cube[1][1][1]
        BREdge = (topEdgeTop == rmid or topEdgeTop == bmid) and (topEdgeFront == rmid or topEdgeFront == bmid)
        BLEdge = (topEdgeTop == lmid or topEdgeTop == bmid) and (topEdgeFront == lmid or topEdgeFront == bmid)
        FLEdge = (topEdgeTop == fmid or topEdgeTop == lmid) and (topEdgeFront == fmid or topEdgeFront == lmid)
        if self.f2lCornerOnTop():
            while True:
                self.solveFrontSlot()
                if self.f2lCorrect():
                    break
                self.m("U")
        else:
            if self.f2lCornerCheck() == "BR":
                if BREdge:
                    self.m("Ri Ui R U2")
                else:
                    self.m("Ri U R U")
            elif self.f2lCornerCheck() == "BL":
                if BLEdge:
                    self.m("L U Li U")
                else:
                    self.m("L Ui Li U2")
            elif self.f2lCornerCheck() == "FL":
                if FLEdge:
                    self.m("Li U L Ui")
                else:
                    self.m("Li Ui L")
        self.solveFrontSlot()

        if not self.f2lCorrect():
            raise Exception("Exception found in f2lEdgeNoCorner()")


    
    def f2lCornerNoEdge(self):
        topEdgeTop = self.cube[0][2][1]
        topEdgeFront = self.cube[1][0][1]
        rmid = self.cube[2][1][1]
        bmid = self.cube[5][1][1]
        lmid = self.cube[3][1][1]
        fmid = self.cube[1][1][1]
        
        BREdge = (topEdgeTop == rmid or topEdgeTop == bmid) and (topEdgeFront == rmid or topEdgeFront == bmid)
        BLEdge = (topEdgeTop == lmid or topEdgeTop == bmid) and (topEdgeFront == lmid or topEdgeFront == bmid)
        FLEdge = (topEdgeTop == fmid or topEdgeTop == lmid) and (topEdgeFront == fmid or topEdgeFront == lmid)
        if self.f2lEdgeOnTop():
            while True:
                self.solveFrontSlot()
                if self.f2lCorrect():
                    break
                self.m("U")
        else:
            if self.f2lEdgeCheck() == "BR":
                if BREdge:
                    self.m("Ri Ui R U2")
                else:
                    self.m("Ri U R U")
            elif self.f2lEdgeCheck() == "BL":
                if BLEdge:
                    self.m("L U Li U")
                else:
                    self.m("L Ui Li U2")
            elif self.f2lEdgeCheck() == "FL":
                if FLEdge:
                    self.m("Li U L Ui")
                else:
                    self.m("Li Ui L")
        self.solveFrontSlot()

        if not self.f2lCorrect():
            raise Exception("Exception found in f2lCornerNoEdge()")



    def f2lCornerTopNoEdge(self):
        topEdgeTop = self.cube[0][2][1]
        topEdgeFront = self.cube[1][0][1]
        rmid = self.cube[2][1][1]
        bmid = self.cube[5][1][1]
        lmid = self.cube[3][1][1]
        fmid = self.cube[1][1][1]
        BREdge = (topEdgeTop == rmid or topEdgeTop == bmid) and (topEdgeFront == rmid or topEdgeFront == bmid)
        BLEdge = (topEdgeTop == lmid or topEdgeTop == bmid) and (topEdgeFront == lmid or topEdgeFront == bmid)
        FLEdge = (topEdgeTop == fmid or topEdgeTop == lmid) and (topEdgeFront == fmid or topEdgeFront == lmid)

        
        while True:
            if self.f2lFRCor():
                break
            self.m("U")
        
        if self.f2lEdgeCheck() == "BR":
            if BREdge:
                self.m("Ri Ui R")
            else:
                self.m("Ri U R")
        elif self.f2lEdgeCheck() == "BL":
            if BLEdge:
                self.m("U2 L Ui Li")
            else:
                self.m("L Ui Li U")
        elif self.f2lEdgeCheck() == "FL":
            if FLEdge:
                self.m("U2 Li Ui L U2")
            else:
                self.m("Li Ui L U")
        self.solveFrontSlot()

        if not self.f2lCorrect():
            raise Exception("Exception found in f2lCornerTopNoEdge()")


    def f2lEdgeTopNoCorner(self):
        BackEdgeTop = self.cube[0][0][1]
        BackEdgeBack = self.cube[5][2][1]
        rmid = self.cube[2][1][1]
        bmid = self.cube[5][1][1]
        lmid = self.cube[3][1][1]
        fmid = self.cube[1][1][1]
        rs1 = BackEdgeTop == rmid or BackEdgeTop == bmid
        rs2 = BackEdgeBack == rmid or BackEdgeBack == bmid
        BREdge = rs1 and rs2
        BLEdge = (BackEdgeTop == lmid or BackEdgeTop == bmid) and (BackEdgeBack == lmid or BackEdgeBack == bmid)
        FLEdge = (BackEdgeTop == fmid or BackEdgeTop == lmid) and (BackEdgeBack == fmid or BackEdgeBack == lmid)

        
        while True:
            if self.f2lFUEdge():
                break
            self.m("U")
        
        if self.f2lCornerCheck() == "BR":
            if BREdge:
                self.m("Ri U R U")
            else:
                self.m("Ui Ri U R U")
        elif self.f2lCornerCheck() == "BL":
            if BLEdge:
                self.m("L Ui Li U2")
            else:
                self.m("U2 L U2 Li")
        elif self.f2lCornerCheck() == "FL":
            if FLEdge:
                self.m("Li Ui L")
            else:
                self.m("U Li Ui L")
        self.solveFrontSlot()

        if not self.f2lCorrect():
            raise Exception("Exception found in f2lEdgeTopNoCorner()")


    
    def f2lNoEdgeOrCorner(self):
       

        BackEdgeTop = self.cube[0][0][1]
        BackEdgeBack = self.cube[5][2][1]
        rmid = self.cube[2][1][1]
        bmid = self.cube[5][1][1]
        lmid = self.cube[3][1][1]
        fmid = self.cube[1][1][1]
      
        BREdge = (BackEdgeTop == rmid or BackEdgeTop == bmid) and (BackEdgeBack == rmid or BackEdgeBack == bmid)
        BLEdge = (BackEdgeTop == lmid or BackEdgeTop == bmid) and (BackEdgeBack == lmid or BackEdgeBack == bmid)
        FLEdge = (BackEdgeTop == fmid or BackEdgeTop == lmid) and (BackEdgeBack == fmid or BackEdgeBack == lmid)

       
        if self.f2lCornerCheck() == "BR":
            if BREdge:
                self.m("Ri U R U")
            else:
                self.m("Ui Ri U R U")
        elif self.f2lCornerCheck() == "BL":
            if BLEdge:
                self.m("L Ui Li U2")
            else:
                self.m("U2 L U2 Li")
        elif self.f2lCornerCheck() == "FL":
            if FLEdge:
                self.m("Li Ui L")
            else:
                self.m("U Li Ui L")
        self.solveFrontSlot()

        if self.f2lCorrect():
            return
        else:
            self.f2lCornerTopNoEdge()

        if not self.f2lCorrect():
            raise Exception("Exception found in f2lNoEdgeOrCorner()")



    def isf2lDone(self):
        rside = self.cube[2][0][1] == self.cube[2][0][2] == self.cube[2][1][1] == self.cube[2][1][2] == self.cube[2][2][1] == self.cube[2][2][2]
        bside = self.cube[5][0][0] == self.cube[5][0][1] == self.cube[5][0][2] == self.cube[5][1][0] == self.cube[5][1][1] == self.cube[5][1][2]
        lside = self.cube[3][0][0] == self.cube[3][0][1] == self.cube[3][1][0] == self.cube[3][1][1] == self.cube[3][2][0] == self.cube[3][2][1]
        fside = self.cube[1][1][0] == self.cube[1][1][1] == self.cube[1][1][2] == self.cube[1][2][0] == self.cube[1][2][1] == self.cube[1][2][2]
        return rside and bside and lside and fside


  
    def f2l(self):
        pairsSolved = 0
        while pairsSolved < 4:
            # Look ahead for easiest pair
            best_pair = self.findEasiestF2LPair()
            moves_to_position = self.movesToPosition(best_pair)
            
            # Execute optimal sequence
            self.m(moves_to_position)
            
            if not self.f2lCorrect():
                if self.f2lEdgeOnTop() and self.f2lCornerOnTop():
                    self.solvePairFromTop()
                elif self.f2lEdgeInserted():
                    self.f2lEdgeNoCorner()
                elif self.f2lCornerInserted():
                    self.f2lCornerNoEdge()
                else:
                    self.f2lNoEdgeOrCorner()
            
            pairsSolved += 1
            self.m("Y")
            self.simplify_moves()
        
    def findEasiestF2LPair(self):
    # Check all possible pairs and score them based on moves needed
        pairs = []
        for _ in range(4):
            if not self.f2lCorrect():
                pair_data = {
                    'corner': self.f2lCornerCheck(),
                    'edge': self.f2lEdgeCheck(),
                    'moves': self.estimateMovesForPair()
                }
                pairs.append(pair_data)
            self.m("Y")
        
        # Return pair requiring fewest moves
        return min(pairs, key=lambda x: x['moves'])


    def fish(self):
        return [self.cube[0][0][0], self.cube[0][0][2], self.cube[0][2][0], self.cube[0][2][2]].count(self.cube[0][1][1]) == 1


    def sune(self):
        self.m("R U Ri U R U2 Ri")


    def antisune(self):
        self.m("R U2 Ri Ui R Ui Ri")


    def getfish(self):
        for i in range(4):
            if self.fish():
                return
            self.sune()
            if self.fish():
                return
            self.antisune()
            self.m("U")
        assert self.fish()


    def bOLL(self):
        # Create OLL pattern recognition
        top_pattern = [
            [self.cube[0][0][0], self.cube[0][0][1], self.cube[0][0][2]],
            [self.cube[0][1][0], self.cube[0][1][1], self.cube[0][1][2]],
            [self.cube[0][2][0], self.cube[0][2][1], self.cube[0][2][2]]
        ]
        
        # Use pattern matching for direct algorithm selection
        pattern_key = self.getOLLPattern(top_pattern)
        if pattern_key in OLL_ALGORITHMS:
            self.m(OLL_ALGORITHMS[pattern_key])
        else:
            # Fallback to original fish method if pattern not recognized
            self.getfish()
            if self.fish():
                self.solveFish()
        
        self.simplify_moves()


    def getCornerState(self):
        corner0 = self.cube[1][0][0] == self.cube[1][1][1] and self.cube[3][2][2] == self.cube[3][1][1]
        corner1 = self.cube[1][0][2] == self.cube[1][1][1] and self.cube[2][2][0] == self.cube[2][1][1]
        corner2 = self.cube[5][2][2] == self.cube[5][1][1] and self.cube[2][0][0] == self.cube[2][1][1]
        corner3 = self.cube[5][2][0] == self.cube[5][1][1] and self.cube[3][0][2] == self.cube[3][1][1]
        return [corner0, corner1, corner2, corner3]


    # permutation of the top corners
    def permuteCorners(self):
        for i in range(2):
            for j in range(4):
                num = self.getCornerState().count(True)
                if num == 4:
                    return
                if num == 1:
                    index = self.getCornerState().index(True)
                    for k in range(index):
                        self.m("Y")
                    if self.cube[1][0][2] == self.cube[2][1][1]:
                        self.m("R2 B2 R F Ri B2 R Fi R")
                    else:
                        self.m("Ri F Ri B2 R Fi Ri B2 R2")
                    for f in range(index):
                        self.m("Yi")
                    return
                self.m("U")
            self.m("R2 B2 R F Ri B2 R Fi R")


    # permutation of top edges
    def permuteEdges(self):
        if all(self.getEdgeState()):
            return
        if self.cube[1][0][1] == self.cube[5][1][1] and self.cube[5][2][1] == self.cube[1][1][1]:  # H perm
            self.m("R2 U2 R U2 R2 U2 R2 U2 R U2 R2")
        elif self.cube[1][0][1] == self.cube[2][1][1] and self.cube[2][1][0] == self.cube[1][1][1]:  # Normal Z perm
            self.m("U Ri Ui R Ui R U R Ui Ri U R U R2 Ui Ri U")
        elif self.cube[1][0][1] == self.cube[3][1][1] and self.cube[3][1][2] == self.cube[1][1][1]:  # Not oriented Z perm
            self.m("Ri Ui R Ui R U R Ui Ri U R U R2 Ui Ri U2")
        else:
            uNum = 0
            while True:
                if self.cube[5][2][0] == self.cube[5][2][1] == self.cube[5][2][2]:  # solid bar is on back then
                    if self.cube[3][1][2] == self.cube[1][0][0]:  # means we have to do counterclockwise cycle
                        self.m("R Ui R U R U R Ui Ri Ui R2")
                        break
                    else:
                        self.m("R2 U R U Ri Ui Ri Ui Ri U Ri")
                        break
                else:
                    self.m("U")
                    uNum += 1
            for x in range(uNum):
                self.m("Ui")


    def getEdgeState(self):
        fEdge = self.cube[1][0][1] == self.cube[1][1][1]
        rEdge = self.cube[2][1][0] == self.cube[2][1][1]
        bEdge = self.cube[5][2][1] == self.cube[5][1][1]
        lEdge = self.cube[3][1][2] == self.cube[3][1][1]
        return [fEdge, rEdge, bEdge, lEdge]


    def topCorners(self):
        self.permuteCorners()
        assert all(self.getCornerState())


    def topEdges(self):
        self.permuteEdges()
        assert all(self.getEdgeState())


    def bPLL(self):
        # Get PLL case pattern
        pattern = self.getPLLPattern()
        
        # Direct algorithm lookup
        PLL_ALGORITHMS = {
            'H': "M2 U M2 U2 M2 U M2",
            'Ua': "R U' R U R U R U' R' U' R2",
            'Ub': "R2 U R U R' U' R' U' R' U R'",
            'Z': "M2 U M2 U M' U2 M2 U2 M' U2",
            # Add more PLL cases
        }
        
        if pattern in PLL_ALGORITHMS:
            self.m(PLL_ALGORITHMS[pattern])
        else:
            # Fallback to original corner/edge permutation
            self.topCorners()
            self.topEdges()
        
        self.simplify_moves()




    def solve(self):
        print("Starting solve...")
        
        print("Solving cross...")
        self.cross()
        
        print("Solving F2L...")
        self.f2l()
        
        print("Solving OLL...")
        self.bOLL()
        
        print("Solving PLL...")
        self.bPLL()
        
        print("Solution completed!")
        print(f"Total moves: {len(self.moves_list)}")
        print(f"Cross: {self.step_moves_list[0]} moves")
        print(f"F2L: {self.step_moves_list[1]} moves")
        print(f"OLL: {self.step_moves_list[2]} moves")
        print(f"PLL: {self.step_moves_list[3]} moves")

def solve_cube(cube_data):
    
        
        solver = CubeSolver(cube_data)
        solver.solve()
        print(solver.get_moves())
        print("total moves:", len(solver.get_moves()))
 
    


cube_data = { 'top': [['Y', 'Y', 'G'],
             ['W', 'W', 'Y'],
             ['W', 'B', 'G']],  # Up/white

            'front': [['B', 'Y', 'O'],
             ['B', 'G', 'W'],
             ['B', 'R', 'R']],  # front/green

            'right': [['Y', 'R', 'R'],
             ['G', 'R', 'R'],
             ['Y', 'B', 'B']],  # right/red

            'left': [['O', 'O', 'B'],
             ['O', 'O', 'G'],
             ['O', 'O', 'R']],  # left/orange

            'bottom': [['W', 'Y', 'Y'],
             ['W', 'Y', 'W'],
             ['W', 'R', 'W']],  # down/yellow

            'back': [['G', 'B', 'G'],
             ['G', 'B', 'G'],
             ['O', 'O', 'R']]};


solution = solve_cube(cube_data)