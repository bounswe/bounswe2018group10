import Vue from 'vue'

import { library } from '@fortawesome/fontawesome-svg-core'
import {
    faEnvelope,
    faUser,
    faLock,
    faUserEdit,
    faPlus,
    faSignOutAlt,
    faSave,
    faSearch,
    faLayerGroup,
    faTags,
    faMoneyBill,
    faCalendarAlt,
    faClock,
    faMapMarkerAlt,
    faAlignLeft,
    faTextHeight,
    faUsers,
    faHandshake,
    faBolt,
    faFileImport,
    faListUl,
    faFileMedicalAlt,
    faFile,
    faUserCog,
    faCheck
} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faEnvelope,
    faUser,
    faLock,
    faUserEdit,
    faPlus,
    faSignOutAlt,
    faSave,
    faSearch,
    faLayerGroup,
    faTags,
    faMoneyBill,
    faCalendarAlt,
    faClock,
    faMapMarkerAlt,
    faAlignLeft,
    faTextHeight,
    faUsers,
    faHandshake,
    faBolt,
    faFileImport,
    faListUl,
    faFileMedicalAlt,
    faFile,
    faUserCog,
    faCheck)

Vue.component('font-awesome-icon', FontAwesomeIcon)
