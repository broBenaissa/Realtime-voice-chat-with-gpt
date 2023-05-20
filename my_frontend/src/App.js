import React, { useState, useEffect } from "react";
import axios from 'axios';
//import audio from '../src/audio.json';
import server from './backend/server.py'

function App() {
  const [result, setResult] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000')
      .then(response => response.data)
      .then(data => {
        setResult(data);
        //console.log(data);
      })
      .catch(error => {
        console.log(error);
      });
  }, []);

  return (
    <div>
      <p>{result["result"]}</p>
    </div>
  );
}

export default App;
