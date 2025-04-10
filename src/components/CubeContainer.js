import React, { Component, forwardRef } from 'react';
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
        this.cubeRefs = Array(27).fill().map(() => React.createRef());
        this.domRef = React.createRef();
        
        
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
            touchStarted: false,
            mousePoint: {x: 0, y: 0},
            angleOfRotation: Array(27).fill(0), 
            rotationVector: Array(27).fill().map(() => [1,0,0])
        };
        console.log('Initial positions:', this.state.positions);
        this.onTouchStart = this.onTouchStart.bind(this);
        this.onTouchMove = this.onTouchMove.bind(this);
        this.onTouchEnd = this.onTouchEnd.bind(this);
    }

    resetToDefaultPosition = () => {
        const initialPositions = [
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
            [cubeWidth, cubeWidth, cubeWidth]
        ];
    
        this.setState({
          positions: initialPositions,
          angleOfRotation: Array(27).fill(0),
          rotationVector: Array(27).fill().map(() => [1, 0, 0])
        });
      };

    componentDidMount() {
        if (this.domRef.current) {
            this.domRef.current.addEventListener('mouseup', this.onTouchEnd);
            this.domRef.current.addEventListener('touchend', this.onTouchEnd);
            this.domRef.current.addEventListener('touchcancel', this.onTouchEnd);
            
        }
        
        this.rotateCubeSpace(120, 0);
    }

    componentWillUnmount() {
        this.domRef.current.removeEventListener('mouseup', this.onTouchEnd);
        this.domRef.current.removeEventListener('touchend', this.onTouchEnd);
        this.domRef.current.removeEventListener('touchcancel', this.onTouchEnd);
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
      
        this.state.positions.forEach((position, index) => {
        const cubeRef = this.cubeRefs[index] ? this.cubeRefs[index].current : null;
          if (!Cube) return;
      
          const colors = cubeRef.getFaceColors ? cubeRef.getFaceColors() : {};
          const [x, y, z] = position.map(coord => coord / cubeWidth);
      
          // Direct mapping since we're in default position
          if (z === 1) faceStructure.front[1 - y][x + 1] = colors.front;
          if (z === -1) faceStructure.back[1 - y][1 - x] = colors.back;
          if (x === -1) faceStructure.left[1 - y][z + 1] = colors.left;
          if (x === 1) faceStructure.right[1 - y][1 - z] = colors.right;
          if (y === -1) faceStructure.top[1 - z][x + 1] = colors.top;
          if (y === 1) faceStructure.bottom[z + 1][x + 1] = colors.bottom;
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
        const arr = this.state.positions.map(pos => [...pos]);
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
        console.log('Cube instance rendering');
        return (
            <div ref={this.domRef}
                
                className="cube-container"
                style={{ transform: `scale(${this.getScalingFactor()})` }}
                onMouseDown={this.onTouchStart}
                onTouchStart={this.onTouchStart}
                onMouseMove={this.onTouchMove}
            >
                {this.state.positions.map((val, index) => (
                    <Cube
                        key={index}
                        ref={this.cubeRefs[index]}
                        translate={this.state.positions[index]}
                        orientation={this.getOrientation(index)}
                        onFaceClick={this.handleFaceClick}
                    />
                ))}
                
            </div>

        );
    }
}

export default forwardRef((props, ref) => (
    <CubeContainer {...props} ref={ref} />
  ));
