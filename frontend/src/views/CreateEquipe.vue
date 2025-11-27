<template>
  <div class="page-container">

    <header class="navbar">
      <div class="brand">
        <h2>Gestão de Tarefas</h2>
      </div>
      <div class="user-controls">
        <div v-if="user" class="user-info">
          <span class="user-name">{{ user.nome }}</span>
          <span class="user-role">{{ user.auth }}</span>
        </div>
        <button @click="fetchAll" class="btn-refresh">
          Atualizar
        </button>
        <button @click="logout" class="btn-logout">
          Sair
        </button>
      </div>
    </header>

    <main class="content-area">

      <div v-if="user && user.auth === 'admin'" class="form-card">
        <h3>Criar Nova Equipe</h3>

        <form @submit.prevent="createEquipe">

          <label>Nome</label>
          <input type="text" v-model="nome" required />

          <label>Descrição</label>
          <input type="text" v-model="descricao" required />

          <button type="submit" class="btn-save">
            Criar Equipe
          </button>
        </form>
      </div>

      <div v-else class="access-denied-card">
        <div class="icon-lock">🔒</div>
        <h3>Acesso Restrito</h3>
        <p>Apenas administradores podem criar equipes.</p>
        <button @click="$router.push('/dashboard')" class="btn-back">
          Voltar para minhas tarefas
        </button>
      </div>

    </main>
  </div>
</template>

<script>
import api from '@/api'

export default {
  name: 'CreateEquipe',

  data () {
    return {
      user: null,
      nome: '',
      descricao: ''
    }
  },

  created () {
    this.fetchUser()
  },

  methods: {

    fetchUser () {
      this.user = {
        nome: localStorage.getItem('nome'),
        auth: localStorage.getItem('auth'),
        username: localStorage.getItem('username'),
        equipe_id: localStorage.getItem('equipe_id')
      }
      if (this.user.auth !== 'admin') {
        alert('Acesso negado')
        this.$router.push('/dashboard')
      }
    },

    async createEquipe () {
      try {
        const response = await api.post('/create-equipe', {
          nome: this.nome,
          descricao: this.descricao
        })

        alert(response.data.mensagem)
        this.$router.push('/equipes')
        window.location.reload(true)
      } catch (err) {
        console.error(err)
        alert('Erro ao criar equipe.')
      }
    },

    async logout () {
      try {
        await api.post('/logout', {}) // Manda JSON vazio
      } catch (err) {
        console.error(err)
      } finally {
        localStorage.removeItem('nome')
        localStorage.removeItem('auth')
        localStorage.removeItem('username')
        localStorage.removeItem('equipe_id')
        this.$router.push('/login')
      }
    }
  }
}
</script>

<style scoped>

.page-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f4f6f9;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
  height: 60px;
  background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
  color: white;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.brand h2 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.user-controls {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-info {
  text-align: right;
  margin-right: 10px;
}

.user-name {
  display: block;
  font-weight: bold;
  font-size: 0.9rem;
}

.user-role {
  display: block;
  font-size: 0.75rem;
  opacity: 0.8;
  text-transform: uppercase;
}

.btn-refresh, .btn-logout {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  border: 1px solid rgba(255,255,255,0.3);
  background: rgba(255,255,255,0.1);
  color: white;
  transition: all 0.2s;
}

.btn-refresh:hover {
  background: rgba(255,255,255,0.2);
}

.btn-logout:hover {
  background: #c0392b;
  border-color: #c0392b;
}

.content-area {
  padding: 40px;
  display: flex;
  justify-content: center;
}

.form-card {
  background: white;
  padding: 30px;
  border-radius: 8px;
  max-width: 450px;
  width: 100%;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.form-card h3 {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-top: 15px;
  margin-bottom: 5px;
  color: #34495e;
  font-weight: 600;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #dcdde1;
  border-radius: 4px;
  margin-bottom: 10px;
}

.btn-save {
  width: 100%;
  margin-top: 15px;
  padding: 10px;
  background: #2980b9;
  border: none;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.btn-save:hover {
  background: #3498db;
}

.access-denied-card {
  background: white;
  padding: 40px;
  border-radius: 8px;
  text-align: center;
  max-width: 400px;
}

.btn-back {
  background-color: #34495e;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
}
</style>
