import React from 'react'
import './App.css';
import { Routes, Route, BrowserRouter } from 'react-router-dom'
import Header from './components/Header'
import Home from './components/pages/Home'


function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
