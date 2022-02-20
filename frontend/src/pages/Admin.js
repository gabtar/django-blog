import React from 'react';
import { Link } from 'react-router-dom';

function Admin() {
  return (
    <>
      <h1>Admin Page</h1>
      <Link to='/admin/newpost'>Escribir un nuevo post</Link>
    </>
  )
}

export default Admin;
