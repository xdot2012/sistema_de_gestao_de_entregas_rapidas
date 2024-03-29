import authRequest from '../../requests';
import { getOrdersWithRouteData } from '../../functions';

const routing = {
  state: () => ({
    citys: [],
    currentPath: [],
  }),

  getters: {
    getAllCitys: (state) => state.citys,
    getPath: (state) => state.currentPath.data,
    getOrdersPathData: (state) => state.currentPath.data,
    polylineData: (state) => state.currentPath.route.full_path,
    polylineLegData: (state) => state.currentPath.route.legs,
    polylineStepData: (state) => state.currentPath.route.legs.steps,
    ordersInPath: (state) => getOrdersWithRouteData(state.currentPath.data),
  },

  actions: {
    getCitys({ commit, dispatch }) {
      authRequest.get('/api/branches/')
        .then((response) => {
          commit('RESET_CITYS');
          commit('ADD_CITY', response.data);
        })
        .catch((err) => {
          if (err.response?.data) {
            console.log(err.response.data);
            dispatch('alertError', err.response.data);
          } else (dispatch('alertError', err));
        });
    },
    getLocation({ dispatch }, formData) {
      authRequest.post('/api/location/', { address: formData.address })
        .then((response) => {
          formData.callback(response.data);
        })
        .catch((err) => {
          if (err.response?.data) {
            console.log(err.response.data);
            dispatch('alertError', err.response.data);
          } else (dispatch('alertError', err));
        });
    },
    generatePath({ commit, dispatch }, formData) {
      authRequest.post('/api/pathfinder/', { orders: formData.orders })
        .then((response) => {
          commit('RESET_PATH');
          commit('ADD_PATH', response.data);
          dispatch('alertSuccess', { non_field_errors: ['Rota gerada com Sucesso'] });
          formData.callback(formData.orders);
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
    RESET_CITYS(state) {
      state.citys = [];
    },
    ADD_CITY(state, payload) {
      state.citys = state.citys.concat(payload);
    },
    RESET_PATH(state) {
      state.currentPath = [];
    },
    ADD_PATH(state, payload) {
      state.currentPath = payload;
    },
  },
};

export default routing;
