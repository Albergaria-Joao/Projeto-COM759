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
        <button @click="logout" class="btn-logout">
          Sair
        </button>
      </div>
    </header>

    <main class="content-area">

      <div v-if="user && user.auth === 'admin'" class="card-container">
        <div class="card-header">
          <h3>Equipes Cadastradas</h3>
          <div class="header-actions">
             <button @click="goToCreate" class="btn-create">
              + Criar Equipe
            </button>
            <span class="badge">{{ equipes.length }} equipes</span>
          </div>
        </div>

        <div class="table-responsive">
          <table>
            <thead>
              <tr>
                <th>Nome da Equipe</th>
                <th>Descrição</th>
                <th style="text-align: right;">Ações</th> </tr>
            </thead>
            <tbody>
              <tr v-if="equipes.length === 0">
                <td colspan="3" class="empty-state">Nenhuma equipe encontrada.</td>
              </tr>
              <tr v-for="e in equipes" :key="e._id.$oid">
                <td class="team-name">{{ e.nome }}</td>
                <td class="team-desc">{{ e.descricao }}</td>
                <td class="actions-cell">
                  <button class="btn-action btn-edit" @click="editarEquipe(e._id.$oid)" title="Editar">
                    ✏️ Editar
                  </button>

                  <button class="btn-action btn-delete" @click="deletarEquipe(e._id.$oid)" title="Excluir">
                    🗑️ Excluir
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div v-else class="access-denied-card">
        <div class="icon-lock">🔒</div>
        <h3>Acesso Restrito</h3>
        <p>Apenas administradores podem visualizar e gerenciar as equipes.</p>
        <button @click="$router.push('/dashboard')" class="btn-back">
          Voltar para minhas tarefas
        </button>
      </div>

    </main>
  </div>
</template>

<script>
/* eslint-disable */
import api from '@/api'

export default {
  name: 'EquipesView',
  data() {
    return {
      equipes: [],
      user: null
    }
  },
  async created() {
    this.fetchUser()
    if (this.user && this.user.auth === 'admin') {
      this.fetchEquipes()
    }
  },
  methods: {
    fetchUser () {
      this.user = {
        nome: localStorage.getItem('nome'),
        auth: localStorage.getItem('auth'),
        username: localStorage.getItem('username')
      }
    },

    async fetchEquipes() {
      try {
        const params = new URLSearchParams()
        const res = await api.post('/get-equipes', params)
        this.equipes = res.data
      } catch (e) {
        console.error('Erro ao buscar equipes:', e)
      }
    },

    async logout() {
      try {
        const params = new URLSearchParams()
        await api.post('/logout', params)
      } catch (err) {
        console.error(err)
      } finally {
        localStorage.removeItem('nome')
        localStorage.removeItem('auth')
        localStorage.removeItem('username')
        this.$router.push('/login')
      }
    },

    editarEquipe (id) {
      this.$router.push(`/update-equipe?id=${id}`)
    },

    goToCreate () {
      this.$router.push("/create-equipe");
    },

    async deletarEquipe(id) {
      if (!confirm("Tem certeza que deseja excluir esta equipe?")) {
        return
      }
      try {
        const payload = new URLSearchParams()
        payload.append("id", id)
        const res = await api.post(`/delete-equipe/${id}`, {})
        alert(res.data.mensagem || "Equipe removida!")
        this.fetchEquipes()
      } catch (err) {
        console.error("Erro ao excluir equipe:", err)
        alert("Erro ao excluir.")
      }
    }
  }
}
</script>

<style scoped>
/* Layout Geral */
.page-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f4f6f9;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Navbar */
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
.user-info { text-align: right; margin-right: 10px; }
.user-name { display: block; font-weight: bold; font-size: 0.9rem; }
.user-role { display: block; font-size: 0.75rem; opacity: 0.8; text-transform: uppercase; }

.btn-nav, .btn-logout {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  border: 1px solid rgba(255,255,255,0.3);
  background: rgba(255,255,255,0.1);
  color: white;
  transition: all 0.2s;
}
.btn-nav:hover { background: rgba(255,255,255,0.2); }
.btn-logout:hover { background: #c0392b; border-color: #c0392b; }

/* Área de Conteúdo */
.content-area { padding: 40px; display: flex; justify-content: center; }

/* Cartão */
.card-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  width: 100%;
  max-width: 900px;
  overflow: hidden;
}

.card-header {
  padding: 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
}
.card-header h3 { margin: 0; color: #2c3e50; font-size: 1.1rem; }

/* Header Actions (Novo) */
.header-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.badge {
  background: #3498db;
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
}

/* --- ESTILO NOVO DO BOTÃO CRIAR --- */
.btn-create {
  background-color: #27ae60; /* Verde */
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.2s;
  box-shadow: 0 2px 5px rgba(39, 174, 96, 0.3);
}
.btn-create:hover {
  background-color: #219150;
  transform: translateY(-1px);
}

/* Tabela */
.table-responsive { width: 100%; overflow-x: auto; }
table { width: 100%; border-collapse: collapse; }

th {
  background-color: #f8f9fa;
  color: #7f8c8d;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.8rem;
  padding: 15px 20px;
  text-align: left;
  border-bottom: 2px solid #eee;
}

td {
  padding: 15px 20px;
  border-bottom: 1px solid #f1f2f6;
  color: #2c3e50;
  vertical-align: middle;
}

.team-name { font-weight: 600; color: #2980b9; }
.team-desc { color: #636e72; }

/* --- ESTILO NOVO DOS BOTÕES DE AÇÃO --- */
.actions-cell {
  text-align: right; /* Joga os botões para a direita */
  white-space: nowrap; /* Não deixa quebrar linha */
}

.btn-action {
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  margin-left: 8px; /* Espaço entre eles */
  transition: all 0.2s;
  color: white;
}

.btn-edit {
  background-color: #f39c12; /* Laranja/Amarelo */
}
.btn-edit:hover {
  background-color: #e67e22;
}

.btn-delete {
  background-color: #e74c3c; /* Vermelho */
}
.btn-delete:hover {
  background-color: #c0392b;
}

.empty-state { text-align: center; padding: 40px; color: #b2bec3; font-style: italic; }

/* Access Denied */
.access-denied-card {
  background: white; padding: 40px; border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center; max-width: 400px;
}
.icon-lock { font-size: 3rem; margin-bottom: 15px; }
.access-denied-card h3 { color: #c0392b; margin-bottom: 10px; }
.btn-back {
  background-color: #34495e; color: white; border: none;
  padding: 10px 20px; border-radius: 4px; cursor: pointer;
}
</style>
