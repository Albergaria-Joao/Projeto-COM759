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
        <button @click="$router.push('/dashboard')" class="btn-nav">
          Voltar ao Dashboard
        </button>
      </div>
    </header>

    <main class="content-area">
      <div class="card-container form-card">
        <div class="card-header">
          <h3>Editar Tarefa</h3>
        </div>

        <div class="card-body">
          <form @submit.prevent="updateTarefa">

            <div class="form-row">
              <div class="form-group full">
                <label>Nome da Tarefa</label>
                <input type="text" v-model="form.nome" required placeholder="Ex: Corrigir bug do login">
              </div>
            </div>

            <div class="form-row">
              <div class="form-group full">
                <label>Descrição</label>
                <textarea v-model="form.descricao" rows="3" placeholder="Detalhes da tarefa..."></textarea>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group half">
                <label>Prazo</label>
                <input type="date" v-model="form.prazo" required>
              </div>

              <div class="form-group half">
                <label>Equipe Responsável</label>
                <select v-model="form.equipe_id" @change="fetchMembros" required>
                  <option value="" disabled>Selecione a equipe</option>
                  <option v-for="eq in listaEquipes" :key="eq._id.$oid" :value="eq._id.$oid">
                    {{ eq.nome }}
                  </option>
                </select>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group full">
                <label>Membro Responsável</label>
                <select v-model="form.membro_id" required>
                  <option value="" disabled>Selecione o membro</option>
                  <option v-for="m in listaMembros" :key="m._id.$oid" :value="m._id.$oid">
                    {{ m.nome }} ({{ m.login }})
                  </option>
                </select>
              </div>
            </div>

            <div class="form-actions">
              <button type="button" class="btn-cancel" @click="$router.push('/dashboard')">Cancelar</button>
              <button type="submit" class="btn-save">Salvar Alterações</button>
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
  name: 'UpdateTarefa',
  data () {
    return {
      user: null,
      id: null,
      listaEquipes: [],
      listaMembros: [],
      form: {
        nome: '',
        descricao: '',
        prazo: '',
        equipe_id: '',
        membro_id: ''
      }
    }
  },
  async created () {
    this.fetchUser()
    this.id = this.$route.query.id

    if (this.id) {
      await this.loadInitialData()
    } else {
      alert('ID da tarefa não fornecido.')
      this.$router.push('/dashboard')
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
      if (this.user.auth !== 'admin' && this.user.auth !== 'gerente') {
        alert('Acesso negado')
        this.$router.push('/dashboard')
      }
    },

    async loadInitialData () {
      try {
        // 1. Carrega Equipes (para o select)
        const resEquipes = await api.post('/get-equipes', {})
        this.listaEquipes = resEquipes.data

        // 2. Carrega a Tarefa Atual
        const resTarefa = await api.post(`/get-tarefas/${this.id}`, {})
        const tarefa = resTarefa.data

        // Preenche o formulário
        this.form.nome = tarefa.nome
        this.form.descricao = tarefa.descricao
        this.form.prazo = tarefa.prazo

        // Extrai o ID do objeto $oid se necessário (Mongo retorna assim: { $oid: "..." })
        this.form.equipe_id = tarefa.equipe_id.$oid || tarefa.equipe_id

        // 3. Carrega os Membros (baseado na equipe da tarefa)
        await this.fetchMembros()

        // Define o membro (depois de carregar a lista)
        this.form.membro_id = tarefa.membro_id.$oid || tarefa.membro_id
      } catch (err) {
        console.error('Erro ao carregar dados:', err)
        alert('Erro ao carregar dados da tarefa.')
      }
    },

    // Busca membros filtrados pela equipe selecionada
    async fetchMembros () {
      if (!this.form.equipe_id) return
      try {
        const payload = { equipe_id: this.form.equipe_id }
        const res = await api.post('/get-membros', payload)
        this.listaMembros = res.data
      } catch (err) {
        console.error(err)
      }
    },

    async updateTarefa () {
      try {
        const payload = {
          id: this.id,
          nome: this.form.nome,
          descricao: this.form.descricao,
          prazo: this.form.prazo,
          equipe_id: this.form.equipe_id,
          membro_id: this.form.membro_id
        }

        // Envia JSON para evitar erro 415
        await api.post('/update-tarefa', payload)

        alert('Tarefa atualizada com sucesso!')
        this.$router.push('/dashboard')
      } catch (err) {
        console.error(err)
        alert('Erro ao atualizar tarefa. Verifique se você é Gerente ou Admin.')
      }
    }
  }
}
</script>

<style scoped>
/* REUTILIZANDO O DESIGN SYSTEM */
.page-container {
  display: flex; flex-direction: column; height: 100vh;
  background-color: #f4f6f9; font-family: 'Segoe UI', sans-serif;
}

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

.content-area { padding: 40px; display: flex; justify-content: center; }

.card-container {
  background: white; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  width: 100%; max-width: 800px; overflow: hidden;
}

.card-header { padding: 20px; border-bottom: 1px solid #eee; background-color: #fff; }
.card-header h3 { margin: 0; color: #2c3e50; font-size: 1.1rem; }
.card-body { padding: 30px; }

.form-row { display: flex; gap: 20px; margin-bottom: 20px; }
.form-group { margin-bottom: 0; }
.half { flex: 1; }
.full { flex: 1; width: 100%; }

.form-group label {
  display: block; margin-bottom: 8px; color: #34495e; font-weight: 600; font-size: 0.9rem;
}

input, select, textarea {
  width: 100%; padding: 12px; border: 1px solid #dfe6e9; border-radius: 6px;
  font-size: 1rem; color: #2c3e50; background-color: #fcfcfc;
  box-sizing: border-box; transition: border-color 0.3s;
}
input:focus, select:focus, textarea:focus {
  outline: none; border-color: #3498db; background-color: white;
}

.form-actions { display: flex; justify-content: flex-end; gap: 15px; margin-top: 30px; }

.btn-save {
  background-color: #2980b9; color: white; border: none; padding: 12px 24px;
  border-radius: 6px; font-weight: 600; cursor: pointer;
}
.btn-save:hover { background-color: #21618c; }

.btn-cancel {
  background-color: #ecf0f1; color: #7f8c8d; border: none; padding: 12px 24px;
  border-radius: 6px; font-weight: 600; cursor: pointer;
}
.btn-cancel:hover { background-color: #bdc3c7; color: #2c3e50; }

@media (max-width: 600px) { .form-row { flex-direction: column; gap: 15px; } }
</style>
