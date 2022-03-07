<template>
    <v-simple-table>
    <template v-slot:default>
      <thead class="table-head">
        <tr>
          <th class="text-left">
            ENTREGADOR
          </th>
          <th class="text-left">
            STATUS
          </th>
          <th class="text-left">
            SAÍDA
          </th>
        </tr>
      </thead>
      <tbody class="table-body">
        <tr
          v-for="item in getAllDeliveryman"
          :key="item.id"
        >
          <td>{{ item.name }}</td>
          <td>{{ item.status }}</td>
          <td>{{ item.saida }}</td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>

</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'TabelaEntregadores',
  computed: mapGetters(['getAllDeliveryman']),
  beforeCreate() {
    this.$store.dispatch('getDeliveryman');
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
