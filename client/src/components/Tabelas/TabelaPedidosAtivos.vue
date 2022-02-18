<template>
    <v-simple-table dark>
    <template v-slot:default>
      <thead class="primary table-head">
        <tr>
          <th class="text-left">
            STATUS
          </th>
          <th class="text-left">
            CLIENTE
          </th>
          <th class="text-left">
            PEDIDO
          </th>
        </tr>
      </thead>
      <tbody class="table-body">
        <tr
          v-for="item in desserts"
          :key="item.id"
        >
          <td>{{ item.status }}</td>
          <td>{{ item.cliente }}</td>
          <td>{{ item.pedido }}</td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>

</template>

<script>
export default {
  name: 'Painel',
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
