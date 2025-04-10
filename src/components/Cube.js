import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { getTouchPositions } from '../utilities/utilities';
export const cubeWidth = 50;
export const faceArray = ['front', 'back', 'top', 'bottom', 'left', 'right'];
export const facePosition = {
    left: [-cubeWidth, 0, 0],
    right: [cubeWidth, 0, 0],
    front: [0, 0, cubeWidth],
    back: [0, 0, -cubeWidth],
    top: [0, -cubeWidth, 0],
    bottom: [0, cubeWidth, 0]
};

const colorOrder = ['#B90000', '#0045AD', '#FF5900', '#FFFFFF', '#FFD500', '#009B48'];


class Cube extends Component {

    static propTypes = {
        translate: PropTypes.array.isRequired,
        orientation: PropTypes.array.isRequired,
        onFaceClick: PropTypes.func.isRequired,
        index: PropTypes.number.isRequired,
        faceRotationInit: PropTypes.func.isRequired
    };

    constructor(props) {
        super(props);
        this.disableFaceRotation= false;
        const initialFaceColors = this.initializeColors(props.translate);
        this.state = {
            faceColors: initialFaceColors
        };

        this.onTouchStart = this.onTouchStart.bind(this);
    
    };

    
        
        initializeColors(translate) {
            const colors ={
                front: '',
                back: '',
                left: '',
                right: '',
                top: '',
                bottom: ''
            };

        if (translate) {
            const [x, y, z] = translate;
            colors.front = z === cubeWidth ? '#009B48' : '';
            colors.back = z === -cubeWidth ? '#0045AD' : '';
            colors.left = x === -cubeWidth ? '#B90000' : '';
            colors.right = x === cubeWidth ? '#FF5900' : '';
            colors.top = y === -cubeWidth ? '#FFFFFF' : '';
            colors.bottom = y === cubeWidth ? '#FFD500' : '';
        }

        return colors;
    }

    getFaceColors() {
        // You can return colors from this.state or this.props as needed.
        return this.state.faceColors;
      }


    handleFaceClick = (face, eve) => {
        eve.stopPropagation();
        const currentColor = this.state.faceColors[face];
        const currentIndex = colorOrder.indexOf(currentColor);
        const nextIndex = (currentIndex + 1) % colorOrder.length;
        
        this.setState(prevState => ({
            faceColors: {
                ...prevState.faceColors,
                [face]: colorOrder[nextIndex]
            }
        }));
    };

    
    cubePosition() {
        if (!this.props.translate) return {};
        
        return {
            transform: `translate3d(
                ${this.props.translate[0]}px,
                ${this.props.translate[1]}px,
                ${this.props.translate[2]}px
            ) rotate3d(
                ${this.props.orientation[0]},
                ${this.props.orientation[1]},
                ${this.props.orientation[2]},
                ${this.props.orientation[3]}deg
            )`
        };
    }

    onTouchStart(eve, face,index) {
        if(this.disableFaceRotation)
            return true;
        eve.stopPropagation();
        this.props.faceRotationInit(
            {x: getTouchPositions(eve).clientX, y: getTouchPositions(eve).clientY},
            face
        );
    }

    getFaceColors = () => this.state.faceColors;

    

    render() {
        console.log('Rendering Cube');
        return (
            <div className="cube" style={this.cubePosition()}>
                {faceArray.map((face) => (
                    <div
                        key={face}
                        className={`face ${face}`}
                        style={{ 
                            backgroundColor: this.state.faceColors[face],
                            cursor: 'pointer'
                        }}
                        onClick={(e) => this.handleFaceClick(face, e)}
                        onTouchEnd={(e) => this.handleFaceClick(face, e)}
                    ></div>
                ))}
            </div>
        );
    }
}

export default Cube;