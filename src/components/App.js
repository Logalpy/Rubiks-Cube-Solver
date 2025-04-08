import React, { Component } from 'react';
import CubeContainer from './CubeContainer';
import Button from './Button';

class App extends Component {
  

  
    render() {
        return (
          <div className="app">
            <header className="header">
              <h1>Rubiks Cube Solver</h1>
              <h2>Logan Aiuppy</h2>
            </header>
            <CubeContainer ref={this.cubeContainerRef}/>

            
            
            {/* Control buttons */}
            <div className="button-container">
              <Button className="controls">
                Back
              </Button>
              
              <Button className="controls">
                Next
              </Button>

              <button 
                className="solver"
                onClick={this.handleSolveClick}
            >
                Solve!
            </button>
              
            </div>
            
                
            
          </div>
        );
      }
  };
  

export default App;