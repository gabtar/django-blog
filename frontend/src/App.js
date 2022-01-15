import React from 'react'
import './App.css';
import { Routes, Route, BrowserRouter } from 'react-router-dom';
import Header from './components/Header';
import Home from './components/pages/Home';
import PostDetail from './components/pages/PostDetail';
import Login from './components/pages/Login';


function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/post/:id" element={<PostDetail />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
