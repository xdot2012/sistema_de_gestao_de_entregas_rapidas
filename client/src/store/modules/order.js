import authRequest from '../../requests';

const order = {
  state: () => ({
  }),

  getters: {
  },

  actions: {
    createOrder({ commit, dispatch }, formData) {
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
  },
};

export default order;
