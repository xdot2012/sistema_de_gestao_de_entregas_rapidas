import Vue from 'vue';
import axios from 'axios';
import VueRouter from 'vue-router';
import { VueMaskDirective } from 'v-mask';
import App from './App.vue';

import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';

Vue.directive('mask', VueMaskDirective);
Vue.config.productionTip = false;
Vue.use(VueRouter);

axios.defaults.baseURL = 'http://localhost:8000';

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
