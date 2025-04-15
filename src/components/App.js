import React, { Component, useRef, useState, useEffect } from 'react';
import CubeContainer from './CubeContainer';
import Button from './Button';

function App() {
  const cubeContainerRef = useRef(null);
  const [solutionText, setSolutionText] = useState('');
  const [selectedSolver, setSelectedSolver] = useState('kociemba'); // 'cfop' or 'kociemba'
  const [cfopSolution, setCfopSolution] = useState('');
  const [kociembaSolution, setKociembaSolution] = useState('');


  const handleSolveClick = async () => {
    if (!cubeContainerRef.current) return;
  
    try {
      // Reset to default position
      cubeContainerRef.current.resetToDefaultPosition();
      
      // Wait for state update and cube reset
      await new Promise(resolve => setTimeout(resolve, 100));
      
      // Get updated cube state
      const cubeState = cubeContainerRef.current.getCubeState();
      console.log('Cube State:', cubeState);
  
      // Send to backend
      const [res1, res2] = await Promise.all([
        fetch('http://localhost:5000/solve1', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(cubeState)
        }),
        fetch('http://localhost:5001/solve2', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(cubeState)
        })
      ]);

      const result1 = await res1.json();
      const result2 = await res2.json();
  
      setCfopSolution(result1.solution || 'No CFOP Solution found')
      setKociembaSolution(result2.solution || 'No Kociemba solution found');
  
    } catch (error) {
      console.error('Operation Failed:', error.message);
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
      <Button 
        className={"controls ${selectedSolver === 'cfop' ? 'active' : ''}"}
        onClick={() =>{
          setSelectedSolver('cfop');
          setSolutionText(cfopSolution);
        }}
        >
          CFOP
        </Button>
        
        <Button 
        className={"controls ${selectedSolver === 'kociemba' ? 'active' : ''}"}
        onClick={() =>{
          setSelectedSolver('kociemba');
          setSolutionText(kociembaSolution);
        }}
        >
          Kociemba
        </Button>

        <button 
          className="solver"
          onClick={handleSolveClick}
        >
          Solve!
        </button>
      </div>
      <div className="solution-box">
        <textarea
          readOnly
          value={solutionText}
          placeholder="Click Solve! to generate solutions"
          rows="4"
        />
        <button 
          className="copy-btn"
          onClick={() => navigator.clipboard.writeText(solutionText)}
        >
          Copy
        </button>
      </div>
    </div>
  );
};

export default App;