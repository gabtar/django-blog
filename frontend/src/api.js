// Django blog api endpoints
const routes = {
  users: {
    LOGIN_URL: "http://localhost:8000/api/v1/users/auth/",
  },
  posts: {
    GET: "http://localhost:8000/api/v1/posts/",
  },
  comments: {
    GET: "http://localhost:8000/api/v1/comments/",
    POST: "http://localhost:8000/api/v1/comments/",
  }
}

export default routes
