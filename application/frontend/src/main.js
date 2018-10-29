import '@babel/polyfill'
import Vue from 'vue'
import './plugins/bootstrap-vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import VoerroTagsInput from '@voerro/vue-tagsinput'

Vue.component('tags-input', VoerroTagsInput);

Vue.config.productionTip = false

const axiosConfig = {
	baseURL: 'http://127.0.0.1:8000/api/v1'
};
Vue.prototype.$axios = axios.create(axiosConfig);

new Vue({
  data: {
    user_id: 0,
    role: localStorage.getItem('role') || '',
  },
  router,
  render: h => h(App)
}).$mount('#app')
