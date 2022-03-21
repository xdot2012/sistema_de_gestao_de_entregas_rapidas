<template>
  <div class="d-flex flex-column fill-height" style="max-height: 90%">
    <h2 class="mt-2">Informações do Cliente</h2>
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

      <v-divider class="mt-3"></v-divider>
      <h2 class="mt-1">Endereço de Entrega</h2>

      <v-row>
        <v-autocomplete
        v-model="enderecoEntregaCidadeID"
        :items="getAllCitys"
        item-text="name"
        item-value="pk"
        dense
        filled
        label="Cidade/Estado"
        :rules="[v => !!v || 'Item is required']"
        ></v-autocomplete>
        <v-text-field
        disabled
        v-model="enderecoEntregaEstado"
        dense
        filled
        label="Estado"
        ></v-text-field>
        <v-text-field
        class="mr-3"
        style="max-width: 30%"
        label="Bairro"
        v-model="enderecoEntregaBairro"
        dense
        filled
        ></v-text-field>
      </v-row>

      <v-row>
        <v-text-field
        class="mr-3"
        label="Rua"
        v-model="enderecoEntregaRua"
        dense
        filled
        required
        :rules="[v => !!v || 'Item is required']"
        ></v-text-field>

        <v-text-field
        class="mr-3"
        style="max-width: 10%"
        label="Número"
        :rules="regraNumero"
        v-model="enderecoEntregaNumero"
        hide-details="auto"
        required
        ></v-text-field>
      </v-row>

      <v-row class="mb-10">
        <v-text-field
        class="mr-3"
        style="max-width: 25%"
        label="CEP"
        v-mask="'#####-###'"
        :rules="regraCEP"
        v-model="enderecoEntregaCEP"
        hide-details="auto"
        required
        ></v-text-field>
        <v-text-field
        class="mr-3"
        label="Referência"
        v-model="enderecoEntregaReferencia"
        hide-details="auto"
        ></v-text-field>
      </v-row>

      <v-row>
        <v-btn
          :disabled="!fullAddress()"
          color="primary"
          @click="showAddress()"
          >Buscar Endereço
          </v-btn>
      </v-row>

      <v-row v-if="showMap">
        <l-map style="height: 300px" :zoom="zoom" :center="center">
          <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
          <l-marker :lat-lng="markerLatLng"></l-marker>
        </l-map>
      </v-row>

      <v-row class="d-flex align-end justify-end fill-height">
          <v-btn
            :disabled="!valid"
            color="primary"
            x-large
            @click="validate">
              Cadastrar Cliente
          </v-btn>
      </v-row>
    </v-form>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { LMap, LTileLayer, LMarker } from 'vue2-leaflet';

import {
  regraTelefone,
  regraNomeCliente,
  regraNumero,
  regraCEP,
  regraTexto,
} from '../../regras_input';
import { formatAddressNominatin } from '../../functions';

export default {
  name: 'NovoClienteForm',
  props: ['dialog'],
  computed: mapGetters(['getAllCitys', 'findCity']),
  components: {
    LMap,
    LTileLayer,
    LMarker,
  },
  data: () => ({
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
    enderecoEntregaCidadeID: null,
    enderecoEntregaCidade: null,
    enderecoEntregaEstado: null,
    enderecoEntregaNumero: null,
    enderecoEntregaRua: null,
    enderecoEntregaBairro: null,
    enderecoEntregaCEP: null,
    enderecoEntregaReferencia: null,
    clienteID: null,
    regraNomeCliente,
    regraTelefone,
    regraNumero,
    regraCEP,
    regraTexto,
  }),
  methods: {
    setMapMarker(pointData) {
      this.markerLatLng = [pointData.latitude, pointData.longitude];
      this.center = [pointData.latitude, pointData.longitude];
      this.zoom = 50;
      this.showMap = true;
    },
    showAddress() {
      const data = {
        street: this.enderecoEntregaRua,
        number: this.enderecoEntregaNumero,
        district: this.enderecoEntregaBairro,
        city_name: this.enderecoEntregaCidade,
        state_name: this.enderecoEntregaEstado,
        code: this.enderecoEntregaCEP,
        reference: this.enderecoEntregaReferencia,
      };
      this.$store.dispatch('getLocation', { address: formatAddressNominatin(data), callback: this.setMapMarker });
    },
    fullAddress() {
      return (this.enderecoEntregaBairro
      && this.enderecoEntregaCidade
      && this.enderecoEntregaBairro
      && this.enderecoEntregaRua
      && this.enderecoEntregaNumero
      && this.enderecoEntregaCEP);
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
      const formatPhone = this.telefoneCliente.replace(' ', '').replace('(', '').replace(')', '').replace('-', '');
      const client = {
        name: this.nomeCliente,
        phone: formatPhone,
        number: this.enderecoEntregaNumero,
        street: this.enderecoEntregaRua,
        district: this.enderecoEntregaBairro,
        code: this.enderecoEntregaCEP,
        country_name: this.enderecoEntregaPais,
        state_name: this.enderecoEntregaEstado,
        city_name: this.enderecoEntregaCidade,
        reference: this.enderecoEntregaReferencia,
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

      this.enderecoEntregaCidade = city.name;
      this.enderecoEntregaEstado = city.state;
      this.enderecoEntregaPais = city.country;
      return val;
    },
  },
};
</script>
