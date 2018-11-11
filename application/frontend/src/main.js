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
	baseURL: `${process.env.VUE_APP_BACKEND_BASE_URL}/api/v1`
};
Vue.prototype.$axios = axios.create(axiosConfig);

Vue.filter('shortDescription', function (value) {
  if (!value) return "";
  const limit = 200;
  if(value.length > limit){
    return value.slice(0,limit) + "...";
  }else{
    return value;
  }
})

new Vue({
  data: {
    user_id: 0,
    role: localStorage.getItem('role') || '',
  },
  router,
  render: h => h(App)
}).$mount('#app')
