<template>
    <v-simple-table >
    <template v-slot:default>
      <thead class="table-head">
        <tr>
          <th class="text-left">#</th>
          <th class="text-left">CLIENTE</th>
          <th class="text-left">PEDIDO</th>
        </tr>
      </thead>
      <tbody class="table-body">
        <tr
          v-for="item in activeOrders"
          :key="item.id"
        >
          <td>{{ item.pk }}</td>
          <td>{{ item.client_name }}</td>
          <td>
            <div v-for="product in item.products" :key="product.pk">
              x{{product.quantity}} {{product.name}}
            </div>
          </td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>

</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'TabelaPedidosAtivos',
  computed: mapGetters(['activeOrders']),

  beforeCreate() {
    this.$store.dispatch('getOrders');
  },
  data() {
    return {
    };
  },
};
</script>

<style>
  .table-body {
    color:black;
    background-color: white;
  }
</style>
