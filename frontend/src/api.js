import axios from 'axios'

const api = axios.create({
  // Como estamos usando o Proxy do Vite, não coloque http://localhost:5000 aqui.
  // Deixe vazio ou apenas '/' para ele usar o mesmo domínio do frontend.
  baseURL: 'http://localhost:5000',
  withCredentials: true
})

export default api
