<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h2>Bem-vindo</h2>
        <p>Insira suas credenciais para acessar</p>
      </div>

      <form @submit.prevent="submit">
        <div class="form-group">
          <label for="login">Usuário</label>
          <input
            id="login"
            v-model="login"
            type="text"
            placeholder="Ex: admin"
            required
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label for="senha">Senha</label>
          <input
            id="senha"
            type="password"
            v-model="senha"
            placeholder="••••••"
            required
            :disabled="loading"
          />
        </div>

        <button type="submit" :disabled="loading" class="btn-submit">
          {{ loading ? 'Autenticando...' : 'Acessar Sistema' }}
        </button>

        <div v-if="error" class="error-msg">
          {{ error }}
        </div>
      </form>

      <div class="login-footer">
        <p>Projeto COM759 &copy; 2025</p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/api'

export default {
  data () {
    return {
      login: '',
      senha: '',
      error: ''
    }
  },
  methods: {
    async submit () {
      this.error = ''
      try {
        // GAMBIARRA 1: Transformar JSON em formato de Formulário
        // O backend espera application/x-www-form-urlencoded
        const params = new URLSearchParams()
        params.append('login', this.login)
        params.append('senha', this.senha)

        // Envia para o backend
        const res = await api.post('/login', params)

        // GAMBIARRA 2: Checar se o login falhou via URL
        // O backend redireciona para /login se der erro, ou /index se der certo.
        // O axios segue o redirecionamento e nos devolve a URL final.
        if (res.request.responseURL && res.request.responseURL.includes('login')) {
          this.error = 'Login ou senha inválidos'
          return
        }

        // GAMBIARRA 3: Simular os dados do usuário (já que não temos rota /me)
        // Se o login for 'admin', damos permissão de admin.
        const nivelAuth = this.login === 'admin' ? 'admin' : 'gerente'

        const usuarioFalso = {
          login: this.login,
          nome: this.login.toUpperCase(), // Improviso estético
          auth: nivelAuth
        }

        // Salva no navegador para usar nas outras telas
        localStorage.setItem('usuario_app', JSON.stringify(usuarioFalso))

        // Redireciona para o Dashboard
        this.$router.push('/dashboard')
      } catch (err) {
        console.error(err)
        this.error = 'Erro de conexão com o servidor.'
      }
    }
  }
}
</script>

<style scoped>
/* Fundo Elegante (Gradiente Azul Escuro) */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
  font-family: 'Roboto', 'Helvetica Neue', sans-serif;
}

/* Cartão com sombra suave */
.login-card {
  background: white;
  padding: 2.5rem;
  border-radius: 8px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2); /* Sombra mais sofisticada */
  width: 100%;
  max-width: 380px;
}

.login-header h2 {
  text-align: center;
  color: #2c3e50; /* Azul chumbo */
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.login-header p {
  text-align: center;
  color: #7f8c8d;
  font-size: 0.9rem;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.2rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #34495e;
  font-weight: 600;
  font-size: 0.9rem;
}

input {
  width: 100%;
  padding: 12px;
  border: 1px solid #dfe6e9;
  border-radius: 6px;
  box-sizing: border-box;
  font-size: 1rem;
  background-color: #fdfdfd;
  transition: border-color 0.3s;
}

input:focus {
  outline: none;
  border-color: #2980b9; /* Azul focado */
  background-color: #fff;
}

/* Botão Profissional */
.btn-submit {
  width: 100%;
  padding: 14px;
  background-color: #2980b9; /* Azul Corporativo */
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s, transform 0.1s;
  font-weight: 600;
  margin-top: 10px;
}

.btn-submit:hover:not(:disabled) {
  background-color: #1a5276; /* Azul mais escuro no hover */
}

.btn-submit:active {
  transform: scale(0.98);
}

.btn-submit:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.error-msg {
  margin-top: 15px;
  color: #c0392b;
  font-size: 0.9rem;
  text-align: center;
  background-color: #fadbd8;
  padding: 10px;
  border-radius: 5px;
}

.login-footer {
  margin-top: 2rem;
  text-align: center;
}

.login-footer p {
  color: #b2bec3;
  font-size: 0.8rem;
}
</style>
