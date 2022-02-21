import authRequest from '../../variables';

function formatAddress(obj) {
  let address = `Rua/Av ${obj.street} nº${obj.number}, Bairro ${obj.district} - ${obj.city_name}/${obj.state_name}.\nCEP: ${obj.code};\n`;
  if (obj.reference) {
    address += `Referência: ${obj.reference}`;
  }
  return address;
}

const client = {
  state: () => ({
    client: null,
    clientList: [],
  }),

  getters: {
    getAllClients: (state) => state.clientList,
    getAutoCompleteClientName: (state) => state.clientList.map(
      (item) => ({
        name: item.name,
        pk: item.pk,
        phone: item.phone,
        address: formatAddress(item),
      }),
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
    updateClient({ commit, dispatch }, formData) {
      console.log(formData);
      authRequest.put(`/api/clients/${formData.clientID}/`, formData.client)
        .then((response) => {
          commit('UPDATE_CLIENT', [response.data]);
          dispatch('alertSuccess', { non_field_errors: ['Cliente Alterado com Sucesso.'] });
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
    UPDATE_CLIENT(state, payload) {
      this.REMOVE_CLIENT(state, payload);
      this.ADD_CLIENTS(state, [payload]);
    },
  },
};

export default client;
