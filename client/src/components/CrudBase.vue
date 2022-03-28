<template>
  <v-card class="pa-8">
    <v-card-title class="d-flex">
        <div class="text-h5">Base do Sistema</div>
    </v-card-title>

    <v-card-text>
      <div v-if="editBase">
        <novo-endereco-form :onFinish="getAddress"/>
      </div>
      <div v-else>
        <v-row>{{address.format_address}}</v-row>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
import NovoEnderecoForm from './Forms/NovoEnderecoForm.vue';

export default {
  components: { NovoEnderecoForm },
  name: 'ConfiguracoesBase',
  data() {
    return {
      editBase: false,
      address: {
        street: null,
        number: null,
        district: null,
        city_name: null,
        state_name: null,
        country_name: null,
        code: null,
        reference: null,
        latitude: null,
        longitude: null,
        altitude: null,
        format_address: null,
      },
    };
  },
  methods: {
    getAddress(value) {
      this.address = value;
    },
  },
};
</script>
