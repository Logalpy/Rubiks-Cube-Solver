from tkinter import *

class CFOPSolver:
    def __init__(self, cube_data):
        self.moves = []
        self.solution_length = 0


    def create_cube(self, cube_data):
        return [[[cell.upper() for cell in row] for row in cube_data['top']],  # Up/white

                [[cell.upper() for cell in row] for row in cube_data['front']],  # front/green

                [[cell.upper() for cell in row] for row in cube_data['right']],  # right/red

                [[cell.upper() for cell in row] for row in cube_data['left']],  # left/orange

                [[cell.upper() for cell in row] for row in cube_data['bottom']],  # down/yellow

                [[cell.upper() for cell in row] for row in cube_data['back']]]  # back/blue
    

    def get_moves(self):
        self.simplify_moves()
        s = ""
        for i in self.moves:
            s += str(i) + " "
        # makes for easier reading
        s = str.replace(s, "i", "'")[:-1]
        return s
    
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

    def transformY(self, move):
        if move[0] in ["U", "D"]:
            return move
        if move[0] == "F":
            return "R" + move[1:]
        if move[0] == "B":
            return "L" + move[1:]
        if move[0] == "L":
            return "F" + move[1:]
        raise Exception("Transform Error: " + move)
    
    def simplifyMoves(self):
        # Remove redundant moves
        simplified_moves = []
        for move in self.moves:
            if simplified_moves and simplified_moves[-1] == move:
                simplified_moves.pop()
            else:
                simplified_moves.append(move)
        self.moves = simplified_moves
        
        # Remove unnecessary rotations
        self.moves = [move for move in self.moves if not (move[0] == 'U' and move[1] == 'i')]
        
        # Remove unnecessary Y rotations
        self.moves = [self.transformY(move) for move in self.moves]
        
        # Remove unnecessary rotations again after Y transformation
        simplified_moves = []
        for move in self.moves:
            if simplified_moves and simplified_moves[-1] == move:
                simplified_moves.pop()
            else:
                simplified_moves.append(move)
        self.moves = simplified_moves

    