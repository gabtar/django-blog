import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import routes from '../api'
import '../assets/styles.css'


function NewPost({user}) {

  // Para usar el mismo componente si es para editar o crear el post
  const location = useLocation();
  const postToEdit = location.hasOwnProperty('state') ? location.state : null;

  const navigate = useNavigate();

  const [newPost, setNewPost] = useState({
    title: postToEdit ? postToEdit.title : '',
      body: postToEdit ? postToEdit.body : '',
  })

  const url = postToEdit ? `${routes.posts.PATCH}${postToEdit.postId}/` : routes.posts.POST;

  const createPost = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch(url, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization' : `Token ${user.token}`
        },
        method: postToEdit ? 'PATCH' : 'POST',
        body: JSON.stringify({ author: user.id, ...newPost })
      });
      const json = await response.json();

      if (response.status === 201 || response.status === 200) {
        navigate('/');
      }

    } catch(error) {
      console.log(error);
    }
  }

  return (
    <form onSubmit={createPost} className="form-container">
     <h1>Nuevo post</h1>
     <input 
      type="text"
      className="form-control"
      value={newPost.title}
      placeholder='Título'
      onChange={(event) => setNewPost({...newPost, 'title' : event.target.value })}
     />
     <textarea 
      className="form-control"
      placeholder="Escribir nuevo post..."
      style={{ height: 300 }}
      onChange={(event) => setNewPost({...newPost, 'body' : event.target.value })} 
      defaultValue={newPost.body}
     />
     <input type="submit" className="btn" value={postToEdit ? 'Editar Post' : 'Crear Post'} />
    </form>
  )
}

export default NewPost;
