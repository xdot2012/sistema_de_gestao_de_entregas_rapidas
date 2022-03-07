import authRequest from '../../requests';

const order = {
  state: () => ({
    orderList: [],
    orderHistory: [],
  }),

  getters: {
    activeOrders: (state) => state.orderList,
    allOrders: (state) => state.orderHistory,
  },

  actions: {
    getOrders({ commit, dispatch }) {
      authRequest.get('/api/orders/')
        .then((response) => {
          commit('RESET_ORDERS');
          commit('ADD_ORDER', response.data);
        })
        .catch((err) => {
          console.log(err);
          if (err.response?.data) {
            console.log(err.response.data);
            dispatch('alertError', err.response.data);
          } else (dispatch('alertError', err));
        });
    },

    getHistory({ commit, dispatch }) {
      authRequest.get('/api/orders/history/')
        .then((response) => {
          commit('RESET_HISTORY');
          commit('ADD_HISTORY', response.data);
        })
        .catch((err) => {
          console.log(err);
          if (err.response?.data) {
            console.log(err.response.data);
            dispatch('alertError', err.response.data);
          } else (dispatch('alertError', err));
        });
    },
    createOrder({ commit, dispatch }, formData) {
      authRequest.post('/api/orders/', formData.order)
        .then((response) => {
          commit('ADD_ORDER', [response.data]);
          dispatch('alertSuccess', { non_field_errors: ['Ordem Iniciada com Sucesso.'] });
          formData.callback(response.data.pk, response.data);
        })
        .catch((err) => {
          console.log(err);
          if (err.response?.data) {
            console.log(err.response.data);
            dispatch('alertError', err.response.data);
          } else (dispatch('alertError', err));
        });
    },
  },
  mutations: {
    RESET_ORDERS(state) {
      state.orderList = [];
    },
    ADD_ORDER(state, payload) {
      state.orderList = state.orderList.concat(payload);
    },
    RESET_HISTORY(state) {
      state.orderHistory = [];
    },
    ADD_HISTORY(state, payload) {
      state.orderHistory = state.orderHistory.concat(payload);
    },
  },
};

export default order;
