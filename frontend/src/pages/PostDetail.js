import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import Comment from '../components/Comment';
import CommentForm from '../components/CommentForm';
import routes from '../api'


function PostDetail({user}) {

  const { id } = useParams();

  const [post, setPost] = useState('Not loaded');
  const [comments, setComments] = useState([]);

  // Load data
  useEffect( () => {
    const urlPost = routes.posts.GET+`${id}/`
    const urlComments = routes.comments.GET+`${id}/`

    const getPosts = async (url, set) => {
      try {
        const response = await fetch(url);
        const json = await response.json();
        set(json);
      } catch (error) {
        console.log("error", error);
      }
    };

 
    getPosts(urlPost, setPost);
    getPosts(urlComments, setComments);

  }, [id]);

  const comments_view = comments.map( (comment) => 
    <Comment key={comment.id}
      id={comment.id}
      username={comment.mail}
      editable={user.username === comment.mail}
      body={comment.comment}
      created_at={comment.created_at}
      comments={comments}
      setComments={setComments}
      user={user}
    />
  )
  
  return (
    <>
      <h1>{post.title}</h1>
      { user.isAuthor ? <Link to='/admin/newpost' state={{ title: post.title, body: post.body, postId: post.id }}>Editar Post</Link> : '' }
      <p>Fecha: {post.created_at}</p>
      <p>{post.body}</p>
      {user.isAuthenticated ? <CommentForm user={user} postId={post.id} setComments={setComments} comments={comments} /> : 'Ingrese para publicar un comentario'}
      <h2>Comentarios</h2>
      {comments.length > 0 ? comments_view : 'Publicá el primer comentario'}
    </>
  );

}

export default PostDetail;

