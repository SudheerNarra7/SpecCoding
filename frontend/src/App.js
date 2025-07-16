import React, { useState, useEffect } from 'react';
import api from './services/api';
import './App.css';

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchMessage = async () => {
      try {
        const response = await api.get('/');
        setMessage(response.data.message);
      } catch (error) {
        setMessage('Failed to fetch message from backend.');
        console.error(error);
      }
    };

    fetchMessage();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>{message}</h1>
      </header>
    </div>
  );
}

export default App;
