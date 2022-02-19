import authRequest from '../../variables';

const client = {
  state: () => ({
    client: null,
    clientList: [],
  }),

  getters: {
    getAllClients: (state) => state.clientList,
    getAutoCompleteClientName: (state) => state.clientList.map(
      (item) => ({ name: item.name, id: item.pk }),
    ),
  },

  actions: {
    getClients({ commit }) {
      authRequest.get('/api/clients/')
        .then((response) => {
          commit('RESET_CLIENTS');
          commit('ADD_CLIENTS', response.data);
        });
    },
    createClient({ commit, dispatch }, formData) {
      authRequest.post('/api/clients/', formData.client)
        .then((response) => {
          commit('ADD_CLIENT', [response.data]);
          dispatch('alertSuccess', { non_field_errors: ['Cliente Adicionado com Sucesso.'] });
          formData.callback();
        })
        .catch((err) => {
          if (err.response?.data) {
            dispatch('alertError', err.response.data);
          } else (dispatch('alertError', [err]));
        });
    },
    deleteClient({ commit, dispatch }, formData) {
      authRequest.delete(`/api/clients/${formData.clientID}/`)
        .then(() => {
          commit('REMOVE_CLIENT', formData.clientID);
          dispatch('alertSuccess', { non_field_errors: ['Cliente Excluído com Sucesso.'] });
          formData.callback();
        })
        .catch((err) => {
          if (err.response?.data) {
            dispatch('alertError', { non_field_errors: [err.response.data] });
          } else (dispatch('alertError', [err]));
        });
    },
  },

  mutations: {
    RESET_CLIENTS(state) {
      state.clientList = [];
    },
    ADD_CLIENTS(state, payload) {
      state.clientList = state.clientList.concat(payload);
    },
    REMOVE_CLIENT(state, payload) {
      const index = state.clientList.findIndex((item) => item.pk === payload);
      if (index !== -1) {
        state.clientList.splice(index, 1);
      } else {
        console.log('ERRO, CLIENTE NÃO ENCONTRADO!');
      }
    },
  },
};

export default client;
