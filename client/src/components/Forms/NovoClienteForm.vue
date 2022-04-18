<template>
  <v-col cols=12>
    <v-row><h2 class="mb-10">Informações do Cliente</h2>
    </v-row>
    <v-form
      ref="form"
      v-model="valid"
      lazy-validation>
      <v-row>
        <v-text-field class="mr-2"
        label="Nome Cliente"
        :rules="regraNomeCliente"
        v-model="nomeCliente"
        hide-details="auto"
        required
        ></v-text-field>

        <v-text-field label="Telefone do Cliente"
        :rules="regraTelefone"
        v-model="telefoneCliente"
        v-mask="'(##)#####-####'"
        hide-details="auto"
        required
        ></v-text-field>
      </v-row>

      <h2 class="mt-10">Endereço de Entrega</h2>

      <novo-endereco-form class="mt-5" :onFinish="setAddress"/>

      <v-row class="d-flex align-end justify-end fill-height">
          <v-btn
            :disabled="!valid||!hasAddress"
            color="primary"
            x-large
            @click="validate">
              Cadastrar Cliente
          </v-btn>
      </v-row>
    </v-form>
  </v-col>
</template>

<script>
import { mapGetters } from 'vuex';

import {
  regraTelefone,
  regraNomeCliente,
  regraNumero,
  regraCEP,
  regraTexto,
} from '../../regras_input';
import { formatPhone } from '../../functions';
import NovoEnderecoForm from './NovoEnderecoForm.vue';

export default {
  name: 'NovoClienteForm',
  props: ['dialog'],
  computed: mapGetters(['getAllCitys', 'findCity']),
  components: {
    NovoEnderecoForm,
  },
  data: () => ({
    formatPhone,
    showMap: false,
    overlay: false,
    url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attribution:
      '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
    zoom: 15,
    center: [-19.4307142, -44.1882217],
    markerLatLng: [-19.4307142, -44.1882217],
    valid: false,
    clienteSelecao: null,
    nomeCliente: null,
    telefoneCliente: null,
    address: {
      street: null,
      number: null,
      district: null,
      city_name: null,
      state_name: null,
      contry_name: null,
      code: null,
      reference: null,
      latitude: null,
      longitude: null,
      altitude: null,
    },
    clienteID: null,
    regraNomeCliente,
    regraTelefone,
    regraNumero,
    regraCEP,
    regraTexto,
    hasAddress: false,
  }),
  methods: {
    setAddress(data) {
      this.address = data;
      this.hasAddress = true;
    },
    fullAddress() {
      let response = false;
      if (this.address.street
        && this.address.number
        && this.address.district
        && this.address.city_name
        && this.address.state_name
        && this.address.contry_name
        && this.address.code
        && this.address.latitude
        && this.address.longitude) {
        response = true;
      }
      return response;
    },
    callback(id, data) {
      this.reset();
      this.dialog(id, data);
    },
    validate() {
      if (this.$refs.form.validate()) {
        this.criarCliente();
      }
    },
    reset() {
      this.$refs.form.reset();
    },
    resetValidation() {
      this.$refs.form.resetValidation();
    },
    criarCliente() {
      const clearPhone = this.formatPhone(this.telefoneCliente);
      const client = {
        name: this.nomeCliente,
        phone: clearPhone,
        address: this.address,
      };
      this.$store.dispatch('createClient', { client, callback: this.callback });
    },
  },
  watch: {
    enderecoEntregaCidadeID: function onChange(val) {
      if (!val) {
        return null;
      }
      const city = this.$store.getters.getAllCitys
        .find((item) => item.pk === val);

      this.enderecoEntregaCidade = city.city_name;
      this.enderecoEntregaEstado = city.city_state;
      this.enderecoEntregaPais = city.city_country;
      return val;
    },
  },
};
</script>
