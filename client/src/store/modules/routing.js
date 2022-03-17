import authRequest from '../../requests';

const routing = {
  state: () => ({
    citys: [],
  }),

  getters: {
    getAllCitys: (state) => state.citys,
  },

  actions: {
    getCitys({ commit, dispatch }) {
      authRequest.get('/api/branches/')
        .then((response) => {
          commit('RESET_CITYS');
          commit('ADD_CITY', response.data);
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
  },
};

export default routing;
