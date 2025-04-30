import React, { useRef, useState } from 'react';
import CubeContainer from './RCube';
import Button from './Button';

function App() {
  const cubeContainerRef = useRef(null);
  const [solutionText, setSolutionText] = useState('');
  const [selectedSolver, setSelectedSolver] = useState('kociemba'); // 'TT' or 'kociemba'
  const [TTSolution, setTTSolution] = useState('');
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
      const res = await fetch('http://localhost:5001/solve2', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(cubeState)
      });

      const result = await res.json();
      setKociembaSolution(result.solution || 'No Kociemba solution found');

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
          className={"controls ${selectedSolver === 'TT' ? 'active' : ''}"}
          onClick={() => {
            setSelectedSolver('TT');
            setSolutionText(TTSolution);
          }}
        >
          Thistlethwaite's
        </Button>

        <Button
          className={"controls ${selectedSolver === 'kociemba' ? 'active' : ''}"}
          onClick={() => {
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
          value={kociembaSolution}
          placeholder="Click and hold to rotate the cube, click each cubie face to change its color. When finished, click Solve! to generate solutions"
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