import '@babel/polyfill'
import Vue from 'vue'
import './plugins/bootstrap-vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

Vue.config.productionTip = false

const axiosConfig = {
	baseURL: 'http://127.0.0.1:8000/api/v1'
};
Vue.prototype.$axios = axios.create(axiosConfig);

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
