import React, { Component } from 'react';
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
        translate: React.PropTypes.array,
        orientation: React.PropTypes.array,
        onFaceClick: React.PropTypes.func,
        index: React.PropTypes.number
    };

    constructor(props) {
        super(props);
        let faceColors = {
            front: '',
            back: '',
            left: '',
            right: '',
            top: '',
            bottom: ''
        };

        this.onTouchStart = this.onTouchStart.bind(this);
        
        faceColors.top = this.props.translate[1] === -cubeWidth ? '#FFFFFF' : '';
        faceColors.bottom = this.props.translate[1] === cubeWidth ? '#FFD500' : '';
        faceColors.left = this.props.translate[0] === -cubeWidth ? '#B90000' : '';
        faceColors.right = this.props.translate[0] === cubeWidth ? '#FF5900' : '';
        faceColors.front = this.props.translate[2] === cubeWidth ? '#009B48' : '';
        faceColors.back = this.props.translate[2] === -cubeWidth ? '#0045AD' : '';

        this.state = {faceColors};

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

    getFaceColors = () => {
        
        return this.state.faceColors;
    };

    

    render() {
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