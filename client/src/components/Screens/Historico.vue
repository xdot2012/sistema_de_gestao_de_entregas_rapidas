<template>
  <div class="d-flex flex-column justify-center align-center">
    <v-card class="main-card pa-5 elevation-5">
      <v-card-title class="text-h5">
        Histórico de Pedidos
        <v-spacer />
        <v-col cols="6">
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search"
            single-line
            hide-details
          ></v-text-field>
        </v-col>
      </v-card-title>
      <v-card-text class="card-body">
        <v-data-table
          :headers="headers"
          :items="allOrders"
          :items-per-page="10"
          :search="search"
        >
            <template v-slot:item.products="{ item }">
          <v-chip
            dark
            v-for="product in item.products" :key="product.pk"
          >
            x{{product.quantity}} - {{ product.name }}
          </v-chip>
        </template>
        </v-data-table>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-col cols="3">
          <buscar-pedido />
        </v-col>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

import BuscarPedido from '../Modals/BuscarPedido.vue';

export default {
  components: { BuscarPedido },
  name: 'Historico',
  computed: mapGetters(['allOrders']),
  beforeCreate() {
    this.$store.dispatch('getHistory');
  },
  data() {
    return {
      drawer: null,
      search: null,
      headers: [
        { text: '#', value: 'pk' },
        { text: 'Data', value: 'created_on' },
        { text: 'Cliente', value: 'client_name' },
        { text: 'Pedido', value: 'products' }],
    };
  },
};
</script>
