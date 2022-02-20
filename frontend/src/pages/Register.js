import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../assets/styles.css'
import './Login.css';
import api from '../api';

function Register({setUser}) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const navigate = useNavigate();

  const getToken = async (event) => {

    event.preventDefault();

    try {
      const response = await fetch(api.users.REGISTER, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify({ email: username, password: password })
      });
      const json = await response.json();
      console.log(response.status)

      if (response.status === 201) {
        // Loguear al usuario
        // Display success register
        navigate('/login')
      } else {
        // Error
        console.log("Bad request / cannot create");
      }

    } catch (error) {
      // ej No se puede conectar con el servidor(?)
      console.log(error);
    }
  };


  return (
    <form className='login-form' onSubmit={getToken}>
      <h2>Registrarse</h2>
      <input className='form-control' type='email' placeholder='Username' onChange={(event) => setUsername(event.target.value)} />
      <input className='form-control' type='password' placeholder='Password' onChange={(event) => setPassword(event.target.value)} />
      <input type='submit' className='btn' value='Register' />
    </form>
  );

}

export default Register;
