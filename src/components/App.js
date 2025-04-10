import React, { Component, useRef, useState, useEffect } from 'react';
import CubeContainer from './CubeContainer';
import Button from './Button';

function App() {
  const cubeContainerRef = useRef(null);

  const handleSolveClick = () => {
    if (cubeContainerRef.current) {
      // First reset to default position
      cubeContainerRef.current.resetToDefaultPosition();
      
      // Add slight delay to allow state update
      setTimeout(() => {
        try {
          const cubeState = cubeContainerRef.current.getCubeState();
          console.log('Cube State:', cubeState);
        } catch (error) {
          console.error('Error getting cube state:', error);
        }
      }, 100);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>Rubiks Cube Solver</h1>
        <h2>Logan Aiuppy</h2>
      </header>
      <CubeContainer ref={cubeContainerRef}
      />

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
          onClick={handleSolveClick}
        >
          Solve!
        </button>
      </div>
    </div>
  );
}

export default App;