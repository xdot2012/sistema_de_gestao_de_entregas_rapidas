import authRequest from '../../requests';

const deliveryman = {
  state: () => ({
    all: [],
  }),

  getters: {
    getAllDeliveryman: (state) => state.all,
  },

  actions: {
    getDeliveryman({ commit }) {
      authRequest.get('/api/deliveryman/')
        .then((response) => {
          commit('RESET_DELIVERYMANS');
          commit('ADD_DELIVERYMAN', response.data);
        });
    },
    createDeliveryman({ commit, dispatch }, formData) {
      authRequest.post('/api/deliveryman/', formData.deliveryman)
        .then((response) => {
          commit('ADD_DELIVERYMAN', [response.data]);
          dispatch('alertSuccess', { non_field_errors: ['Entregador Adicionado com Sucesso.'] });
          formData.callback();
        })
        .catch((err) => {
          if (err.response?.data) {
            dispatch('alertError', err.response.data);
          } else (dispatch('alertError', err));
        });
    },
    updateDeliveryman({ commit, dispatch }, formData) {
      authRequest.put(`/api/deliveryman/${formData.deliverymanID}/`, formData.deliveryman)
        .then((response) => {
          commit('REMOVE_DELIVERYMAN', formData.deliverymanID);
          commit('ADD_DELIVERYMAN', [response.data]);
          dispatch('alertSuccess', { non_field_errors: ['Entregador Alterado com Sucesso.'] });
          formData.callback();
        })
        .catch((err) => {
          if (err.response?.data) {
            dispatch('alertError', err.response.data);
          } else (dispatch('alertError', { non_field_errors: [err] }));
        });
    },
    deleteDeliveryman({ commit, dispatch }, formData) {
      authRequest.delete(`/api/deliveryman/${formData.deliverymanID}/`)
        .then(() => {
          commit('REMOVE_DELIVERYMAN', formData.deliverymanID);
          dispatch('alertSuccess', { non_field_errors: ['Entregador Excluído com Sucesso.'] });
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
    RESET_DELIVERYMANS(state) {
      state.all = [];
    },
    ADD_DELIVERYMAN(state, payload) {
      state.all = state.all.concat(payload);
    },
    REMOVE_DELIVERYMAN(state, payload) {
      const index = state.all.findIndex((item) => item.pk === payload);
      if (index !== -1) {
        state.all.splice(index, 1);
      } else {
        console.log('ERRO, ENTREGADOR NÃO ENCONTRADO!');
      }
    },
  },
};

export default deliveryman;
