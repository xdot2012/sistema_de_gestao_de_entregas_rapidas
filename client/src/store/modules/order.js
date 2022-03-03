import authRequest from '../../requests';

const order = {
  state: () => ({
    orderList: [],
  }),

  getters: {
    allOrders: (state) => state.orderList,
  },

  actions: {
    getOrders({ commit, dispatch }) {
      authRequest.get('/api/orders/')
        .then((response) => {
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
  },
};

export default order;
