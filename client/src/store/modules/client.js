import authRequest from '../../variables';

const client = {
  state: () => ({
    client: null,
  }),

  getters: {
  },

  actions: {
    createClient({ commit, dispatch }, formData) {
      authRequest.post('/api/clients/', formData.client)
        .then((response) => {
          commit('CREATE_CLIENT', response.data);
          dispatch('alertSuccess', { non_field_errors: ['Cliente Adicionado com Sucesso.'] });
          formData.callback();
        })
        .catch((err) => {
          if (err.response?.data) {
            dispatch('alertError', err.response.data);
          } else (dispatch('alertError', err));
        });
    },
  },

  mutations: {
    CREATE_CLIENT(state, data) {
      state.client = data;
    },
  },
};

export default client;
