import React from 'react';
import './Article.css';

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
    </article>
  )
}

export default Article;
