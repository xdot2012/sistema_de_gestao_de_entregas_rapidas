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
          v-for="item in allOrders"
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
  name: 'Painel',
  computed: mapGetters(['allOrders']),

  data() {
    return {
      desserts: [
        {
          id: 1,
          cliente: 'Maria',
          status: 1,
          pedido: 1,
        },
        {
          id: 2,
          cliente: 'Pedrin',
          status: 1,
          pedido: 1,
        },
        {
          id: 3,
          cliente: 'Sebastião',
          status: 1,
          pedido: 1,
        },
      ],
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
