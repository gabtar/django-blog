import React, { useEffect, useState } from 'react';
import Article from '../components/Article';

function Home() {

  const [posts, setPosts] = useState([]);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    const url = "http://localhost:8000/api/v1/posts/";

    const getPosts = async () => {
      try {
        const response = await fetch(url);
        const json = await response.json();
        setLoaded(true);
        setPosts(json);
      } catch (error) {
        console.log("error", error);
      }
    };

    getPosts();
  }, []);

  const articles = posts.map((post) =>
    <Article key={post.id}
      id={post.id}
      title={post.title}
      author={post.author}
      body={post.body}
      created={post.created_at}
    />
  );

  return (
    <>
      <h1>Últimos posts</h1>
      {loaded ? articles : <p>No se pudieron cargar los posts</p>}
    </>
  )
}


export default Home;
