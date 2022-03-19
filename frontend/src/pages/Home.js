import React, { useEffect, useState } from 'react';
import Article from '../components/Article';
import routes from '../api';

function Home() {

  const [posts, setPosts] = useState([]);
  const [loaded, setLoaded] = useState(false);

  const [previousPage, setPreviousPage] = useState(null)
  const [nextPage, setNextPage] = useState(null)

  const getPosts = async (url) => {
      try {
        const apiRoute = url === undefined ? routes.posts.GET : url

        const response = await fetch(apiRoute);
        const json = await response.json();
        setLoaded(true);
        setPosts(json.results);

        setPreviousPage(json.previous);
        setNextPage(json.next);

      } catch (error) {
        console.log("error", error);
      }
    };

  useEffect(() => {
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
      <button className='btn' disabled={ previousPage === null } onClick={() => {
        getPosts(previousPage)
      }}>
        {'<< Anterior'}
      </button>
      <button className='btn' disabled={ nextPage === null } onClick={() => {
        getPosts(nextPage)
      }}>
        {'Siguiente >>'}
      </button>
    </>
  )
}


export default Home;
