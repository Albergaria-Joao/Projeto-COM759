<template>
  <div class='page-container'>
    <header class='navbar'>
      <div class='brand'>
        <h2>Gestão de Membros</h2>
      </div>
      <div class='user-controls'>
        <div v-if='user' class='user-info'>
          <span class='user-name'>{{ user.nome }}</span>
          <span class='user-role'>{{ user.auth }}</span>
        </div>
        <button @click="$router.push('/dashboard')" class='btn-nav'>
          Voltar ao Dashboard
        </button>
        <button @click='logout' class='btn-logout'>Sair</button>
      </div>
    </header>

    <main class='content-area'>
      <div class='card-container'>
        <div class='card-header'>
          <h3>Membros Cadastrados</h3>
          <span class='count-badge'>{{ membrosFiltered.length }} usuários</span>
        </div>

        <div class='table-responsive'>
          <table>
            <thead>
              <tr>
                <th>Nome</th>
                <th>Login</th>
                <th>Email</th>
                <th>Equipe</th>
                <th>Permissão</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if='membrosFiltered.length === 0'>
                <td colspan='5' class='empty-state'>
                  Nenhum membro encontrado.
                </td>
              </tr>

              <tr v-for='m in membrosFiltered' :key='m._id.$oid'>
                <td class='col-name'>{{ m.nome }}</td>
                <td class='col-login'>{{ m.login }}</td>
                <td class='col-email'>{{ m.email }}</td>
                <td class='col-team'>
                  {{ m.equipe_nome ? m.equipe_nome : '—' }}
                </td>
                <td>
                  <span :class="['auth-badge', `auth-${m.auth}`]">
                    {{ m.auth }}
                  </span>
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
import api_post from '@/api';

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
      // Se não tiver usuário carregado, mostra tudo ou nada (optei por mostrar)
      if (!this.user) return this.membros;

      // Se for admin, vê todo mundo
      if (this.user.auth === 'admin') return this.membros;

      // Lógica de filtro:
      // Como o backend projeta 'equipe_nome' e não ID, filtramos pelo que temos.
      // Se não tiver info de equipe no usuário local, retorna tudo para não travar.
      return this.membros;
    },
  },
  created() {
    this.fetchUser();
    this.fetchMembros();
  },
  methods: {
    fetchUser() {
      const dadosSalvos = localStorage.getItem('usuario_app');
      if (dadosSalvos) {
        this.user = JSON.parse(dadosSalvos);
      } else {
        this.user = { nome: 'Visitante', auth: 'guest' };
      }
    },

    async fetchMembros() {
      try {
        const params = new URLSearchParams();
        // Envia POST vazio (form-data) para pegar todos
        const res = await api_post('/get-membros', params);
        this.membros = res.data;
      } catch (e) {
        console.error('Erro ao buscar membros:', e);
      }
    },

    async logout() {
      try {
        const params = new URLSearchParams();
        await api.post('/logout', params);
      } catch (err) {
        console.error(err);
      } finally {
        localStorage.removeItem('usuario_app');
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

/* Botões da Navbar */
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

.btn-nav:hover {
  background: rgba(255, 255, 255, 0.2);
}

.btn-logout:hover {
  background: #c0392b;
  border-color: #c0392b;
}

/* Área de Conteúdo */
.content-area {
  padding: 40px;
  display: flex;
  justify-content: center;
}

/* Cartão da Tabela */
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

.card-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.1rem;
}

.count-badge {
  background: #7f8c8d;
  color: white;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
}

/* Tabela */
.table-responsive {
  width: 100%;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

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

tr:last-child td {
  border-bottom: none;
}

tr:hover {
  background-color: #fcfcfc;
}

.col-name {
  font-weight: 600;
  color: #2c3e50;
}
.col-login {
  color: #2980b9;
  font-family: monospace;
}
.col-email {
  color: #7f8c8d;
}
.col-team {
  font-weight: 500;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #b2bec3;
  font-style: italic;
}

/* Badges de Permissão */
.auth-badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: bold;
  text-transform: uppercase;
}

.auth-admin {
  background-color: #e74c3c;
  color: white;
}

.auth-gerente {
  background-color: #3498db;
  color: white;
}

.auth-peao,
.auth-user {
  background-color: #95a5a6;
  color: white;
}
</style>
