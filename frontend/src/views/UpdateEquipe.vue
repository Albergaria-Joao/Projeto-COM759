<template>
  <div class="page-container">

    <header class="navbar">
      <div class="brand">
        <h2>Gestão de Equipes</h2>
      </div>

      <div class="user-controls">
        <div v-if="user" class="user-info">
          <span class="user-name">{{ user.nome }}</span>
          <span class="user-role">{{ user.auth }}</span>
        </div>

        <button @click="$router.push('/dashboard')" class="btn-nav">
          Voltar ao Dashboard
        </button>
      </div>
    </header>

    <main class="content-area">

      <div v-if="user && user.auth === 'admin'" class="form-card">
        <h3>Alterar Equipe</h3>

        <form @submit.prevent="updateEquipe">

          <label>Nome</label>
          <input type="text" v-model="form.nome" required />

          <label>Descrição</label>
          <input type="text" v-model="form.descricao" required />

          <button type="submit" class="btn-save">
            Salvar Alterações
          </button>
        </form>

      </div>

      <div v-else class="access-denied-card">
        <div class="icon-lock">🔒</div>
        <h3>Acesso Restrito</h3>
        <p>Apenas administradores podem alterar equipes.</p>
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
  name: 'UpdateEquipeView',

  data () {
    return {
      user: null,
      id: null,

      form: {
        nome: '',
        descricao: ''
      }
    }
  },

  async created () {
    this.fetchUser()

    this.id = this.$route.query.id

    if (!this.id) {
      console.error('ID não informado na URL.')
      return
    }

    if (this.user && this.user.auth === 'admin') {
      await this.fetchEquipe()
    }
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

    async fetchEquipe () {
      try {
        const res = await api.post(`/get-equipes/${this.id}`)
        this.form.nome = res.data.nome
        this.form.descricao = res.data.descricao
      } catch (err) {
        console.error('Erro ao carregar equipe:', err)
      }
    },

    async updateEquipe () {
      try {
        const payload = {
          id: this.id,
          nome: this.form.nome,
          descricao: this.form.descricao
        }

        const res = await api.post('/update-equipe', payload)

        alert(res.data.mensagem || 'Equipe atualizada!')

        this.$router.push('/equipes')
      } catch (err) {
        console.error('Erro ao atualizar:', err)
        alert('Não foi possível atualizar a equipe.')
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
  background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
  color: white;
}

.user-controls {
  display: flex;
  align-items: center;
  gap: 15px;
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
  font-size: 0.9rem;
}
</style>
