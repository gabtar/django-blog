import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';


function PostDetail() {

  const { id } = useParams();

  const [post, setPost] = useState('Not loaded');

  // Load whole post
  useEffect( () => {
    const url = `http://localhost:8000/api/v1/posts/${id}/`

    const getPosts = async () => {
      try {
        const response = await fetch(url);
        const json = await response.json();
        setPost(json);
      } catch (error) {
        console.log("error", error);
      }
    };

    getPosts();
  }, [id]);

  return (
    <>
    <h1>{post.title}</h1>
    <p>Fecha: {post.created_at}</p>
    <p>{post.body}</p>
    <h2>Comentarios</h2>
    </>
  );

}

export default PostDetail;

