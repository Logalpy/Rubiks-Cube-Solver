import kociemba
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])


def create_cube(face_name, face_data):
    if face_name == 'top':
        # Read rows left-right, top-bottom
        return ''.join(''.join(row) for row in face_data)
    
    elif face_name == 'right':
        # Read columns top-bottom, right-left
        return ''.join(face_data[row][col] 
                    for col in range(3)
                    for row in reversed(range(3)))
                      
    
    elif face_name == 'front':
        # Read rows left-right, top-bottom
        return ''.join(''.join(row) for row in face_data)
    
    elif face_name == 'bottom':
        # Read rows left-right, bottom-top
        return ''.join(face_data[row][col]
                       for row in range(3)
                       for col in range(3))
    
    elif face_name == 'left':
        # Read columns top-bottom, left-right
        return ''.join(face_data[row][col] 
                    for col in reversed(range(3))
                    for row in range(3)
                      )
    
    elif face_name == 'back':
        # Read rows right-left, bottom-top
        return ''.join(''.join(reversed(row)) 
                      for row in reversed(face_data))
    
    else:
        raise ValueError(f"Unknown face: {face_name}")
    
face_order = ['top', 'right', 'front', 'bottom', 'left', 'back']


def solve_cube(cube_data):
    translation_dict = {'G': 'F', 'W': 'U', 'Y': 'D', 'O': 'L'}
    solver = ''.join(create_cube(face, cube_data[face])
                        for face in face_order)
    translation_table = str.maketrans(translation_dict)
    translated_solver = solver.translate(translation_table)
    print(kociemba.solve(translated_solver))


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

solve_cube(cube_data)