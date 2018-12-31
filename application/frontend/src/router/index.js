import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from '../components/Home.vue'
import Login from '../components/Login.vue'
import Signup from '../components/Signup.vue'
import Dashboard from '../components/Dashboard.vue'
import Profile from '../components/Profile.vue'
import OtherProfiles from '../components/OtherProfiles.vue'
import ProfileEdit from '../components/ProfileEdit.vue'
import ProjectCreate from '../components/ProjectCreate.vue'
import MyProjects from '../components/MyProjects.vue'
import MyAcceptedProjects from '../components/MyAcceptedProjects.vue'
import AllProjects from '../components/AllProjects.vue'
import AcceptedProject from '../components/AcceptedProject.vue'
import Project from '../components/Project.vue'
import Search from '../components/Search.vue'
import Settings from '../components/Settings.vue'
import Deposit from '../components/Deposit.vue'
import MyTextAnnotations from '../components/MyTextAnnotations.vue'
import MyImageAnnotations from '../components/MyImageAnnotations.vue'


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
    path: '/profile/:id/:role?',
    component: OtherProfiles
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
    path: '/my-accepted-projects',
    component: MyAcceptedProjects
  },
  {
    path: '/all-projects',
    component: AllProjects
  },
  {
    path: '/project/:id',
    component: Project
  },
  {
    path: '/accepted-project/:id',
    component: AcceptedProject
  },
  {
    path: '/search/:query',
    component: Search
  },
  {
    path: '/settings',
    component: Settings
  },
  {
    path: '/deposit',
    component: Deposit
  },
  {
    path: '/my-text-annotations',
    component: MyTextAnnotations
  },
  {
    path: '/my-image-annotations',
    component: MyImageAnnotations
  }
]

// eslint-disable-next-line no-new
const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
