import Vue from 'vue';
import axios from 'axios';
import VueRouter from 'vue-router';
import { VueMaskDirective } from 'v-mask';
import L from 'leaflet';
import App from './App.vue';

import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';
import 'leaflet/dist/leaflet.css';

Vue.directive('mask', VueMaskDirective);
Vue.config.productionTip = false;
Vue.use(VueRouter);

// Leaflet Iconfix
/* eslint-disable no-underscore-dangle */
delete L.Icon.Default.prototype._getIconUrl;

const iconRetinaUrl = require('leaflet/dist/images/marker-icon-2x.png');
const iconUrl = require('leaflet/dist/images/marker-icon.png');
const shadowUrl = require('leaflet/dist/images/marker-shadow.png');

L.Icon.Default.mergeOptions({
  iconRetinaUrl,
  iconUrl,
  shadowUrl,
});
/* eslint-enable no-underscore-dangle */

axios.defaults.baseURL = 'http://localhost:80';

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
