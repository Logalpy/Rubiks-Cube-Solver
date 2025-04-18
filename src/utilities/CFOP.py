from tkinter import *
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from .cube import RubiksCube

app = Flask(__name__)
CORS(app, resources={
    r"/solve1": {"origins": "http://localhost:3000"},
    r"/solve2": {"origins": "http://localhost:3000"}
})

class CubeSolver:
    def __init__(self, cube_data):
        self.cube = RubiksCube()
        self.cube.load_from_cube_data(cube_data)
        self.moves_list = []
        self.last_scramble = []
        self.f2l_list = []
        self.step_moves_list = [0, 0, 0, 0]
        self.solution_length = 0

    def get_moves(self):
        self.simplify_moves()
        s = ""
        for i in self.moves_list:
            s += str(i) + " "
        s = str.replace(s, "i", "'")[:-1]
        return s

    def all_same(items):
        return all(x == items[0] for x in items)

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

    def m(self, s):
        s = str.replace(s, "'", "i")
        k = s.split(' ')
        self.solution_length += len(k)
        for word in k:
            self.moves_list.append(word)
            self.move(word)

    def move(self, mv):
        mv = str.replace(mv, "'", "i")  # Convert notation to match RubiksCube class
        self.cube.move(mv)

    def rotate(self, axis):
        # Convert X, Y, Z rotations into the equivalent face moves
        axis = str.upper(axis)
        if axis == 'X':
            # X rotation is equivalent to R rotation of entire cube
            self.move("L'")
            self.move("M'")
            self.move("R")
        elif axis == 'Y':
            # Y rotation is equivalent to U rotation of entire cube
            self.move("U")
            self.move("E'")
            self.move("D'")
        elif axis == 'Z':
            # Z rotation is equivalent to F rotation of entire cube
            self.move("F")
            self.move("S")
            self.move("B'")

    def U(self):
        self.move("U")

    def rotate_face_clockwise(self, face):
        face = face.upper()  # RubiksCube uses uppercase face letters
        self.cube.rotate_face_clockwise(face)

    def rotate_face_counterclockwise(self, face):
        face = face.upper()  # RubiksCube uses uppercase face letters
        self.cube.rotate_face_counterclockwise(face)

    def topCross(self):
        if self.cube.is_top_cross_solved():
            return
        else:
            while not self.cube.is_top_cross_solved():
                if self.cube.is_top_cross_line():
                    self.m("F R U Ri Ui Fi")
                    break
                elif self.cube.is_top_cross_L():
                    self.m("U F R U Ri Ui Fi")
                    break
                elif self.cube.is_top_cross_dot():
                    self.m("F U R Ui Ri Fi U F R U Ri Ui Fi")
                    break
                else:
                    self.m("U")

    def isTopSolved(self):
        return self.cube.is_top_solved()

    def putCrossEdge(self):
        for i in range(3):
            if i == 1:
                self.m("Ri U R F2")  # bring out back-right edge
            elif i == 2:
                self.m("L Ui Li F2")  # bring out back-left edge
            for j in range(4):
                for k in range(4):
                    if "Y" in [self.cube.get_bottom_color(), self.cube.get_front_color()]:
                        return
                    self.m("F")
                self.m("U")

    def cross(self):
        for i in range(4):
            self.putCrossEdge()
            assert "Y" in [self.cube.get_bottom_color(), self.cube.get_front_color()]
            if self.cube.get_front_color() == "Y":
                self.m("Fi R U Ri F2")   #orient if necessary
            self.m("Di")

        condition = False
        while not condition:
            fSame = self.cube.get_front_color() == self.cube.get_front_center()
            rSame = self.cube.get_right_color() == self.cube.get_right_center()
            bSame = self.cube.get_back_color() == self.cube.get_back_center()
            lSame = self.cube.get_left_color() == self.cube.get_left_center()
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
        fSame = self.cube.get_front_color() == self.cube.get_front_center()
        rSame = self.cube.get_right_color() == self.cube.get_right_center()
        bSame = self.cube.get_back_color() == self.cube.get_back_center()
        lSame = self.cube.get_left_color() == self.cube.get_left_center()
        assert all([fSame, rSame, bSame, lSame])

    def solveFrontSlot(self):
        rmid = self.cube.get_right_center()
        fmid = self.cube.get_front_center()
        dmid = self.cube.get_bottom_center()
        fCorU = self.cube.is_f2l_corner_U(dmid, fmid, rmid)
        rCorU = self.cube.is_f2l_corner_U(dmid, rmid, fmid)
        uCorU = self.cube.is_f2l_corner_U(fmid, rmid, dmid)
        fCorD = self.cube.is_f2l_corner_D(dmid, fmid, rmid)
        rCorD = self.cube.is_f2l_corner_D(dmid, rmid, fmid)
        dCorD = self.cube.is_f2l_corner_D(fmid, rmid, dmid)
        norEdgeFU = self.cube.is_f2l_edge_U(fmid, rmid)
        norEdgeLU = self.cube.is_f2l_edge_U(fmid, rmid)
        norEdgeBU = self.cube.is_f2l_edge_U(fmid, rmid)
        norEdgeRU = self.cube.is_f2l_edge_U(fmid, rmid)
        norEdgeAny = norEdgeFU or norEdgeLU or norEdgeBU or norEdgeRU
        flipEdgeFU = self.cube.is_f2l_edge_U(rmid, fmid)
        flipEdgeLU = self.cube.is_f2l_edge_U(rmid, fmid)
        flipEdgeBU = self.cube.is_f2l_edge_U(rmid, fmid)
        flipEdgeRU = self.cube.is_f2l_edge_U(rmid, fmid)
        flipEdgeAny = flipEdgeFU or flipEdgeLU or flipEdgeBU or flipEdgeRU
        norEdgeInsert = self.cube.is_f2l_edge_inserted(fmid, rmid)
        flipEdgeInsert = self.cube.is_f2l_edge_inserted(rmid, fmid)
        backRight = self.cube.is_back_right_slot_open(dmid, rmid)
        frontLeft = self.cube.is_front_left_slot_open(dmid, fmid)

        if dCorD and norEdgeInsert:
            return
        elif fCorU and flipEdgeRU:
            self.m("U R Ui Ri")
        elif rCorU and norEdgeFU:
            self.m("F Ri Fi R")
        elif fCorU and norEdgeLU:
            self.m("Fi Ui F")
        elif rCorU and flipEdgeBU:
            self.m("R U Ri")
        elif fCorU and flipEdgeBU:
            self.m("F2 Li Ui L U F2")
        elif rCorU and norEdgeLU:
            self.m("R2 B U Bi Ui R2")
        elif fCorU and flipEdgeLU:
            self.m("Ui R U2 Ri U2 R Ui Ri")
        elif rCorU and norEdgeBU:
            self.m("U Fi U2 F Ui F Ri Fi R")
        elif fCorU and norEdgeBU:
            self.m("Ui R Ui Ri U Fi Ui F")
        elif rCorU and flipEdgeLU:
            if not backRight:
                self.m("Ri U R2 U Ri")
            else:
                self.m("Ui R U Ri U R U Ri")
        elif fCorU and norEdgeRU:
            self.m("Ui R U2 Ri U Fi Ui F")
        elif rCorU and flipEdgeFU:
            if not backRight:
                self.m("Ri U2 R2 U Ri")
            else:
                self.m("Ri U2 R2 U R2 U R")
        elif fCorU and norEdgeFU:
            if not backRight:
                self.m("Ri U R Fi Ui F")
            else:
                self.m("U Fi U F Ui Fi Ui F")
        elif rCorU and flipEdgeRU:
            self.m("Ui R Ui Ri U R U Ri")
        elif fCorU and flipEdgeFU:
            if not backRight:
                self.m("Ui Ri U R Ui R U Ri")
            elif not frontLeft:
                self.m("U R Ui Ri D R Ui Ri Di")
            else:
                self.m("U Ri F R Fi U R U Ri")
        elif rCorU and norEdgeRU:
            self.m("R Ui Ri U2 Fi Ui F")
        elif uCorU and flipEdgeRU:
            self.m("R U2 Ri Ui R U Ri")
        elif uCorU and norEdgeFU:
            self.m("Fi U2 F U Fi Ui F")
        elif uCorU and flipEdgeBU:
            self.m("U R U2 R2 F R Fi")
        elif uCorU and norEdgeLU:
            self.m("Ui Fi U2 F2 Ri Fi R")
        elif uCorU and flipEdgeLU:
            self.m("R B U2 Bi Ri")
        elif uCorU and norEdgeBU:
            self.m("Fi Li U2 L F")
        elif uCorU and flipEdgeFU:
            self.m("U2 R2 U2 Ri Ui R Ui R2")
        elif uCorU and norEdgeRU:
            self.m("U Fi Li U L F R U Ri")
        elif dCorD and flipEdgeAny:
            if flipEdgeBU:
                self.m("U")
            elif flipEdgeLU:
                self.m("U2")
            elif flipEdgeFU:
                self.m("Ui")
            if not backRight:
                self.m("R2 Ui Ri U R2")
            else:
                self.m("Ri Fi R U R Ui Ri F")
        elif dCorD and norEdgeAny:
            if norEdgeRU:
                self.m("U")
            elif norEdgeBU:
                self.m("U2")
            elif norEdgeLU:
                self.m("Ui")
            self.m("U R Ui Ri F Ri Fi R")
        elif fCorD and flipEdgeAny:
            if flipEdgeBU:
                self.m("U")
            elif flipEdgeLU:
                self.m("U2")
            elif flipEdgeFU:
                self.m("Ui")
            self.m("R Ui Ri U R Ui Ri")
        elif rCorD and norEdgeAny:
            if norEdgeRU:
                self.m("U")
            elif norEdgeBU:
                self.m("U2")
            elif norEdgeLU:
                self.m("Ui")
            self.m("R U Ri Ui F Ri Fi R")
        elif fCorD and norEdgeAny:
            if norEdgeRU:
                self.m("U")
            elif norEdgeBU:
                self.m("U2")
            elif norEdgeLU:
                self.m("Ui")
            self.m("U2 R Ui Ri Fi Ui F")
        elif rCorD and flipEdgeAny:
            if flipEdgeBU:
                self.m("U")
            elif flipEdgeLU:
                self.m("U2")
            elif flipEdgeFU:
                self.m("Ui")
            self.m("R U Ri Ui R U Ri")
        elif uCorU and flipEdgeInsert:
            self.m("R U2 Ri Ui F Ri Fi R")
        elif uCorU and norEdgeInsert:
            self.m("R2 U R2 U R2 U2 R2")
        elif fCorU and norEdgeInsert:
            self.m("Ui R Ui Ri U2 R Ui Ri")
        elif rCorU and norEdgeInsert:
            self.m("Ui R U2 Ri U R U Ri")
        elif fCorU and flipEdgeInsert:
            self.m("U2 R Ui Ri Ui Fi Ui F")
        elif rCorU and flipEdgeInsert:
            self.m("U Fi Ui F Ui R U Ri")
        elif dCorD and flipEdgeInsert:
            self.m("R2 U2 F R2 Fi U2 Ri U Ri")
        elif fCorD and norEdgeInsert:
            self.m("R2 U2 Ri Ui R Ui Ri U2 Ri")
        elif rCorD and norEdgeInsert:
            self.m("R U2 R U Ri U R U2 R2")
        elif fCorD and flipEdgeInsert:
            self.m("F2 Li Ui L U F Ui F")
        elif rCorD and flipEdgeInsert:
            self.m("R Ui Ri Fi Li U2 L F")

    def f2lCorner(self):
        return self.cube.is_f2l_corner_solved()

    def f2lEdge(self):
        return self.cube.is_f2l_edge_solved()

    def f2lCorrect(self):
        return self.f2lCorner() and self.f2lEdge()

    def f2lEdgeOnTop(self):
        return self.cube.is_f2l_edge_on_top()

    def f2lEdgeInserted(self):
        return self.cube.is_f2l_edge_inserted()

    def f2lEdgeInserted2(self, p):
        return self.cube.is_f2l_edge_inserted2(p)

    def f2lCornerInserted(self):
        return self.cube.is_f2l_corner_inserted()

    def f2lFRCor(self):
        return self.cube.is_f2l_FR_corner()

    def f2lFUEdge(self):
        return self.cube.is_f2l_FU_edge()

    def f2lCornerOnTop(self):
        return self.cube.is_f2l_corner_on_top()

    def f2lCornerCheck(self):
        return self.cube.f2l_corner_check()

    def f2lEdgeCheck(self):
        return self.cube.f2l_edge_check()

    def f2lEdgeNoCorner(self):
        topEdgeTop = self.cube.get_top_edge_top()
        topEdgeFront = self.cube.get_top_edge_front()
        rmid = self.cube.get_right_center()
        bmid = self.cube.get_back_center()
        lmid = self.cube.get_left_center()
        fmid = self.cube.get_front_center()
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

    def f2lCornerTopNoEdge(self):
        self.topEdgeTop = self.cube.get_top_edge_top()
        self.topEdgeFront = self.cube.get_top_edge_front()
        self.rmid = self.cube.get_right_center()
        self.bmid = self.cube.get_back_center()
        self.lmid = self.cube.get_left_center()
        self.fmid = self.cube.get_front_center()
        BREdge = (self.topEdgeTop == self.rmid or self.topEdgeTop == self.bmid) and (self.topEdgeFront == self.rmid or self.topEdgeFront == self.bmid)
        BLEdge = (self.topEdgeTop == self.lmid or self.topEdgeTop == self.bmid) and (self.topEdgeFront == self.lmid or self.topEdgeFront == self.bmid)
        FLEdge = (self.topEdgeTop == self.fmid or self.topEdgeTop == self.lmid) and (self.topEdgeFront == self.fmid or self.topEdgeFront == self.lmid)

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

    def f2lCornerTopNoEdge(self):
        self.BackEdgeTop = self.cube.get_back_edge_top()
        self.BackEdgeBack = self.cube.get_back_edge_back()
        self.rmid = self.cube.get_right_center()
        self.bmid = self.cube.get_back_center()
        self.lmid = self.cube.get_left_center()
        self.fmid = self.cube.get_front_center()
        BREdge = (self.BackEdgeTop == self.rmid or self.BackEdgeTop == self.bmid) and (self.BackEdgeBack == self.rmid or self.BackEdgeBack == self.bmid)
        BLEdge = (self.BackEdgeTop == self.lmid or self.BackEdgeTop == self.bmid) and (self.BackEdgeBack == self.lmid or self.BackEdgeBack == self.bmid)
        FLEdge = (self.BackEdgeTop == self.fmid or self.BackEdgeTop == self.lmid) and (self.BackEdgeBack == self.fmid or self.BackEdgeBack == self.lmid)

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

    def f2lEdgeTopNoCorner(self):
        BackEdgeTop = self.cube.get_back_edge_top()
        BackEdgeBack = self.cube.get_back_edge_back()
        rmid = self.cube.get_right_center()
        bmid = self.cube.get_back_center()
        lmid = self.cube.get_left_center()
        fmid = self.cube.get_front_center()
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

    def isf2lDone(self):
        return self.cube.is_f2l_done()

    def f2l(self):
        pairsSolved = 0
        uMoves = 0
        while pairsSolved < 4:
            if not self.f2lCorrect():
                while uMoves < 4:
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
        return self.cube.is_fish()

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
            while self.cube.get_top_corner() != self.cube.get_top_center():
                self.m("U")
            if self.cube.get_front_corner() == self.cube.get_top_center():
                self.antisune()
            elif self.cube.get_back_corner() == self.cube.get_top_center():
                self.m("U2")
                self.sune()
            else:
                raise Exception("Something went wrong")
        else:
            raise Exception("Fish not set up")
        assert self.isTopSolved()

    def getCornerState(self):
        return self.cube.get_corner_state()

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
                    if self.cube.get_front_corner() == self.cube.get_right_center():
                        self.m("R2 B2 R F Ri B2 R Fi R")
                    else:
                        self.m("Ri F Ri B2 R Fi Ri B2 R2")
                    for f in range(index):
                        self.m("Yi")
                    return
                self.m("U")
            self.m("R2 B2 R F Ri B2 R Fi R")

    def permuteEdges(self):
        if all(self.getEdgeState()):
            return
        if self.cube.get_front_edge() == self.cube.get_back_center() and self.cube.get_back_edge() == self.cube.get_front_center():
            self.m("R2 U2 R U2 R2 U2 R2 U2 R U2 R2")
        elif self.cube.get_front_edge() == self.cube.get_right_center() and self.cube.get_right_edge() == self.cube.get_front_center():
            self.m("U Ri Ui R Ui R U R Ui Ri U R U R2 Ui Ri U")
        elif self.cube.get_front_edge() == self.cube.get_left_center() and self.cube.get_left_edge() == self.cube.get_front_center():
            self.m("Ri Ui R Ui R U R Ui Ri U R U R2 Ui Ri U2")
        else:
            uNum = 0
            while True:
                if self.cube.get_back_edge() == self.cube.get_back_center():
                    if self.cube.get_left_edge() == self.cube.get_front_corner():
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
        return self.cube.get_edge_state()

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
        return self.cube.is_solved()

    def isCrossSolved(self):
        return self.cube.is_cross_solved()

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



