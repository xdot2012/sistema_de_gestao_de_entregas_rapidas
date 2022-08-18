const message = {
  state: () => ({
    text: null,
    success: false,
    error: false,
  }),

  getters: {
    getAlertType: (state) => (state.success ? 'success' : 'error'),
    showSuccess: (state) => state.success,
    showError: (state) => state.error,
    getMessage: (state) => state.text,
  },

  actions: {
    alertSuccess({ commit }, text) {
      commit('CLEAR_MESSAGE');
      commit('SET_SUCCESS', text);
    },

    alertError({ commit }, text) {
      commit('CLEAR_MESSAGE');
      commit('SET_ERROR', text);
    },

    alertClear({ commit }) {
      commit('CLEAR_MESSAGE');
    },
  },

  mutations: {
    CLEAR_MESSAGE(state) {
      state.success = false;
      state.text = null;
    },

    SET_ERROR(state, text) {
      state.text = text;
      state.error = true;
    },

    SET_SUCCESS(state, text) {
      state.error = false;
      state.text = text;
      state.success = true;
    },
  },
};

export default message;
