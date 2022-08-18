import authRequest from '../../requests';

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
        phone_format: item.phone_format,
        address: item.main_address.format,
      }),
    ),
    getAutoCompleteAddress: (state) => state.clientList.map(
      (item) => item.main_address.format,
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
            dispatch('alertError', err.response.data);
          } else (dispatch('alertError', err));
        });
    },
    updateClient({ commit, dispatch }, formData) {
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
    updateClientNamePhone({ commit, dispatch }, formData) {
      authRequest.put(`/api/clients/${formData.clientID}/name_and_phone/`, formData.client)
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
    addClientAddress({ commit, dispatch }, formData) {
      const fullAddress = Object.assign(formData.address, { client: formData.client });
      authRequest.post('/api/address/', fullAddress)
        .then((response) => {
          commit('ADD_ADDRESS', response.data);
          dispatch('alertSuccess', { non_field_errors: ['Endereço Adicionado com Sucesso.'] });
          formData.callback(response.data);
        })
        .catch((err) => {
          console.log(err);
          if (err.response?.data) {
            dispatch('alertError', { non_field_errors: [err.response.data] });
          } else (dispatch('alertError', [err]));
        });
    },
    deleteClientAddress({ commit, dispatch }, formData) {
      authRequest.delete(`/api/address/${formData.addressID}/`)
        .then(() => {
          commit('REMOVE_ADDRESS', formData);
          dispatch('alertSuccess', { non_field_errors: ['Endereço Excluído com Sucesso.'] });
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
    ADD_ADDRESS(state, payload) {
      const index = state.clientList.findIndex((item) => item.pk === payload.client);
      if (index !== -1) {
        const obj = state.clientList[index].addresses.concat([payload]);
        state.clientList[index].addresses = obj;
      } else {
        console.log('ERRO, CLIENTE NÃO ENCONTRADO!');
      }
    },
    REMOVE_ADDRESS(state, payload) {
      const index = state.clientList.findIndex((item) => item.pk === payload.clientID);
      if (index !== -1) {
        const addressIndex = state.clientList[index].addresses.findIndex(
          (item) => item.pk === payload.addressID,
        );
        if (addressIndex !== -1) state.clientList[index].addresses.splice(addressIndex, 1);
        else console.log('ERRO, ENDEREÇO NÃO ENCONTRADO');
      } else {
        console.log('ERRO, CLIENTE NÃO ENCONTRADO!');
      }
    },
  },
};

export default client;
