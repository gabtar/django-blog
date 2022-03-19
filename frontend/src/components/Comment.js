import React, { useEffect, useState } from 'react';
import Modal from './Modal';
import './Comment.css';
import routes from '../api'

function Comment(props) {

  const urlEditComment = routes.comments.PATCH+`${props.id}/`

  const [showEditModal, setShowEditModal] = useState(false)
  const [newCommentValue, setNewCommentValue ] = useState(props.body)

  const editComment = async (event) => {
    event.preventDefault();

    try {
      const response = await fetch(urlEditComment, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization' : `Token ${props.user.token}`
        },
        method: 'PATCH',
        body: JSON.stringify({ comment: newCommentValue })
      });

      const json = await response.json();
      console.log(json);
      props.setComments([json, ...props.comments.filter( (comment) => comment.id != props.id )])
      setShowEditModal(false);
    } catch (error) {
      console.log("error", error);
    }
  };

  return (
    <div className="comment-container">
      <div className="comment-header">
        <div className="comment-user">
          {props.username}
          {props.editable ? 
            <button className='btn' onClick={() => setShowEditModal(true)}>Editar</button> : ''}
            <Modal show={showEditModal} setShow={setShowEditModal} >
              <h2>Editar el comentario</h2>
              <form className="form-container">
                <textarea className="form-control" 
                placeholder="Edite su comentario" 
                value={newCommentValue} 
                onChange={(event) => setNewCommentValue(event.target.value)}
                />
                <input type="submit" className="btn" value="Modificar" onClick={editComment} />
              </form>
            </Modal>
        </div>
        <div className="comment-date">Fecha: {props.created_at}</div>
      </div>
      <div className="comment-body">
        {props.body}
      </div>
    </div>
  )

}


export default Comment;
