import React, { useState, useEffect } from 'react'
import './App.css';
import { Routes, Route, BrowserRouter } from 'react-router-dom';
import Header from './components/Header';
import Home from './pages/Home';
import PostDetail from './pages/PostDetail';
import Login from './pages/Login';


function App() {
  
  const [user, setUser] = useState({
    username: '',
    isAuthenticated: false,
    userId: '',
  });

  useEffect(() => {
    if (localStorage.getItem('token') !== null) {
      setUser({
        username: '',
        isAuthenticated: true,
        userId: ''
      });
    }

  }, []);

  return (
    <div className="App">
      <BrowserRouter>
        <Header user={user} setUser={setUser}/>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/post/:id" element={<PostDetail user={user}/>} />
          <Route path="/login" element={<Login setUser={setUser}/>} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
