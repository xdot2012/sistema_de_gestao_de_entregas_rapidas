import axios from 'axios';

const auth = {
  state: () => ({
    count: 0,
    currentUser: {
      id: null,
      email: null,
      username: null,
    },
  }),

  getters: {
  },

  actions: {
    async login({ commit, dispatch }, data) {
      await axios.post('/api/accounts/token/', data)
        .then((response) => {
          dispatch('alertSuccess', { non_field_errors: ['Success.'] });
          commit('ADD_USER', response.data);
          window.location.replace('/');
        })
        .catch((err) => {
          if (err.response?.data) {
            dispatch('alertError', err.response.data);
          } else {
            dispatch('alertError', { non_field_errors: [err] });
          }
        });
    },
    logout({ commit }) {
      const token = axios.defaults.headers.common.Authorization;
      commit('REMOVE_USER');
      window.location.replace('/auth');
      console.log(token);
    },
  },

  mutations: {
    ADD_USER(state, data) {
      state.currentUser.id = data.user_id;
      state.currentUser.email = data.email;
      state.currentUser.username = data.username;
      localStorage.setItem('token', data.token);
      axios.defaults.headers.common.Authorization = `Token ${data.token}`;
    },
    REMOVE_USER(state) {
      state.currentUser.id = null;
      state.currentUser.email = null;
      state.currentUser.username = null;
      localStorage.setItem('token', null);
      localStorage.removeItem('token');
      axios.defaults.headers.common.Authorization = null;
    },
  },
};

export default auth;
