import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

function Header() {

  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    if (localStorage.getItem('token') !== null) {
      setIsAuthenticated(true);
    }
  }, [isAuthenticated]);

  const logout = () => {
    localStorage.clear();
    setIsAuthenticated(false);
  };

  return (
    <div className="header-container">
      <div className="logo">
        BLOG! &#9968;
      </div>
      <div className="nav-menu">
        <Link to="/" className="nav-link">Home</Link>
        { isAuthenticated ? <span onClick={logout} className='nav-link'>Logout</span> : <Link to="/login" className="nav-link">Login</Link>}
      </div>
    </div>
  )

}

export default Header;
