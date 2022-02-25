import authRequest from '../../requests';

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
    getClientByID: (state, id) => (state.clientList.find((item) => item.pk === id)),
    getAllClients: (state) => state.clientList,
    getAutoCompleteClientName: (state) => state.clientList.map(
      (item) => ({
        name: item.name,
        pk: item.pk,
        phone: item.phone,
        phone_format: item.phone_format,
        address: formatAddress(item),
      }),
    ),
  },

  actions: {
    getClients({ commit }) {
      authRequest.get('/api/clients/')
        .then((response) => {
          commit('RESET_CLIENTS');
          commit('ADD_CLIENT', response.data);
        });
    },
    createClient({ commit, dispatch }, formData) {
      authRequest.post('/api/clients/', formData.client)
        .then((response) => {
          commit('ADD_CLIENT', [response.data]);
          dispatch('alertSuccess', { non_field_errors: ['Cliente Adicionado com Sucesso.'] });
          formData.callback(response.data.pk, response.data);
        })
        .catch((err) => {
          console.log(err);
          if (err.response?.data) {
            console.log('err.response.data');
            console.log(err.response.data);
            dispatch('alertError', err.response.data);
          } else (dispatch('alertError', err));
        });
    },
    updateClient({ commit, dispatch }, formData) {
      console.log(formData);
      authRequest.put(`/api/clients/${formData.clientID}/`, formData.client)
        .then((response) => {
          commit('REMOVE_CLIENT', formData.clientID);
          commit('ADD_CLIENT', [response.data]);
          dispatch('alertSuccess', { non_field_errors: ['Cliente Alterado com Sucesso.'] });
          formData.callback();
        })
        .catch((err) => {
          console.log(err);
          if (err.response?.data) {
            dispatch('alertError', err.response.data);
          } else (dispatch('alertError', { non_field_errors: [err] }));
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
          console.log(err);
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
    ADD_CLIENT(state, payload) {
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
