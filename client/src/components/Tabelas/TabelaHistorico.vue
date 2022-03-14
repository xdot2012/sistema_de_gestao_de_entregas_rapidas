<template>
  <v-card>
    <v-card-title>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
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
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'TabelaHistórico',
  computed: mapGetters(['allOrders']),
  beforeCreate() {
    this.$store.dispatch('getHistory');
  },
  data() {
    return {
      search: null,
      headers: [
        { text: '#', value: 'pk' },
        { text: 'Data', value: 'created_on' },
        { text: 'Cliente', value: 'client_name' },
        { text: 'Pedido', value: 'products' }],
    };
  },
  methods: {
    getColor() {
      return 'green';
    },
  },
};
</script>
