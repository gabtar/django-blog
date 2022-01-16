import React from 'react';
import './Comment.css';

function Comment(props) {

  return (
    <div className="comment-container">
      <div className="comment-header">
        <div className="comment-user">{props.user}</div>
        <div className="comment-date">Fecha: {props.created_at}</div>
      </div>
      <div className="comment-body">
        {props.body}
      </div>
    </div>
  )

}


export default Comment;
