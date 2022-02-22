import Vue from 'vue';
import Vuex from 'vuex';

// modules
import message from './modules/messages';
import auth from './modules/auth';
import client from './modules/client';
import deliveryman from './modules/deliveryman';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    message,
    auth,
    client,
    deliveryman,
  },
});
