import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

function Header() {

  return (
    <div className="header-container">
      <div className="logo">
        BLOG! &#9968;
      </div>
      <div className="nav-menu">
        <Link to="/" className="nav-link">Home</Link>
        <Link to="/" className="nav-link">Login</Link>
      </div>
    </div>        
  )

}


export default Header;
