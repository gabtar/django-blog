import React, { useState, useEffect } from 'react'
import { Routes, Route, BrowserRouter } from 'react-router-dom';
import './App.css';

// Componentes
import Header from './components/Header';
import Home from './pages/Home';
import PostDetail from './pages/PostDetail';
import Login from './pages/Login';
import Register from './pages/Register';
import Admin from './pages/Admin';
import NewPost from './pages/NewPost';


function App() {
  
  const [user, setUser] = useState({
    username: '',
    isAuthenticated: false,
    isBlogAuthor: false,
    token: '',
  });

  useEffect(() => {
    let session = localStorage.getItem('userCredentials')
    if (session !== null) {
      setUser(JSON.parse(session));
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
          <Route path="/register" element={<Register setUser={setUser}/>} />
          <Route path="/admin" element={<Admin/>} />
          <Route path="/admin/newpost" element={<NewPost user={user}/>} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
