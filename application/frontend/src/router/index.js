import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from '../components/Home.vue'
import Login from '../components/Login.vue'
import Signup from '../components/Signup.vue'

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
  }
]

// eslint-disable-next-line no-new
const router = new VueRouter({
  routes
})

export default router
