<template>
  <div>
    <v-row>
      <v-autocomplete
      v-model="enderecoEntregaCidadeID"
      :items="getAllCitys"
      item-text="city_name"
      item-value="pk"
      dense
      filled
      label="Cidade/Estado"
      :rules="[v => !!v || 'Item is required']"
      ></v-autocomplete>
      <v-text-field
      disabled
      v-model="address.state_name"
      dense
      filled
      label="Estado"
      ></v-text-field>
      <v-text-field
      class="mr-3"
      style="max-width: 30%"
      label="Bairro"
      v-model="address.district"
      dense
      filled
      ></v-text-field>
    </v-row>

    <v-row>
      <v-text-field
      class="mr-3"
      label="Rua"
      v-model="address.street"
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
      v-model="address.number"
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
      v-model="address.code"
      hide-details="auto"
      required
      ></v-text-field>
      <v-text-field
      class="mr-3"
      label="Referência"
      v-model="address.reference"
      hide-details="auto"
      ></v-text-field>
    </v-row>

    <v-row>
      <v-btn
        :disabled="!fullAddress()"
        color="primary"
        @click="showAddress()"
        >Validar Endereço
        </v-btn>
    </v-row>

    <v-row v-if="showMap">
      <l-map style="height: 300px" :zoom="zoom" :center="center">
        <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
        <l-marker :lat-lng="markerLatLng"></l-marker>
      </l-map>
    </v-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { LMap, LTileLayer, LMarker } from 'vue2-leaflet';

import {
  regraNumero,
  regraCEP,
  regraTexto,
} from '../../regras_input';
import { formatAddressNominatin } from '../../functions';

export default {
  name: 'NovoEndereçoForm',
  props: ['onFinish'],
  computed: mapGetters(['getAllCitys', 'findCity']),
  components: {
    LMap,
    LTileLayer,
    LMarker,
  },
  beforeCreate() {
    this.$store.dispatch('getCitys');
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
    },
    enderecoEntregaCidadeID: null,
    clienteID: null,
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
      this.address.latitude = pointData.latitude;
      this.address.longitude = pointData.longitude;
      this.address.altitude = pointData.altitude;
      this.onFinish(this.address);
    },
    showAddress() {
      this.$store.dispatch('getLocation', { address: formatAddressNominatin(this.address), callback: this.setMapMarker });
    },
    fullAddress() {
      let response = false;
      if (this.address.street
        && this.address.number
        && this.address.district
        && this.address.city_name
        && this.address.state_name
        && this.address.country_name
        && this.address.code) {
        response = true;
      }
      return response;
    },
  },
  watch: {
    enderecoEntregaCidadeID: function onChange(val) {
      if (!val) {
        return null;
      }
      const city = this.$store.getters.getAllCitys
        .find((item) => item.pk === val);

      this.address.city_name = city.city_name;
      this.address.state_name = city.state_name;
      this.address.country_name = city.country_name;
      return val;
    },
  },
};
</script>
