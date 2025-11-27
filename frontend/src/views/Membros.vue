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
        <button @click="logout" class="btn-logout">Sair</button>
      </div>
    </header>

    <main class="content-area">
      <div class="card-container">
        <div class="card-header">
          <h3>Membros Cadastrados</h3>
          <div class="header-actions">
            <button v-if="user && user.auth === 'admin'" @click="goToCreate" class="btn-create">
              + Criar Membro
            </button>
            <span class="count-badge">{{ membrosFiltered.length }} usuários</span>
          </div>
        </div>

        <div class="table-responsive">
          <table>
            <thead>
              <tr>
                <th>Nome</th>
                <th>Login</th>
                <th>Email</th>
                <th>Equipe</th>
                <th>Permissão</th>
                <th style="text-align: right;">Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="membrosFiltered.length === 0">
                <td colspan="6" class="empty-state">
                  Nenhum membro encontrado.
                </td>
              </tr>

              <tr v-for="m in membrosFiltered" :key="m._id.$oid">
                <td class="col-name">{{ m.nome }}</td>
                <td class="col-login">{{ m.login }}</td>
                <td class="col-email">{{ m.email }}</td>
                <td class="col-team">
                  {{ m.equipe_nome ? m.equipe_nome : '—' }}
                </td>
                <td>
                  <span :class="['auth-badge', `auth-${m.auth}`]">
                    {{ m.auth }}
                  </span>
                </td>
                <td class="actions-cell">
                  <div v-if="user && (user.auth === 'admin' || user.auth === 'gerente')">
                    <button class="btn-action btn-edit" @click="editarMembro(m._id.$oid)" title="Editar">
                      ✏️ Editar
                    </button>
                    <button class="btn-action btn-delete" @click="deletarMembro(m._id.$oid)" title="Excluir">
                      🗑️ Excluir
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
/* eslint-disable */
import api from '@/api';

export default {
  name: 'MembrosView',
  data() {
    return {
      membros: [],
      user: null,
    };
  },
  computed: {
    membrosFiltered() {
      if (!this.user) return this.membros;
      return this.membros;
    },
  },
  created() {
    this.fetchUser();
    this.fetchMembros();
  },
  methods: {
    fetchUser() {
      this.user = {
        nome: localStorage.getItem('nome'),
        auth: localStorage.getItem('auth'),
        username: localStorage.getItem('username')
      }
    },

    async fetchMembros() {
      try {
        // CORREÇÃO AQUI: Enviando objeto vazio {} em vez de URLSearchParams
        const res = await api.post('/get-membros', {});
        this.membros = res.data;
      } catch (e) {
        console.error('Erro ao buscar membros:', e);
      }
    },

    goToCreate() {
      this.$router.push('/create-membro');
    },

    editarMembro(id) {
      this.$router.push(`/update-membro?id=${id}`);
    },

    async deletarMembro(id) {
      if (!confirm("Tem certeza que deseja excluir este membro?")) {
        return;
      }
      try {
        // Já estava correto aqui, manteve {}
        const res = await api.post(`/delete-membro/${id}`, {});
        alert(res.data.mensagem || "Membro removido!");
        this.fetchMembros();
      } catch (err) {
        console.error("Erro ao excluir membro:", err);
        alert("Erro ao excluir.");
      }
    },

    async logout() {
      try {
        // CORREÇÃO AQUI TAMBÉM: Enviando objeto vazio {}
        await api.post('/logout', {});
      } catch (err) {
        console.error(err);
      } finally {
        localStorage.removeItem('nome')
        localStorage.removeItem('auth')
        localStorage.removeItem('username')
        this.$router.push('/login');
      }
    },
  },
};
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
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
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

.btn-nav,
.btn-logout {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.1);
  color: white;
  transition: all 0.2s;
}

.btn-nav:hover { background: rgba(255, 255, 255, 0.2); }
.btn-logout:hover { background: #c0392b; border-color: #c0392b; }

/* Área de Conteúdo */
.content-area {
  padding: 40px;
  display: flex;
  justify-content: center;
}

/* Cartão */
.card-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  width: 100%;
  max-width: 1000px;
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

.header-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.btn-create {
  background-color: #27ae60;
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

.count-badge {
  background: #7f8c8d;
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
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

tr:last-child td { border-bottom: none; }
tr:hover { background-color: #fcfcfc; }

.col-name { font-weight: 600; color: #2c3e50; }
.col-login { color: #2980b9; font-family: monospace; }
.col-email { color: #7f8c8d; }
.col-team { font-weight: 500; }

.empty-state { text-align: center; padding: 40px; color: #b2bec3; font-style: italic; }

.auth-badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: bold;
  text-transform: uppercase;
}
.auth-admin { background-color: #e74c3c; color: white; }
.auth-gerente { background-color: #3498db; color: white; }
.auth-peao, .auth-user { background-color: #95a5a6; color: white; }

.actions-cell { text-align: right; white-space: nowrap; }

.btn-action {
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  margin-left: 8px;
  transition: all 0.2s;
  color: white;
}

.btn-edit { background-color: #f39c12; }
.btn-edit:hover { background-color: #e67e22; }

.btn-delete { background-color: #e74c3c; }
.btn-delete:hover { background-color: #c0392b; }
</style>