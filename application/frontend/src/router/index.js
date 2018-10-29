import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from '../components/Home.vue'
import Login from '../components/Login.vue'
import Signup from '../components/Signup.vue'
import Dashboard from '../components/Dashboard.vue'
import Profile from '../components/Profile.vue'
import ProfileEdit from '../components/ProfileEdit.vue'
import ProjectCreate from '../components/ProjectCreate.vue'
import MyProjects from '../components/MyProjects.vue'
import Project from '../components/Project.vue'
import Search from '../components/Search.vue'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Home
  },
  {
    path: '/login',
    component: Login
  },
  {
    path: '/signup',
    component: Signup
  },
  {
    path: '/dashboard',
    component: Dashboard
  },
  {
    path: '/profile',
    component: Profile
  },
  {
    path: '/profile-edit',
    component: ProfileEdit
  },
  {
    path: '/project-create',
    component: ProjectCreate
  },
  {
    path: '/my-projects',
    component: MyProjects
  },
  {
    path: '/project/:id',
    component: Project
  },
  {
    path: '/search/:query',
    component: Search
  }
]

// eslint-disable-next-line no-new
const router = new VueRouter({
  routes
})

export default router
