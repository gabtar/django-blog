import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';
import api from '../api';

function Login({setUser}) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const navigate = useNavigate();

  const getToken = async (event) => {

    event.preventDefault();

    try {
      const response = await fetch(api.users.LOGIN_URL, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify({ username: username, password: password })
      });
      const json = await response.json();

      if ("token" in json) {
        localStorage.clear();
        localStorage.setItem('token', json.token)
        // Login success
        setUser({
          username: json.token,
          isAuthenticated: true,
          userId: 1
        });
        navigate(-1);
      } else {
        // TODO Popup o algo parecido?
        // Bad request
        console.log(json);
      }
    } catch (error) {
      // ej No se puede conectar con el servidor(?)
      console.log(error);
    }
  };


  return (
    <form className="form-container" onSubmit={getToken}>
      <input className='form-input' type='email' placeholder='Username' onChange={(event) => setUsername(event.target.value)} />
      <input className='form-input' type='password' placeholder='Password' onChange={(event) => setPassword(event.target.value)} />
      <input type='submit' value='Login' />
    </form>
  );

}

export default Login;
