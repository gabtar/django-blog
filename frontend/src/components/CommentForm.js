import React, { useState } from 'react'
import '../assets/styles.css'
import routes from '../api'

function CommentForm({user, postId}) {

  const [newComment, setNewComment] = useState('')

  const postComment = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch(routes.comments.POST, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization' : `Token ${user.token}`
        },
        method: 'POST',
        body: JSON.stringify({ related_post: postId, user: user.id, comment: newComment })
      });
      const json = await response.json();

      console.log(json);

    } catch(error) {
      console.log(error);
    }
  }

  return(
    <form onSubmit={postComment} className="form-container">
      <textarea className="form-control" placeholder="Ingrese su comentario" onChange={(event) => setNewComment(event.target.value)} />
      <input type="submit" className="btn" value="Enviar comentario" />
    </form>
  )
}


export default CommentForm;
