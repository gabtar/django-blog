import React  from 'react';
import { Link } from 'react-router-dom';
import './Header.css';
import '../assets/styles.css'

function Header({ user, setUser }) {

  const logout = () => {
    localStorage.clear();
    setUser({
      username: '',
      isAuthenticated: false,
      userId: ''
    });
  };

  return (
    <div className="header-container">
      <div className="logo">
        BLOG! &#9968;
      </div>
      <div className="nav-menu">
        { user.isAuthenticated ? <span className="logged-in">{ user.username }</span> : '' }
        <Link to="/" className="btn">Home</Link>
        { user.isAuthor ? <Link to="/admin" className="btn">Admin</Link> : '' } 
        { user.isAuthenticated ? <span onClick={logout} className='btn'>Logout</span> :
            <span>
            <Link to="/login" className="btn">Login</Link>
            <Link to="/register" className="btn">Register</Link>
            </span>}
      </div>
    </div>
  )

}

export default Header;
