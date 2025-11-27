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
                <th></th>
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
                <td class="action-cell">
                  <button @click="deleteTarefa(t._id.$oid)" class="btn-delete" title="Excluir">
                    ✕
                  </button>
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
                <th></th>
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
                <td class="action-cell">
                  <button @click="deleteTarefa(t._id.$oid)" class="btn-delete" title="Excluir">
                    ✕
                  </button>
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
                <th></th>
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
                <td class="action-cell">
                  <button @click="deleteTarefa(t._id.$oid)" class="btn-delete" title="Excluir">
                    ✕
                  </button>
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
        // Garante que o status existe nas chaves, senão joga pro 'A fazer'
        let s = t.status
        if (!groups[s]) s = 'A fazer'

        groups[s].push(t)
      })

      return groups
    }
  },
  created () {
    this.fetchUser() // Carrega usuário do localStorage
    this.fetchAll() // Busca tarefas do backend
  },
  methods: {
    // Busca usuário simulado do LocalStorage
    fetchUser () {
      // const dadosSalvos = localStorage.getItem('usuario_app')
      // if (dadosSalvos) {
      //   this.user = JSON.parse(dadosSalvos)
      // } else {
      //   this.user = { nome: 'Visitante', auth: 'guest' }
      // }
      this.user = {
        nome: localStorage.getItem('nome'),
        auth: localStorage.getItem('auth'),
        username: localStorage.getItem('username')
      }
    },

    async fetchAll () {
      try {
        // Envia params vazio para garantir header correto no backend
        const res = await api.post('/get-tarefas', {})

        // O Axios geralmente converte o JSON automaticamente
        this.tarefas = res.data
      } catch (err) {
        console.error('Erro ao buscar tarefas:', err)
      }
    },

    async changeStatus (t) {
      try {
        // Envia dados como Formulário
        const params = new URLSearchParams()
        params.append('status', t.status)

        await api.post(`/update-status-tarefa/${t._id.$oid}`, params)

        // Atualiza a lista para garantir sincronia
        this.fetchAll()
      } catch (err) {
        console.error('Erro ao mudar status:', err)
        alert('Erro ao mudar status')
      }
    },

    async deleteTarefa (id) {
      if (!confirm('Tem certeza que deseja excluir esta tarefa?')) return

      try {
        // Envia POST vazio (mas formatado corretamente)
        const params = new URLSearchParams()
        await api.post(`/delete-tarefa/${id}`, params)

        this.fetchAll()
      } catch (err) {
        console.error('Erro ao excluir:', err)
        alert('Erro ao excluir tarefa')
      }
    },

    async logout () {
      try {
        const params = new URLSearchParams()
        await api.post('/logout', params)
      } catch (err) {
        console.error(err)
      } finally {
        // Limpa o usuário simulado e redireciona
        localStorage.removeItem('nome')
        localStorage.removeItem('auth')
        localStorage.removeItem('username')
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
  background-color: #f4f6f9; /* Fundo cinza claro corporativo */
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Navbar */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
  height: 60px;
  background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); /* Mesmo gradiente do login */
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

.btn-refresh:hover {
  background: rgba(255,255,255,0.2);
}

.btn-logout:hover {
  background: #c0392b;
  border-color: #c0392b;
}

/* Área Principal (Kanban) */
.board-layout {
  display: flex;
  gap: 20px;
  padding: 20px;
  flex: 1;
  overflow-x: auto; /* Permite scroll se a tela for pequena */
}

.column-card {
  flex: 1;
  min-width: 300px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
  height: 100%; /* Ocupa altura toda */
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

/* Botão de Excluir */
.action-cell {
  text-align: right;
  width: 40px;
}

.btn-delete {
  background: none;
  border: none;
  color: #e74c3c;
  cursor: pointer;
  font-size: 1rem;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background 0.2s;
}

.btn-delete:hover {
  background: #fadbd8;
}
</style>
