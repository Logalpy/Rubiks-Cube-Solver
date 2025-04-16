from tkinter import *
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/solve1": {"origins": "http://localhost:3000"},
    r"/solve2": {"origins": "http://localhost:3000"}
})

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







    def get_moves(self):
        self.simplify_moves()
        s = ""
        for i in self.moves_list:
            s += str(i) + " "
        s = str.replace(s, "i", "'")[:-1]
        return s




    def all_same(items):
        return all(x == items[0] for x in items)


    # translates moves
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


    # remove redundancies
    def simplify_moves(self):
        new_list = []
        prev_move = ""
        yCount = 0
        for move in self.moves_list:
            if move == "Y":
                yCount += 1
                yCount %= 4
                continue
            if move == "Yi":
                yCount += 3
                yCount %= 4
                continue
            if move == "Y2":
                yCount += 2
                yCount %= 4
                continue
            if yCount > 0:
                for i in range(yCount):
                    move = self.yTransform(move)
            if prev_move == "" or prev_move == '':
                prev_move = move
                new_list.append(move)
                continue
            if move[0] == prev_move[0]:
                if len(move) == 1:
                    if len(prev_move) <= 1:
                        del new_list[-1]
                        mv = move[0] + "2"
                        new_list.append(mv)
                        prev_move = mv
                        continue
                    if prev_move[1] == "i":
                        del new_list[-1]
                        prev_move = new_list[-1] if len(new_list) > 0 else ""
                        continue
                    if prev_move[1] == "2":
                        del new_list[-1]
                        mv = move[0] + "i"
                        new_list.append(mv)
                        prev_move = mv
                        continue
                if move[1] == "i":
                    if len(prev_move) == 1:
                        del new_list[-1]
                        prev_move = new_list[-1] if len(new_list) > 0 else ""
                        continue
                    if prev_move[1] == "i":
                        del new_list[-1]
                        mv = move[0] + "2"
                        new_list.append(mv)
                        prev_move = mv
                        continue
                    if prev_move[1] == "2":
                        del new_list[-1]
                        mv = move[0]
                        new_list.append(mv)
                        prev_move = mv
                        continue
                if move[1] == "2":
                    if len(prev_move) == 1:
                        del new_list[-1]
                        mv = move[0] + "i"
                        new_list.append(mv)
                        prev_move = mv
                        continue
                    if prev_move[1] == "i":
                        del new_list[-1]
                        mv = move[0]
                        new_list.append(mv)
                        prev_move = mv
                        continue
                    if prev_move[1] == "2":
                        del new_list[-1]
                        prev_move = new_list[-1] if len(new_list) > 0 else ""
                        continue
            new_list.append(move)
            prev_move = move
        self.solution_length = len(new_list)
        self.moves_list = new_list


    # gets cube in position for U
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


    # reverses the setup
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


    # limit moves to performing U moves, by setting up, doing the move, and undoing the setup
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


    # Rotate face counter-clockwise
    def rotate_face_counterclockwise(self,face):
        self.rotate_face_clockwise(face)
        self.rotate_face_clockwise(face)
        self.rotate_face_clockwise(face)


    # Rotate face clockwise
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


    # part of the OLL step
    def topCross(self):
       
        if self.cube[0][0][1] == self.cube[0][1][0] == self.cube[0][1][2] == self.cube[0][2][1]:
         
            return
    
        else:
            while self.cube[0][0][1] != "W" or self.cube[0][1][0] != "W" or self.cube[0][1][2] != "W" or self.cube[0][2][1] != "W":
                if self.cube[0][1][0] == self.cube[0][1][2]:
                   
                    self.m("F R U Ri Ui Fi")
                    break  
                elif self.cube[0][0][1] == self.cube[0][2][1]:
                    
                    self.m("U F R U Ri Ui Fi")
                    break
                elif self.cube[0][0][1] != "W" and self.cube[0][1][0] != "W" and self.cube[0][1][2] != "W" and self.cube[0][2][1] != "W":
                   
                    self.m("F U R Ui Ri Fi U F R U Ri Ui Fi")
                    break
                elif self.cube[0][1][2] == self.cube[0][2][1] or self.cube[0][0][1] == self.cube[0][1][0]:
                    
                    self.m("F R U Ri Ui Fi")
                else:
                    
                    self.m("U")


    def isTopSolved(self):
        if self.cube[0][0][0] == self.cube[0][0][1] == self.cube[0][0][2] == self.cube[0][1][0] == self.cube[0][1][1] == self.cube[0][1][2] == self.cube[0][2][0] == self.cube[0][2][1] == \
                self.cube[0][2][2]:
            return True
        else:
            return False


    # puts an edge in its right spot
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
        for i in range(4):
            self.putCrossEdge()
            assert "Y" in [self.cube[4][0][1], self.cube[1][2][1]]
            if self.cube[1][2][1] == "Y":
                self.m("Fi R U Ri F2")   #orient if necessary
            self.m("Di")

        #permute to correct face: move down face until 2 are lined up,
        #then swap the other 2 if they need to be swapped
        condition = False
        while not condition:
            fSame = self.cube[1][1][1] == self.cube[1][2][1]
            rSame = self.cube[2][1][1] == self.cube[2][1][2]
            bSame = self.cube[5][1][1] == self.cube[5][0][1]
            lSame = self.cube[3][1][1] == self.cube[3][1][0]
            condition = (fSame, rSame, bSame, lSame).count(True) >= 2
            if not condition:
                self.m("D")
        if (fSame, rSame, bSame, lSame).count(True) == 4:
            return
        assert (fSame, rSame, bSame, lSame).count(True) == 2
        if not fSame and not bSame:
            self.m("F2 U2 B2 U2 F2") #swap front-back
        elif not rSame and not lSame:
            self.m("R2 U2 L2 U2 R2") #swap right-left
        elif not fSame and not rSame:
            self.m("F2 Ui R2 U F2") #swap front-right
        elif not rSame and not bSame:
            self.m("R2 Ui B2 U R2") #swap right-back
        elif not bSame and not lSame:
            self.m("B2 Ui L2 U B2") #swap back-left
        elif not lSame and not fSame:
            self.m("L2 Ui F2 U L2") #swap left-front
        fSame = self.cube[1][1][1] == self.cube[1][2][1]
        rSame = self.cube[2][1][1] == self.cube[2][1][2]
        bSame = self.cube[5][1][1] == self.cube[5][0][1]
        lSame = self.cube[3][1][1] == self.cube[3][1][0]
        assert all([fSame, rSame, bSame, lSame])


    # This is uses all the f2l algs to solve all the cases possible
    def solveFrontSlot(self):
        # This will be F2L, with all 42 cases
        rmid = self.cube[2][1][1]
        fmid = self.cube[1][1][1]
        dmid = self.cube[4][1][1]
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


    # returns true if f2l corner is inserted, doesn't have to be orientated correctly
    def f2lCornerInserted(self):
        rmid = self.cube[2][1][1]
        fmid = self.cube[1][1][1]
        dmid = self.cube[4][1][1]
        # Corner orientations for correct location in D layer
        fCorD = self.cube[1][2][2] == dmid and self.cube[2][2][2] == fmid and self.cube[4][0][2] == rmid
        rCorD = self.cube[2][2][2] == dmid and self.cube[4][0][2] == fmid and self.cube[1][2][2] == rmid
        dCorD = self.cube[4][0][2] == dmid and self.cube[1][2][2] == fmid and self.cube[2][2][2] == rmid  # This is solved spot
        return fCorD or rCorD or dCorD


    # Returns true if there is an f2l corner located in the FR orientation
    def f2lFRCor(self):
        rmid = self.cube[2][1][1]
        fmid = self.cube[1][1][1]
        dmid = self.cube[4][1][1]
        # corner orientations if in U layer, first letter means the direction that the color is facing
        fCorU = self.cube[1][0][2] == dmid and self.cube[0][2][2] == fmid and self.cube[2][2][0] == rmid
        rCorU = self.cube[2][2][0] == dmid and self.cube[1][0][2] == fmid and self.cube[0][2][2] == rmid
        uCorU = self.cube[0][2][2] == dmid and self.cube[2][2][0] == fmid and self.cube[1][0][2] == rmid
        return fCorU or rCorU or uCorU


    # Returns true if there is an f2l Edge located in the FU position
    def f2lFUEdge(self):
        rmid = self.cube[2][1][1]
        fmid = self.cube[1][1][1]
        norEdgeFU = self.cube[1][0][1] == fmid and self.cube[0][2][1] == rmid
        flipEdgeFU = self.cube[0][2][1] == fmid and self.cube[1][0][1] == rmid
        return norEdgeFU or flipEdgeFU


    # returns true if f2l corner is located on the U layer
    def f2lCornerOnTop(self):
        wasFound = False
        for i in range(4):  # Does 4 U moves to find the corner
            if self.f2lFRCor():
                wasFound = True
            self.m("U")
        return wasFound


    # Will return the loction of the corner that belongs in the FR spot. Either returns BR, BL, FL, or FR.
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


    # Will return the loction of the edge that belongs in the FR spot.
    # Either returns BR, BL, FL, or FR.
    def f2lEdgeCheck(self):
        if self.f2lEdgeInserted2("FL"):
            return "FL"
        elif self.f2lEdgeInserted2("BL"):
            return "BL"
        elif self.f2lEdgeInserted2("BR"):
            return "BR"
        elif self.f2lEdgeInserted2("FR"):
            return "FR"
        else:
            raise Exception("f2lEdgeCheck() Exception")



    # This is for the case where the Edge is inserted, but the corner is not
    def f2lEdgeNoCorner(self):
        topEdgeTop = self.cube[0][2][1]
        topEdgeFront = self.cube[1][0][1]
        rmid = self.cube[2][1][1]
        bmid = self.cube[5][1][1]
        lmid = self.cube[3][1][1]
        fmid = self.cube[1][1][1]
        # This is for comparing the front edge to other various edges for advanced algs/lookahead
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


    # This is the case for if the corner is inserted, but the edge is not
    def f2lCornerTopNoEdge(self):
        self.topEdgeTop = self.cube[0][2][1]
        self.topEdgeFront = self.cube[1][0][1]
        self.rmid = self.cube[2][1][1]
        self.bmid = self.cube[5][1][1]
        self.lmid = self.cube[3][1][1]
        self.fmid = self.cube[1][1][1]
        #This is for comparing the front edge to other various edges for advanced algs/lookahead
        BREdge = (self.topEdgeTop == self.rmid or self.topEdgeTop == self.bmid) and (self.topEdgeFront == self.rmid or self.topEdgeFront == self.bmid)
        BLEdge = (self.topEdgeTop == self.lmid or self.topEdgeTop == self.bmid) and (self.topEdgeFront == self.lmid or self.topEdgeFront == self.bmid)
        FLEdge = (self.topEdgeTop == self.fmid or self.topEdgeTop == self.lmid) and (self.topEdgeFront == self.fmid or self.topEdgeFront == self.lmid)

        #Turn the top until the corner on the U face is in the proper position
        while True:
            if self.f2lFRCor():
                break
            self.m("U")
        #We will be checking additional edges to choose a more fitting alg for the sake of looking ahead
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


    # this is the case for if the corner is on top, and the edge is not. Neither are inserted properly. Edge must be in another slot.
    def f2lCornerTopNoEdge(self):
        self.BackEdgeTop = self.cube[0][0][1]
        self.BackEdgeBack = self.cube[5][2][1]
        self.rmid = self.cube[2][1][1]
        self.bmid = self.cube[5][1][1]
        self.lmid = self.cube[3][1][1]
        self.fmid = self.cube[1][1][1]
        #This is for comparing the back edge to other various edges for advanced algs/lookahead
        BREdge = (self.BackEdgeTop == self.rmid or self.BackEdgeTop == self.bmid) and (self.BackEdgeBack == self.rmid or self.BackEdgeBack == self.bmid)
        BLEdge = (self.BackEdgeTop == self.lmid or self.BackEdgeTop == self.bmid) and (self.BackEdgeBack == self.lmid or self.BackEdgeBack == self.bmid)
        FLEdge = (self.BackEdgeTop == self.fmid or self.BackEdgeTop == self.lmid) and (self.BackEdgeBack == self.fmid or self.BackEdgeBack == self.lmid)

        # Turn the top until the corner on the U face is in the proper position
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


    # This is the case for if the edge is on top, and the corner is not. Neither are inserted properly. Corner must be in another slot.
    # The lookahead for this step is comparing the back edge to the slots, rather than the front one like other cases have
    def f2lEdgeTopNoCorner(self):
        BackEdgeTop = self.cube[0][0][1]
        BackEdgeBack = self.cube[5][2][1]
        rmid = self.cube[2][1][1]
        bmid = self.cube[5][1][1]
        lmid = self.cube[3][1][1]
        fmid = self.cube[1][1][1]
        rs1 = BackEdgeTop == rmid or BackEdgeTop == bmid
        rs2 = BackEdgeBack == rmid or BackEdgeBack == bmid
        # This is for comparing the back edge to other various edges for advanced algs/lookahead
        BREdge = rs1 and rs2
        BLEdge = (BackEdgeTop == lmid or BackEdgeTop == bmid) and (BackEdgeBack == lmid or BackEdgeBack == bmid)
        FLEdge = (BackEdgeTop == fmid or BackEdgeTop == lmid) and (BackEdgeBack == fmid or BackEdgeBack == lmid)

        # Turn the top until the corner on the U face is in the proper position
        while True:
            if self.f2lFUEdge():
                break
            self.m("U")
        # We will be checking additional edges to choose a more fitting alg for the sake of looking ahead
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



    # Will return true if the f2l is completed
    def isf2lDone(self):
        rside = self.cube[2][0][1] == self.cube[2][0][2] == self.cube[2][1][1] == self.cube[2][1][2] == self.cube[2][2][1] == self.cube[2][2][2]
        bside = self.cube[5][0][0] == self.cube[5][0][1] == self.cube[5][0][2] == self.cube[5][1][0] == self.cube[5][1][1] == self.cube[5][1][2]
        lside = self.cube[3][0][0] == self.cube[3][0][1] == self.cube[3][1][0] == self.cube[3][1][1] == self.cube[3][2][0] == self.cube[3][2][1]
        fside = self.cube[1][1][0] == self.cube[1][1][1] == self.cube[1][1][2] == self.cube[1][2][0] == self.cube[1][2][1] == self.cube[1][2][2]
        return rside and bside and lside and fside


    # f2l will solve the first 2 layers, checks for each case, then does a Y move to check the next
    def f2l(self):
        pairsSolved = 0
        uMoves = 0
        while pairsSolved < 4:
            if not self.f2lCorrect():
                # while not f2lCorrect():
                while uMoves < 4:  # 4 moves before checking rare cases
                    self.solveFrontSlot()
                    if self.f2lCorrect():
                        pairsSolved += 1
                        self.f2l_list.append("Normal Case")
                        break
                    else:
                        self.f2l_list.append("Scanning")
                        uMoves += 1
                        self.m("U")
                if not self.f2lCorrect():
                    if not self.f2lCornerInserted() and self.f2lEdgeInserted():
                        self.f2l_list.append("Rare case 1")
                        self.f2lEdgeNoCorner()
                        pairsSolved += 1
                    elif not self.f2lEdgeInserted() and self.f2lCornerInserted():
                        self.f2l_list.append("Rare case 2")
                        self.f2lCornerNoEdge()
                        pairsSolved += 1
                    # At this point, they can't be inserted, must be in U or other spot
                    elif not self.f2lEdgeOnTop() and self.f2lCornerOnTop():
                        self.f2l_list.append("Rare Case 3")
                        self.f2lCornerTopNoEdge()
                        pairsSolved += 1
                    elif self.f2lEdgeOnTop() and not self.f2lCornerOnTop():
                        self.f2l_list.append("Rare Case 4")
                        self.f2lEdgeTopNoCorner()
                        self.solveFrontSlot()
                        pairsSolved += 1
                    elif not self.f2lEdgeOnTop() and not self.f2lCornerOnTop():
                        self.f2l_list.append("Rare Case 5")
                        self.f2lNoEdgeOrCorner()
                        pairsSolved += 1
                    else:
                        raise Exception("f2l Impossible Case Exception")
            else:
                pairsSolved += 1
            self.f2l_list.append("We have ")
            self.f2l_list.append(str(pairsSolved))
            uMoves = 0
            self.m("Y")
        assert (self.isf2lDone())


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
        self.getfish()
        if self.fish():
            while self.cube[0][0][2] != self.cube[0][1][1]:
                self.m("U")
            if self.cube[1][0][0] == self.cube[0][1][1]:
                self.antisune()
            elif self.cube[5][2][0] == self.cube[0][1][1]:
                self.m("U2");
                self.sune();
            else:
                raise Exception("Something went wrong")
        else:
            raise Exception("Fish not set up")
        assert self.isTopSolved()


    def getCornerState(self):
        corner0 = self.cube[1][0][0] == self.cube[1][1][1] and self.cube[3][2][2] == self.cube[3][1][1]
        corner1 = self.cube[1][0][2] == self.cube[1][1][1] and self.cube[2][2][0] == self.cube[2][1][1]
        corner2 = self.cube[5][2][2] == self.cube[5][1][1] and self.cube[2][0][0] == self.cube[2][1][1]
        corner3 = self.cube[5][2][0] == self.cube[5][1][1] and self.cube[3][0][2] == self.cube[3][1][1]
        return [corner0, corner1, corner2, corner3]


    # Does permutation of the top layer corners, orients them properly
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


    # Does permutation of the top layer edges, must be H, Z or U perms after orientation
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
        self.topCorners()
        self.topEdges()


    def isSolved(self):
        uside = self.cube[0][0][0] == self.cube[0][0][1] == self.cube[0][0][2] == self.cube[0][1][0] == self.cube[0][1][1] == self.cube[0][1][2] == self.cube[0][2][0] == self.cube[0][2][
            1] == self.cube[0][2][2]
        fside = self.cube[1][0][0] == self.cube[1][0][1] == self.cube[1][0][2] == self.cube[1][1][0] == self.cube[1][1][1] == self.cube[1][1][2] == self.cube[1][2][0] == self.cube[1][2][
            1] == self.cube[1][2][2]
        rside = self.cube[2][0][0] == self.cube[2][0][1] == self.cube[2][0][2] == self.cube[2][1][0] == self.cube[2][1][1] == self.cube[2][1][2] == self.cube[2][2][0] == self.cube[2][2][
            1] == self.cube[2][2][2]
        lside = self.cube[3][0][0] == self.cube[3][0][1] == self.cube[3][0][2] == self.cube[3][1][0] == self.cube[3][1][1] == self.cube[3][1][2] == self.cube[3][2][0] == self.cube[3][2][
            1] == self.cube[3][2][2]
        dside = self.cube[4][0][0] == self.cube[4][0][1] == self.cube[4][0][2] == self.cube[4][1][0] == self.cube[4][1][1] == self.cube[4][1][2] == self.cube[4][2][0] == self.cube[4][2][
            1] == self.cube[4][2][2]
        bside = self.cube[5][0][0] == self.cube[5][0][1] == self.cube[5][0][2] == self.cube[5][1][0] == self.cube[5][1][1] == self.cube[5][1][2] == self.cube[5][2][0] == self.cube[5][2][
            1] == self.cube[5][2][2]
        return uside and fside and rside and lside and dside and bside


    def isCrossSolved(self):
        # Check if bottom cross edges match the center color
        bottom_center = self.cube[4][1][1]  # Yellow center
        
        # Check if all cross edges on bottom face are yellow
        cross_edges_yellow = (
            self.cube[4][0][1] == bottom_center and  # Front edge
            self.cube[4][1][2] == bottom_center and  # Right edge
            self.cube[4][2][1] == bottom_center and  # Back edge
            self.cube[4][1][0] == bottom_center      # Left edge
        )
        
        # Check if cross edges match their center colors
        edges_aligned = (
            self.cube[1][2][1] == self.cube[1][1][1] and  # Front edge matches front center
            self.cube[2][2][1] == self.cube[2][1][1] and  # Right edge matches right center
            self.cube[5][2][1] == self.cube[5][1][1] and  # Back edge matches back center
            self.cube[3][2][1] == self.cube[3][1][1]      # Left edge matches left center
        )
        
        return cross_edges_yellow and edges_aligned


    def solve(self):
        
        self.cross()
        self.simplify_moves()
        self.step_moves_list[0] = self.solution_length
        self.f2l()
        self.simplify_moves()
        self.step_moves_list[1] = self.solution_length - self.step_moves_list[0]
        self.topCross()
        self.getfish()
        self.bOLL()
        self.simplify_moves()
        self.step_moves_list[2] = self.solution_length - self.step_moves_list[1] - self.step_moves_list[0]
        self.bPLL()
        self.simplify_moves()
        self.step_moves_list[3] = self.solution_length - self.step_moves_list[2] - self.step_moves_list[1] - self.step_moves_list[0]
        assert (self.isSolved())

@app.route('/solve1', methods=['POST'])
def solve_cube():
    try:
        cube_data = request.json
        solver = CubeSolver(cube_data)
        solver.solve()
        response1 = jsonify({'status': 'success', 'solution': solver.moves_list})
        response1.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        return response1
    except Exception as e:
        print("Error:", str(e))
        response1 = jsonify({'status': 'error', 'message': str(e)})
        response1.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        return response1, 400
    
@app.route('/solve1', methods=['OPTIONS'])
def solve_cube_options():
    response = jsonify()
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response
    
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5000, debug = True)



