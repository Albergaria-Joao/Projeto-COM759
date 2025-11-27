import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/views/Login'
import Dashboard from '@/views/Dashboard'
import Membros from '@/views/Membros'
import Equipes from '@/views/Equipes'
import UpdateEquipe from '@/views/UpdateEquipe'
import CreateEquipe from '@/views/CreateEquipe'
import CreateMembro from '@/views/CreateMembro'
import UpdateMembro from '@/views/UpdateMembro'
import UpdateTarefa from '@/views/UpdateTarefa'
Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    { path: '/', redirect: '/dashboard' },
    { path: '/login', component: Login },
    { path: '/dashboard', component: Dashboard },
    { path: '/membros', component: Membros },
    { path: '/equipes', component: Equipes },
    { path: '/update-equipe', component: UpdateEquipe },
    { path: '/create-equipe', component: CreateEquipe },
    { path: '/create-membro', component: CreateMembro },
    { path: '/update-membro', component: UpdateMembro },
    { path: '/update-tarefa', component: UpdateTarefa }
  ]
})
