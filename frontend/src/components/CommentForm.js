import React, { useState } from 'react'
import './CommentForm.css'
import routes from '../api'

function CommentForm() {

  const [newComment, setNewComment] = useState('')

  const postComment = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch(routes.comments.POST, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization' : `Token ${localStorage.getItem('token')}`
        },
        method: 'POST',
        body: JSON.stringify({ related_post: 1, user: 1, comment: newComment })
      });
      const json = await response.json();

      console.log(json);

    } catch(error) {
      console.log(error);
    }
  }

  return(
    <form onSubmit={postComment}>
      <textarea placeholder="Ingrese su comentario" onChange={(event) => setNewComment(event.target.value)} />
      <input type="submit" value="Enviar comentario" />
    </form>
  )
}


export default CommentForm;

