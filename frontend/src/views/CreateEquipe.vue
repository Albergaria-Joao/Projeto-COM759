<template>
  <div class="container">
    <h2>Criar Equipe</h2>

    <form @submit.prevent="createEquipe">
      <div class="field">
        <label>Nome:</label>
        <input type="text" v-model="nome" required />
      </div>

      <div class="field">
        <label>Descrição:</label>
        <input type="text" v-model="descricao" required />
      </div>

      <button type="submit">Enviar</button>
    </form>
  </div>
</template>

<script>
import api from '@/api'

export default {
  name: 'CreateEquipe',

  data () {
    return {
      nome: '',
      descricao: ''
    }
  },

  methods: {
    async createEquipe () {
      try {
        const response = await api.post('/create-equipe', {
          nome: this.nome,
          descricao: this.descricao
        })

        alert(response.data.mensagem)
        this.$router.push('/equipes')
      } catch (err) {
        console.error(err)
        alert('Erro ao criar equipe.')
      }
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 500px;
  margin: auto;
  padding: 20px;
}

.field {
  margin-bottom: 12px;
  display: flex;
  flex-direction: column;
}

input {
  padding: 8px;
  font-size: 16px;
}

button {
  padding: 10px 15px;
  font-size: 16px;
  cursor: pointer;
}
</style>
