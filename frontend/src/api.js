// Django blog api endpoints
const routes = {
  users: {
    LOGIN_URL: "http://localhost:8000/api/v1/users/auth/",
    REGISTER: "http://localhost:8000/api/v1/users/create/",
  },
  posts: {
    GET: "http://localhost:8000/api/v1/posts/",
    POST: "http://localhost:8000/api/v1/posts/" ,// Url iguales pero deben usuarse con distintos metodos
    PATCH: "http://localhost:8000/api/v1/posts/" // Url iguales pero deben usuarse con distintos metodos
  },
  comments: {
    GET: "http://localhost:8000/api/v1/comments/",
    POST: "http://localhost:8000/api/v1/comments/",
    PATCH: "http://localhost:8000/api/v1/comments/",
  }
}

export default routes
