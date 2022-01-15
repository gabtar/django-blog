import React, { useState } from 'react';
import './Login.css';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const LOGIN_URL = "http://localhost:8000/api/v1/users/auth/";

  const getToken = async (event) => {

    event.preventDefault();

    try {
      const response = await fetch(LOGIN_URL, {
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
        console.log(json);
        window.location.replace('/');
      } else {
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
