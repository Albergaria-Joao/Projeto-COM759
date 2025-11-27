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
          <h3>Editar Membro</h3>
        </div>
        <div class="card-body">
          <form @submit.prevent="updateMembro">
            <div class="form-row">
              <div class="form-group half">
                <label for="nome">Nome Completo</label>
                <input type="text" id="nome" v-model="form.nome" required>
              </div>

              <div class="form-group half">
                <label for="login">Login</label>
                <input type="text" id="login" v-model="form.login" disabled class="input-disabled">
              </div>
            </div>

            <div class="form-row">
              <div class="form-group full">
                <label for="email">Email</label>
                <input type="email" id="email" v-model="form.email" required>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group half">
                <label for="equipe">Equipe</label>
                <select id="equipe" v-model="form.equipe_id" required>
                  <option value="" disabled>Selecione uma equipe</option>
                  <option v-for="eq in listaEquipes" :key="eq._id.$oid" :value="eq._id.$oid">
                    {{ eq.nome }}
                  </option>
                </select>
              </div>

              <div class="form-group half">
                <label for="auth">Nível de Permissão</label>
                <select id="auth" v-model="form.auth" required>
                  <option value="peao">Peão (Sem permissão)</option>
                  <option value="gerente">Gerente</option>
                  <option value="admin">Administrador</option>
                </select>
              </div>
            </div>
            <div class="form-row" style="margin-top: 10px;">
                <button type="button" class="btn-reset-pass" @click="resetarSenha">
                    🔄 Resetar Senha do Usuário
                </button>
            </div>

            <div class="form-actions">
              <button type="button" class="btn-cancel" @click="$router.push('/membros')">Cancelar</button>
              <button type="submit" class="btn-save">Salvar Alterações</button>
            </div>

          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
/* eslint-disable */
import api from '@/api'

export default {
  name: 'UpdateMembro',
  data() {
    return {
      user: null,
      id: null,
      listaEquipes: [],
      form: {
        nome: '',
        login: '',
        email: '',
        equipe_id: '',
        auth: ''
      }
    }
  },
  created() {
    this.fetchUser()
    // Pega o ID da URL
    this.id = this.$route.query.id
    
    if (this.id) {
        this.loadInitialData()
    } else {
        alert("ID do membro não fornecido.")
        this.$router.push('/membros')
    }
  },
  methods: {
    fetchUser() {
      this.user = {
        nome: localStorage.getItem('nome'),
        auth: localStorage.getItem('auth'),
        username: localStorage.getItem('username')
      }
      if (this.user.auth !== 'admin' && this.user.auth !== 'gerente') {
        alert("Acesso negado")
        this.$router.push('/dashboard')
      }
    },

    async loadInitialData() {
        try {
            // 1. Busca lista de equipes para o dropdown
            const resEquipes = await api.post('/get-equipes', {})
            this.listaEquipes = resEquipes.data

            // 2. Busca dados do membro
            const resMembro = await api.post(`/get-membros/${this.id}`, {})
            const dados = resMembro.data
            
            this.form.nome = dados.nome
            this.form.login = dados.login
            this.form.email = dados.email
            this.form.auth = dados.auth
            // O backend manda equipe_id como ObjectId, aqui pegamos só a string se vier aninhado ou direto
            this.form.equipe_id = dados.equipe_id.$oid ? dados.equipe_id.$oid : dados.equipe_id
            
        } catch (err) {
            console.error("Erro ao carregar dados", err)
            alert("Erro ao carregar dados do membro.")
        }
    },

    async updateMembro() {
      try {
        const payload = {
            id: this.id,
            nome: this.form.nome,
            email: this.form.email,
            equipe_id: this.form.equipe_id,
            auth: this.form.auth
        }
        
        await api.post('/update-membro', payload)
        
        alert('Membro atualizado com sucesso!')
        this.$router.push('/membros')
        
      } catch (err) {
        console.error(err)
        alert('Erro ao atualizar membro.')
      }
    },

    async resetarSenha() {
        if(!confirm("Deseja gerar uma nova senha aleatória para este usuário?")) return;
        
        try {
            const res = await api.post(`/reset-senha/${this.id}`, {})
            // O backend retorna a nova senha na mensagem
            alert(res.data.mensagem) 
        } catch (err) {
            console.error(err)
            alert("Erro ao resetar senha.")
        }
    }
  }
}
</script>

<style scoped>
/* MESMO ESTILO DO CREATE MEMBRO */
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

.brand h2 { margin: 0; font-size: 1.2rem; font-weight: 600; }
.user-controls { display: flex; align-items: center; gap: 15px; }
.user-info { text-align: right; }
.user-name { display: block; font-weight: bold; font-size: 0.9rem; }
.user-role { display: block; font-size: 0.75rem; opacity: 0.8; text-transform: uppercase; }

.btn-nav {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  border: 1px solid rgba(255,255,255,0.3);
  background: rgba(255,255,255,0.1);
  color: white;
}
.btn-nav:hover { background: rgba(255,255,255,0.2); }

.content-area {
  padding: 40px;
  display: flex;
  justify-content: center;
}

.card-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  width: 100%;
  max-width: 800px;
  overflow: hidden;
}

.card-header {
  padding: 20px;
  border-bottom: 1px solid #eee;
  background-color: #fff;
}
.card-header h3 { margin: 0; color: #2c3e50; font-size: 1.1rem; }

.card-body { padding: 30px; }

.form-row { display: flex; gap: 20px; margin-bottom: 20px;}
.form-group { margin-bottom: 0; }
.half { flex: 1; }
.full { flex: 1; }

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #34495e;
  font-weight: 600;
  font-size: 0.9rem;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 12px;
  border: 1px solid #dfe6e9;
  border-radius: 6px;
  font-size: 1rem;
  color: #2c3e50;
  background-color: #fcfcfc;
  transition: border-color 0.3s, box-shadow 0.3s;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
  background-color: white;
}

.input-disabled {
    background-color: #e9ecef !important;
    color: #6c757d !important;
    cursor: not-allowed;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 30px;
}

.btn-save {
  background-color: #2980b9; /* Azul para update */
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-save:hover { background-color: #21618c; }

.btn-cancel {
  background-color: #ecf0f1;
  color: #7f8c8d;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
}

.btn-reset-pass {
    background: none;
    border: 1px dashed #e74c3c;
    color: #e74c3c;
    padding: 8px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.8rem;
}
.btn-reset-pass:hover {
    background: #e74c3c;
    color: white;
}

@media (max-width: 600px) {
  .form-row { flex-direction: column; gap: 15px; }
}
</style>