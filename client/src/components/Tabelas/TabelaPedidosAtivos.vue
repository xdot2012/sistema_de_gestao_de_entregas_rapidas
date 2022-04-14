<template>
    <div>
      <div
        class="pa-5 d-flex justify-center"
        v-if="activeOrders.length==0">
        <h2 class="">
          Nenhum Pedido Encontrado
        </h2>
      </div>
      <v-simple-table  v-else>
      <template v-slot:default>
        <thead class="table-head">
          <tr>
            <th class="text-left">#</th>
            <th class="text-left">CLIENTE</th>
            <th class="text-left">PEDIDO</th>
            <th class="text-left">SITUAÇÃO</th>
            <th class="text-left">SELEÇÃO</th>
          </tr>
        </thead>
        <tbody class="table-body">
          <tr
            v-for="item in activeOrders"
            :key="item.key"
          >
            <td>{{ item.pk }}</td>
            <td>{{ item.client_name }}</td>
            <td>
              <div v-for="product in item.products" :key="product.pk">
                x{{product.quantity}} {{product.name}}
              </div>
            </td>
            <td>
              <div v-if="isOut(item)">
                <v-icon color="success">mdi-motorbike</v-icon>
              </div>
              <div v-else-if="isLate(item.created_on)">
                <v-icon color="error">mdi-clock</v-icon>
              </div>
              <div v-else>
                <v-icon color="success">mdi-clock</v-icon>
              </div>
            </td>
            <td>
              <v-checkbox v-model="selectedOrders" :value="item"></v-checkbox>
            </td>
          </tr>
        </tbody>
        <tfoot>
          <atualizar-pedido :orders="selectedOrders" :updateTable="atualizarPedidos"/>
        </tfoot>
      </template>
    </v-simple-table>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import {
  isOut,
  isLate,
  isWarn,
} from '../../functions';
import AtualizarPedido from '../Modals/AtualizarPedido.vue';

export default {
  components: { AtualizarPedido },
  name: 'TabelaPedidosAtivos',
  computed: mapGetters(['activeOrders']),

  beforeCreate() {
    this.$store.dispatch('getOrders');
  },
  data() {
    return {
      isOut,
      isLate,
      isWarn,
      selectedOrders: [],
    };
  },
  methods: {
    openDialog() {

    },
    atualizarPedidos() {
      this.selectedOrders = [];
    },
  },
};
</script>

<style>
  .table-body {
    color:black;
    background-color: white;
  }
</style>
