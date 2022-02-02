import React, { useEffect, useState } from 'react';
import Article from '../components/Article';
import routes from '../api';

function Home() {

  const [posts, setPosts] = useState([]);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    const getPosts = async () => {
      try {
        const response = await fetch(routes.posts.GET);
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
