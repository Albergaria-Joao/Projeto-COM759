<template>
  <div class="page-container">

    <header class="navbar">
      <div class="brand">
        <h2>Gestão de Membros</h2>
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
      <div class="card-container form-card">
        <div class="card-header">
          <h3>Novo Membro</h3>
        </div>

        <div class="card-body">
          <form @submit.prevent="createMembro">

            <div class="form-row">
              <div class="form-group half">
                <label>Nome Completo</label>
                <input type="text" v-model="form.nome" required placeholder="Ex: João da Silva">
              </div>

              <div class="form-group half">
                <label>Login (Usuário)</label>
                <input type="text" v-model="form.login" required placeholder="Ex: joao.silva">
              </div>
            </div>

            <div class="form-row">
              <div class="form-group half">
                <label>Email</label>
                <input type="email" v-model="form.email" required placeholder="joao@email.com">
              </div>

              <div class="form-group half">
                <label>Senha</label>
                <input type="password" v-model="form.senha" required placeholder="******">
              </div>
            </div>

            <div class="form-row">
              <div class="form-group half">
                <label>Equipe</label>
                <select v-model="form.equipe_id" required>
                  <option value="" disabled>Selecione uma equipe</option>
                  <option v-for="eq in listaEquipes" :key="eq._id.$oid" :value="eq._id.$oid">
                    {{ eq.nome }}
                  </option>
                </select>
              </div>

              <div class="form-group half">
                <label>Permissão</label>
                <select v-model="form.auth" required>
                  <option value="peao">Peão (Sem permissão)</option>
                  <option value="gerente">Gerente</option>
                  <option value="admin" v-if="user.auth === 'admin'">Administrador</option>
                </select>
              </div>
            </div>

            <div class="form-actions">
              <button type="button" class="btn-cancel" @click="$router.push('/membros')">Cancelar</button>
              <button type="submit" class="btn-save">Salvar Membro</button>
            </div>

          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script>

import api from '@/api'

export default {
  name: 'CreateMembro',

  data () {
    return {
      user: null, 
      listaEquipes: [],

      form: {
        nome: '',
        login: '',
        email: '',
        senha: '',
        equipe_id: '',
        auth: 'peao' 
      }
    }
  },

  created () {
    this.fetchUser() 
    this.fetchEquipes() 
  },

  methods: {
    fetchUser () {
      this.user = {
        nome: localStorage.getItem('nome'),
        auth: localStorage.getItem('auth'),
        username: localStorage.getItem('username'),
        equipe_id: localStorage.getItem('equipe_id')
      }
      if (this.user.auth !== 'admin' && this.user.auth !== 'gerente') {
        alert('Acesso negado')
        this.$router.push('/dashboard')
      }
    },

    async fetchEquipes () {
      try {
        const response = await api.post('/get-equipes', {})
        this.listaEquipes = response.data
      } catch (err) {
        console.error(err)
        alert('Erro ao carregar lista de equipes.')
      }
    },

    async createMembro () {
      try {
        const response = await api.post('/create-membro', this.form)

        if (response.data.mensagem === 'membro já existe') {
          alert('Erro: Este login já está em uso.')
          return
        }

        alert(response.data.mensagem)
        this.$router.push('/membros')
      } catch (err) {
        console.error(err)
        alert('Erro ao criar membro.')
      }
    }
  }
}
</script>

<style scoped>
/* O DESIGN SYSTEM (MANTIDO PARA FICAR BONITO) */
.page-container {
  display: flex; flex-direction: column; height: 100vh;
  background-color: #f4f6f9; font-family: 'Segoe UI', sans-serif;
}

/* Navbar */
.navbar {
  display: flex; justify-content: space-between; align-items: center;
  padding: 0 2rem; height: 60px; color: white;
  background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
.brand h2 { margin: 0; font-size: 1.2rem; font-weight: 600; }
.user-controls { display: flex; align-items: center; gap: 15px; }
.user-info { text-align: right; }
.user-name { display: block; font-weight: bold; font-size: 0.9rem; }
.user-role { display: block; font-size: 0.75rem; opacity: 0.8; text-transform: uppercase; }

.btn-nav {
  padding: 8px 16px; border-radius: 4px; cursor: pointer;
  border: 1px solid rgba(255,255,255,0.3); background: rgba(255,255,255,0.1); color: white;
}
.btn-nav:hover { background: rgba(255,255,255,0.2); }

/* Conteúdo e Cards */
.content-area { padding: 40px; display: flex; justify-content: center; }

.card-container {
  background: white; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  width: 100%; max-width: 800px; overflow: hidden;
}

.card-header {
  padding: 20px; border-bottom: 1px solid #eee; background-color: #fff;
}
.card-header h3 { margin: 0; color: #2c3e50; font-size: 1.1rem; }

.card-body { padding: 30px; }

/* Formulário */
.form-row { display: flex; gap: 20px; margin-bottom: 20px; }
.form-group { margin-bottom: 0; }
.half { flex: 1; }

.form-group label {
  display: block; margin-bottom: 8px; color: #34495e; font-weight: 600; font-size: 0.9rem;
}

input, select {
  width: 100%; padding: 12px; border: 1px solid #dfe6e9; border-radius: 6px;
  font-size: 1rem; color: #2c3e50; background-color: #fcfcfc;
  box-sizing: border-box; transition: border-color 0.3s;
}
input:focus, select:focus {
  outline: none; border-color: #3498db; background-color: white;
}

/* Botões */
.form-actions { display: flex; justify-content: flex-end; gap: 15px; margin-top: 30px; }

.btn-save {
  background-color: #27ae60; color: white; border: none; padding: 12px 24px;
  border-radius: 6px; font-weight: 600; cursor: pointer;
}
.btn-save:hover { background-color: #219150; }

.btn-cancel {
  background-color: #ecf0f1; color: #7f8c8d; border: none; padding: 12px 24px;
  border-radius: 6px; font-weight: 600; cursor: pointer;
}
.btn-cancel:hover { background-color: #bdc3c7; color: #2c3e50; }

@media (max-width: 600px) { .form-row { flex-direction: column; gap: 15px; } }
</style>
