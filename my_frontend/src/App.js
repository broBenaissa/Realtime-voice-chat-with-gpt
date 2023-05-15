import React, { useState, useEffect } from "react";
import axios from 'axios';
import audio from  './audio.json';

function App() {
  const [result, setResult] = useState([]);

  audio.map(audio => {
    return(
      <div>
        {audio.text}
      </div>
    )
  })
    
   //.then(response => console.log(response.data))
  
  useEffect(() => {
    axios.get('http://localhost:5000')
      .then(response => response.json())
      .then(data => {
        setResult(data);
      })
      .catch(error => {
        console.log(error);
      });
  }, []);
//
  return (
    <div>
      <p>{result}</p>
      <p>Salam alaykom</p>
    </div>
  );
}

export default App;
