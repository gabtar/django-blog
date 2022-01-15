import React from 'react';
import './Article.css';
import { Link } from 'react-router-dom';

function Article(props) {
  return (
    <article>
      <div className="article-title-wrapper">
        <div className="article-title">
          {props.title}
        </div>
        <div className="article-title-date">
          Fecha: {props.created}
        </div>
      </div>
      <div className="article-content">
        {props.body}
      </div>
      <Link to={`post/${props.id}`} className='link'>Ver más...</Link>
    </article>
  )
}

export default Article;
