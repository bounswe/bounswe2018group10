import '@babel/polyfill'
import Vue from 'vue'
import './plugins/fontawesome'
import './plugins/bootstrap-vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import VoerroTagsInput from '@voerro/vue-tagsinput'
import './mixins.js'
import * as VueGoogleMaps from 'vue2-google-maps'
import './filters.js'

Vue.use(VueGoogleMaps, {
  load: {
    key: process.env.VUE_APP_GOOGLE_MAPS_API_KEY,
    libraries: 'places', // This is required if you use the Autocomplete plugin
    //// version
    v: '3.34',
  },
 
  //// If you intend to programmatically custom event listener code
  //// (e.g. `this.$refs.gmap.$on('zoom_changed', someFunc)`)
  //// instead of going through Vue templates (e.g. `<GmapMap @zoom_changed="someFunc">`)
  //// you might need to turn this on.
  // autobindAllEvents: false,
 
  //// If you want to manually install components, e.g.
  //// import {GmapMarker} from 'vue2-google-maps/src/components/marker'
  //// Vue.component('GmapMarker', GmapMarker)
  //// then disable the following:
  // installComponents: true,
})

Vue.use(require('vue-moment'));

Vue.component('tags-input', VoerroTagsInput);

Vue.config.productionTip = false

const axiosConfig = {
	baseURL: `${process.env.VUE_APP_BACKEND_BASE_URL}/api/v1`
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
