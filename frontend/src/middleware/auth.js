// Simple authentication

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'

export function useAuth() {

  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const navigate = useNavigate();

  const LOGIN_URL = 'http://localhost:8000/api/v1/users/auth/';

  return {
    isAuthenticated,
    login(username, password) {
      return async () => {
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
            this.setIsAuthenticated(true);
            console.log(isAuthenticated);
            navigate('/');
          } else {
            // Bad request
            console.log(json);
          }
        } catch (error) {
          console.log(error);
        }
      }
    },
    logout() {
      return new Promise((res) => {
        setIsAuthenticated(false);
        localStorage.clear();
        res();
      });
    }
  };

}
