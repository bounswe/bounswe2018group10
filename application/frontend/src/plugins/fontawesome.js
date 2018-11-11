import Vue from 'vue'

import { library } from '@fortawesome/fontawesome-svg-core'
import { faEnvelope, faUser, faLock, faUserEdit, faPlus, faSignOutAlt, faSave, faSearch } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faEnvelope, faUser, faLock, faUserEdit, faPlus, faSignOutAlt, faSave, faSearch)

Vue.component('font-awesome-icon', FontAwesomeIcon)
