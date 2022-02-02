import React  from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

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
        <Link to="/" className="nav-link">Home</Link>
        { user.isAuthenticated ? <span onClick={logout} className='nav-link'>Logout</span> : <Link to="/login" className="nav-link">Login</Link>}
      </div>
    </div>
  )

}

export default Header;
