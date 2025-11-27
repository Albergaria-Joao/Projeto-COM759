<template>
  <div class="dashboard-container">

    <header class="navbar">
      <div class="brand">
        <h2>Gestão de Tarefas</h2>
      </div>
      <div class="user-controls">
        <div v-if="user" class="user-info">
          <span class="user-name">{{ user.nome }}</span>
          <span class="user-role">{{ user.auth }}</span>
        </div>
        <button @click="$router.push('/create-tarefa')" class="btn-create" v-if="user.auth === 'admin' || user.auth === 'gerente'">
          + Criar nova tarefa
        </button>
        <button @click="$router.push('/membros')" class="btn-refresh" v-if="user.auth === 'admin' || user.auth === 'gerente'">
          Ir para membros
        </button>
        <button @click="$router.push('/equipes')" class="btn-refresh" v-if="user.auth === 'admin'">
          Ir para equipes
        </button>
        <button @click="fetchAll" class="btn-refresh">
          Atualizar
        </button>
        <button @click="logout" class="btn-logout">
          Sair
        </button>

      </div>
    </header>

    <main class="board-layout">

      <div class="column-card">
        <div class="column-header header-todo">
          <h3>A Fazer</h3>
          <span class="count">{{ tarefasByStatus['A fazer'].length }}</span>
        </div>
        <div class="table-responsive">
          <table>
            <thead>
              <tr>
                <th>Tarefa</th>
                <th>Resp.</th>
                <th>Ação</th>
                <th class="actions-header"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="tarefasByStatus['A fazer'].length === 0">
                <td colspan="4" class="empty-state">Nenhuma tarefa.</td>
              </tr>
              <tr v-for="t in tarefasByStatus['A fazer']" :key="t._id.$oid">
                <td class="task-title">{{ t.nome }}</td>
                <td class="task-owner">{{ t.membro_login ? t.membro_login : '—' }}</td>
                <td>
                  <select v-model="t.status" @change="changeStatus(t)" class="status-select">
                    <option>A fazer</option>
                    <option>Em execução</option>
                    <option>Concluída</option>
                  </select>
                </td>
                <td class="action-cell" v-if="user.auth === 'admin' || user.auth === 'gerente'">
                  <button @click="editTarefa(t._id.$oid)" class="btn-edit" title="Editar">✎</button>
                  <button @click="deleteTarefa(t._id.$oid)" class="btn-delete" title="Excluir">✕</button>
                </td>
                <td v-else class="action-cell">
                  <!-- Usuários comuns não veem nada aqui -->
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="column-card">
        <div class="column-header header-doing">
          <h3>Em Execução</h3>
          <span class="count">{{ tarefasByStatus['Em execução'].length }}</span>
        </div>
        <div class="table-responsive">
          <table>
            <thead>
              <tr>
                <th>Tarefa</th>
                <th>Resp.</th>
                <th>Ação</th>
                <th class="actions-header"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="tarefasByStatus['Em execução'].length === 0">
                <td colspan="4" class="empty-state">Nenhuma tarefa.</td>
              </tr>
              <tr v-for="t in tarefasByStatus['Em execução']" :key="t._id.$oid">
                <td class="task-title">{{ t.nome }}</td>
                <td class="task-owner">{{ t.membro_login ? t.membro_login : '—' }}</td>
                <td>
                  <select v-model="t.status" @change="changeStatus(t)" class="status-select">
                    <option>A fazer</option>
                    <option>Em execução</option>
                    <option>Concluída</option>
                  </select>
                </td>
                <td class="action-cell" v-if="user.auth === 'admin' || user.auth === 'gerente'">
                  <button @click="editTarefa(t._id.$oid)" class="btn-edit" title="Editar">✎</button>
                  <button @click="deleteTarefa(t._id.$oid)" class="btn-delete" title="Excluir">✕</button>
                </td>
                <td v-else class="action-cell">
                  <!-- Usuários comuns não veem nada aqui -->
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div class="column-card">
        <div class="column-header header-done">
          <h3>Concluída</h3>
          <span class="count">{{ tarefasByStatus['Concluída'].length }}</span>
        </div>
        <div class="table-responsive">
          <table>
            <thead>
              <tr>
                <th>Tarefa</th>
                <th>Resp.</th>
                <th>Ação</th>
                <th class="actions-header"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="tarefasByStatus['Concluída'].length === 0">
                <td colspan="4" class="empty-state">Nenhuma tarefa.</td>
              </tr>
              <tr v-for="t in tarefasByStatus['Concluída']" :key="t._id.$oid">
                <td class="task-title">{{ t.nome }}</td>
                <td class="task-owner">{{ t.membro_login ? t.membro_login : '—' }}</td>
                <td>
                  <select v-model="t.status" @change="changeStatus(t)" class="status-select">
                    <option>A fazer</option>
                    <option>Em execução</option>
                    <option>Concluída</option>
                  </select>
                </td>
                <td class="action-cell" v-if="user.auth === 'admin' || user.auth === 'gerente'">
                  <button @click="editTarefa(t._id.$oid)" class="btn-edit" title="Editar">✎</button>
                  <button @click="deleteTarefa(t._id.$oid)" class="btn-delete" title="Excluir">✕</button>
                </td>
                <td v-else class="action-cell">
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
import api from '@/api'

export default {
  data () {
    return {
      tarefas: [],
      user: null
    }
  },
  computed: {
    tarefasByStatus () {
      const groups = { 'A fazer': [], 'Em execução': [], 'Concluída': [] }

      this.tarefas.forEach(t => {
        let s = t.status
        if (!groups[s]) s = 'A fazer'
        groups[s].push(t)
      })

      return groups
    }
  },
  created () {
    this.fetchUser()
    this.fetchAll()
  },
  methods: {
    fetchUser () {
      this.user = {
        nome: localStorage.getItem('nome'),
        auth: localStorage.getItem('auth'),
        username: localStorage.getItem('username'),
        equipe_id: localStorage.getItem('equipe_id')
      }
      console.log(this.user)
      if (!this.user.nome || !this.user.auth) this.$router.push('/login')
    },
    async fetchAll () {
      try {
        const res = await api.post('/get-tarefas', {})
        this.tarefas = res.data
      } catch (err) {
        console.error('Erro ao buscar tarefas:', err)
      }
    },

    // --- CORREÇÃO DO ERRO 415 AQUI ---
    async changeStatus (t) {
      try {
        // MANDA JSON AO INVÉS DE URLSEARCHPARAMS
        const payload = {
          status: t.status
        }
        await api.post(`/update-status-tarefa/${t._id.$oid}`, payload)

        this.fetchAll()
      } catch (err) {
        console.error('Erro ao mudar status:', err)
        alert('Erro ao mudar status')
      }
    },

    editTarefa (id) {
      this.$router.push(`/update-tarefa?id=${id}`)
    },

    async deleteTarefa (id) {
      if (!confirm('Tem certeza que deseja excluir esta tarefa?')) return

      try {
        await api.post(`/delete-tarefa/${id}`, {})
        this.fetchAll()
      } catch (err) {
        console.error('Erro ao excluir:', err)
        alert('Erro ao excluir tarefa')
      }
    },

    async logout () {
      try {
        await api.post('/logout', {}) 
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
/* Layout Geral */
.dashboard-container {
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

.brand h2 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  display: inline-block;
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

/* Botões da Navbar */
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

.btn-create {
  padding: 8px 16px;
  margin-left: 1vw;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  border: 1px solid rgba(255,255,255,0.3);
  background-color: #27ae60;
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

.btn-create:hover {
  background: #219150;
}

/* Área Principal (Kanban) */
.board-layout {
  display: flex;
  gap: 20px;
  padding: 20px;
  flex: 1;
  overflow-x: auto;
}

.column-card {
  flex: 1;
  min-width: 300px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
  height: 100%;
  max-height: calc(100vh - 100px);
}

/* Cabeçalho das Colunas */
.column-header {
  padding: 15px;
  border-bottom: 2px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.column-header h3 {
  margin: 0;
  font-size: 1rem;
  color: #2c3e50;
  font-weight: 700;
  text-transform: uppercase;
}

.count {
  background: #dfe6e9;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
  color: #636e72;
}

/* Cores das bordas dos cabeçalhos */
.header-todo { border-top: 4px solid #f39c12; }
.header-doing { border-top: 4px solid #3498db; }
.header-done { border-top: 4px solid #27ae60; }

/* Tabela */
.table-responsive {
  overflow-y: auto;
  flex: 1;
  padding: 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  text-align: left;
  font-size: 0.75rem;
  color: #7f8c8d;
  text-transform: uppercase;
  padding: 8px 4px;
  border-bottom: 1px solid #dfe6e9;
}

td {
  padding: 12px 4px;
  font-size: 0.9rem;
  color: #2c3e50;
  border-bottom: 1px solid #f1f2f6;
  vertical-align: middle;
}

.empty-state {
  text-align: center;
  color: #b2bec3;
  padding: 20px;
  font-style: italic;
}

.task-title {
  font-weight: 600;
  width: 40%;
}

.task-owner {
  font-size: 0.85rem;
  color: #7f8c8d;
}

/* Select de Status */
.status-select {
  padding: 6px;
  border-radius: 4px;
  border: 1px solid #dfe6e9;
  font-size: 0.8rem;
  color: #2c3e50;
  background-color: #fff;
  width: 100%;
  cursor: pointer;
}

.status-select:focus {
  outline: none;
  border-color: #3498db;
}

/* --- NOVOS ESTILOS PARA OS BOTÕES --- */
.action-cell {
  text-align: right;
  white-space: nowrap; /* Garante que os botões fiquem na mesma linha */
  min-width: 60px;
}

.btn-edit, .btn-delete {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  padding: 4px 6px;
  border-radius: 4px;
  transition: background 0.2s;
  margin-left: 2px;
}

.btn-edit {
  color: #f39c12; /* Laranja para editar */
}
.btn-edit:hover {
  background: #fef5e7;
}

.btn-delete {
  color: #e74c3c; /* Vermelho para excluir */
}
.btn-delete:hover {
  background: #fadbd8;
}
</style>
