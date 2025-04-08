import React, { Component } from 'react';
import Cube, { cubeWidth, facePosition } from './Cube';
import {
    calcPosition,
    calculateResultantAngle,
    getCubePositionDiffrence,
    getTouchPositions
} from '../utilities/utilities';


class CubeContainer extends Component {

    constructor(props) {
        super(props);
        
        this.state = {
            positions: [
                [0, 0, 0],
                [-cubeWidth, 0, 0],
                [cubeWidth, 0, 0],
                [0, -cubeWidth, 0],
                [0, cubeWidth, 0],
                [-cubeWidth, -cubeWidth, 0],
                [-cubeWidth, cubeWidth, 0],
                [cubeWidth, -cubeWidth, 0],
                [cubeWidth, cubeWidth, 0],

                [0, 0, -cubeWidth],
                [-cubeWidth, 0, -cubeWidth],
                [cubeWidth, 0, -cubeWidth],
                [0, -cubeWidth, -cubeWidth],
                [0, cubeWidth, -cubeWidth],
                [-cubeWidth, -cubeWidth, -cubeWidth],
                [-cubeWidth, cubeWidth, -cubeWidth],
                [cubeWidth, -cubeWidth, -cubeWidth],
                [cubeWidth, cubeWidth, -cubeWidth],

                [0, 0, cubeWidth],
                [-cubeWidth, 0, cubeWidth],
                [cubeWidth, 0, cubeWidth],
                [0, -cubeWidth, cubeWidth],
                [0, cubeWidth, cubeWidth],
                [-cubeWidth, -cubeWidth, cubeWidth],
                [-cubeWidth, cubeWidth, cubeWidth],
                [cubeWidth, -cubeWidth, cubeWidth],
                [cubeWidth, cubeWidth, cubeWidth],
            ],
            angleOfRotation: Array(27).fill(0), 
            rotationVector: Array(27).fill([1, 0, 0]),
        };
        this.onTouchStart = this.onTouchStart.bind(this);
        this.onTouchMove = this.onTouchMove.bind(this);
        this.onTouchEnd = this.onTouchEnd.bind(this);
    }

    componentDidMount() {
        this.elem.addEventListener('mouseup', this.onTouchEnd);
        this.elem.addEventListener('touchend', this.onTouchEnd);
        this.elem.addEventListener('touchcancel', this.onTouchEnd);
        this.rotateCubeSpace(120, 0);
    }

    componentWillUnmount() {
        this.elem.removeEventListener('mouseup', this.onTouchEnd);
        this.elem.removeEventListener('touchend', this.onTouchEnd);
        this.elem.removeEventListener('touchcancel', this.onTouchEnd);
    }

    getOrientation(index) {
        return [
            this.state.rotationVector[index][0],
            this.state.rotationVector[index][1],
            this.state.rotationVector[index][2],
            this.state.angleOfRotation[index]
        ];
    }

    getCubeState = () => {
        const faceStructure = {
            front: Array(3).fill().map(() => Array(3).fill('')),
            back: Array(3).fill().map(() => Array(3).fill('')),
            left: Array(3).fill().map(() => Array(3).fill('')),
            right: Array(3).fill().map(() => Array(3).fill('')),
            top: Array(3).fill().map(() => Array(3).fill('')),
            bottom: Array(3).fill().map(() => Array(3).fill(''))
        };

        this.cubeRefs.forEach((ref, index) => {
            const cube = ref.current;
            if (!cube) return;

            const position = this.state.positions[index];
            const colors = cube.getFaceColors();

            // Map cube position to face coordinates
            const x = position[0]/cubeWidth + 1;
            const y = position[1]/cubeWidth + 1;
            const z = position[2]/cubeWidth + 1;

            // Front face (z = 1)
            if (position[2] === cubeWidth) {
                faceStructure.front[y][x] = colors.front;
            }
            // Back face (z = -1)
            if (position[2] === -cubeWidth) {
                faceStructure.back[y][x] = colors.back;
            }
            // Left face (x = -1)
            if (position[0] === -cubeWidth) {
                faceStructure.left[y][z] = colors.left;
            }
            // Right face (x = 1)
            if (position[0] === cubeWidth) {
                faceStructure.right[y][z] = colors.right;
            }
            // Top face (y = -1)
            if (position[1] === -cubeWidth) {
                faceStructure.top[z][x] = colors.top;
            }
            // Bottom face (y = 1)
            if (position[1] === cubeWidth) {
                faceStructure.bottom[z][x] = colors.bottom;
            }
        });

        return faceStructure;
    };

    onTouchStart(eve) {
        eve.preventDefault();
        this.setState({
            touchStarted: true,
            mousePoint: { 
                x: getTouchPositions(eve).clientX, 
                y: getTouchPositions(eve).clientY 
            }
        });
    }

    rotateCubeSpace(diffX, diffY) {
        const arr = this.state.positions.slice();
        const angleOfRotationArr = [];
        const rotationVectorArr = [];

        for (let i = 0; i < arr.length; i++) {
            arr[i] = Math.abs(diffY) > Math.abs(diffX) ?
                calcPosition(this.state.positions[i], [1, 0, 0], -diffY) :
                calcPosition(this.state.positions[i], [0, 1, 0], diffX);

            const rotationResult = Math.abs(diffY) > Math.abs(diffX) ?
                calculateResultantAngle(-diffY, [1, 0, 0], 
                this.state.rotationVector[i], this.state.angleOfRotation[i]) :
                calculateResultantAngle(diffX, [0, 1, 0], 
                this.state.rotationVector[i], this.state.angleOfRotation[i]);

            angleOfRotationArr[i] = rotationResult.gama;
            rotationVectorArr[i] = rotationResult.rotationVector;
        }

        this.setState({
            positions: arr,
            angleOfRotation: angleOfRotationArr,
            rotationVector: rotationVectorArr
        });
    }

    onTouchMove(eve) {
        if (!this.state.touchStarted) return;

        const { clientX, clientY } = getTouchPositions(eve);
        const diffY = clientY - this.state.mousePoint.y;
        const diffX = clientX - this.state.mousePoint.x;

        this.setState({ 
            mousePoint: { x: clientX, y: clientY } 
        }, () => {
            this.rotateCubeSpace(diffX, diffY);
        });
    }

    onTouchEnd() {
        this.setState({ 
            touchStarted: false, 
            mousePoint: { x: 0, y: 0 } 
        });
    }

    

    getScalingFactor() {
        const minSize = Math.min(window.innerHeight, window.innerWidth);
        return Math.min(Math.max(minSize/300, 1), 1.5);
    }

    render() {
        return (
            <div ref={elem => this.elem = elem}
                
                className="cube-container"
                style={{ transform: `scale(${this.getScalingFactor()})` }}
                onMouseDown={this.onTouchStart}
                onTouchStart={this.onTouchStart}
                onMouseMove={this.onTouchMove}
                onTouchMove={this.onTouchMove}
            >
                {this.state.positions.map((val, index) => (
                    <Cube
                        key={index}
                        translate={this.state.positions[index]}
                        orientation={this.getOrientation(index)}
                    />
                ))}
                
            </div>

        );
    }
}

export default CubeContainer;