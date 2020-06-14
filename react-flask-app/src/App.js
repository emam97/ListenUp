import React, { useState, useEffect } from 'react';
import DonutChart from './components/DonutChart';
import StackedBarChart from './components/StackedBarChart'
import data from './dummy_data.json';
import './App.css';

function App() {
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <p>
          ListenUp!
        </p>
      </header>
      <div className="chart-container">
          <h3>Chart of Entities</h3>
          <DonutChart
            data = {data.entities}
          />
      </div>
      <div className="chart-container">
          <h3>Chart of Keywords</h3>
          <StackedBarChart
            data = {data.keywords}
          />
      </div>
      <p>The current time is {currentTime}.</p>
    </div>
  );
}

export default App;
