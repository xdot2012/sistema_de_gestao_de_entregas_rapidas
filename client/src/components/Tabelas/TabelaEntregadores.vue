<template>
    <v-simple-table dark>
    <template v-slot:default>
      <thead class="primary table-head">
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
          v-for="item in desserts"
          :key="item.id"
        >
          <td>{{ item.nome }}</td>
          <td>{{ item.status }}</td>
          <td>{{ item.saida }}</td>
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
          nome: 'Maria',
          status: 1,
          saida: 1,
        },
        {
          id: 2,
          nome: 'Leopoldo',
          status: 1,
          saida: 1,
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
