import Vue from 'vue';

import authRequest from '../../requests';
import {
  isLate,
  isWarn,
  getPriority,
  isOut,
  isWaiting,
} from '../../functions';

const order = {
  state: () => ({
    orderList: [],
    orderHistory: [],
  }),

  getters: {
    activeOrders: (state) => state.orderList,
    waitingOrders: (state) => state.orderList.filter((item) => isWaiting(item)),
    allOrders: (state) => state.orderHistory,
    inRouteOrders: (state) => state.orderList.filter((item) => isOut(item)),
    lateOrders: (state) => state.orderList.filter(
      (i) => !isOut(i) && isLate(i.created_on),
    ),
    warnOrders: (state) => state.orderList.filter(
      (i) => !isOut(i) && isWarn(i.created_on),
    ),
    ordersWithPriority: (state) => state.orderList.filter(
      (item) => isWaiting(item),
    ).filter((item) => getPriority(item)),
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

    deliverOrders({ commit, dispatch }, formData) {
      authRequest.post('/api/orders/deliver/', { orders: formData.orders })
        .then((response) => {
          console.log('update!');
          commit('UPDATE_ORDERS', response.data);
          dispatch('alertSuccess', { non_field_errors: ['Ordens foram atualizadas'] });
          formData.callback();
        })
        .catch((err) => {
          console.log(err);
          if (err.response?.data) {
            console.log(err.response.data);
            dispatch('alertError', err.response.data);
          } else (dispatch('alertError', err));
        });
    },

    cancelOrders({ commit, dispatch }, formData) {
      authRequest.post('/api/orders/cancel/', { orders: formData.orders })
        .then((response) => {
          commit('REMOVE_ORDERS', response.data);
          dispatch('alertSuccess', { non_field_errors: ['Ordens foram atualizadas'] });
          formData.callback();
        })
        .catch((err) => {
          console.log(err);
          if (err.response?.data) {
            console.log(err.response.data);
            dispatch('alertError', err.response.data);
          } else (dispatch('alertError', err));
        });
    },
    finishOrders({ commit, dispatch }, formData) {
      authRequest.post('/api/orders/finish/', { orders: formData.orders })
        .then((response) => {
          commit('REMOVE_ORDERS', response.data);
          dispatch('alertSuccess', { non_field_errors: ['Ordens foram atualizadas'] });
          formData.callback();
        })
        .catch((err) => {
          console.log(err);
          if (err.response?.data) {
            console.log(err.response.data);
            dispatch('alertError', err.response.data);
          } else (dispatch('alertError', err));
        });
    },
    resetOrders({ commit, dispatch }, formData) {
      authRequest.post('/api/orders/reset/', { orders: formData.orders })
        .then((response) => {
          commit('UPDATE_ORDERS', response.data);
          dispatch('alertSuccess', { non_field_errors: ['Ordens foram atualizadas'] });
          formData.callback();
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
    UPDATE_ORDERS(state, payload) {
      payload.map((obj) => {
        const index = state.orderList.findIndex((old) => old.pk === obj.pk);
        if (index !== -1) {
          Vue.set(state.orderList, index, obj);
        } else {
          console.log('ERRO, ORDEM NÃO ENCONTRADA!');
        }
        return obj;
      });
    },
    REMOVE_ORDERS(state, payload) {
      payload.map((obj) => {
        const index = state.orderList.findIndex((old) => old.pk === obj.pk);
        if (index !== -1) {
          state.orderList.splice(index, 1);
        } else {
          console.log('ERRO, ORDEM NÃO ENCONTRADA!');
        }
        return obj;
      });
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
