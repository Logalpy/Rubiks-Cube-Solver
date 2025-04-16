import kociemba
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={
    r"/solve1": {"origins": "http://localhost:3000"},
    r"/solve2": {"origins": "http://localhost:3000"}
})

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

def is_cube_solved(cube_data):
    """Check if the cube is already solved by verifying each face has uniform colors"""
    for face_name in face_order:
        face = cube_data[face_name]
        # Get the center color which should be the correct color for this face
        center_color = face[1][1]
        # Check if all stickers match the center
        if not all(all(square == center_color for square in row) for row in face):
            return False
    return True

@app.route('/solve2', methods=['POST'])
def solve_cube():
    translation_dict = {'G': 'F', 'W': 'U', 'Y': 'D', 'O': 'L'}
    try:
        cube_data = request.json
        
        # Check if cube is already solved
        if is_cube_solved(cube_data):
            return jsonify({'status': 'success', 'solution': 'Already Solved'})
            
        solver = ''.join(create_cube(face, cube_data[face])
                         for face in face_order)
        translation_table = str.maketrans(translation_dict)
        translated_solver = solver.translate(translation_table)
        ans = kociemba.solve(translated_solver)
        response2 = jsonify({'status': 'success', 'solution': ans})
        response2.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        return response2
    except Exception as e:
        print("Error:", str(e))
        response2 = jsonify({'status': 'error', 'message': str(e)})
        response2.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        return response2, 400
    
@app.route('/solve2', methods=['OPTIONS'])
def solve_cube_options():
    response = jsonify()
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response
    
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5001, debug = True)