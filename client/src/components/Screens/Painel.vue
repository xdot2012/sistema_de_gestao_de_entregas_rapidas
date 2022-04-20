<template>
  <div>
      <div class="mt-5 d-flex flex-column justify-center align-center">
      <v-card class="card-painel pa-5 elevation-5">
        <v-card-title class="d-flex justify-center text-h4">
          Pedidos Ativos
        </v-card-title>
        <v-card-text class="card-body">
          <div
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
            </template>
          </v-simple-table>
        </v-card-text>
        <v-card-actions class="d-flex align-end">
          <v-col cols="12">
            <v-row>
              <v-col cols="3">
                <atualizar-pedido :orders="selectedOrders" :updateTable="atualizarPedidos"/>
              </v-col>
              <v-spacer />
              <v-col cols="4">
               <gerar-rota></gerar-rota>
              </v-col>
              <v-col cols="4">
                <novo-pedido></novo-pedido>
              </v-col>
            </v-row>
          </v-col>
        </v-card-actions>
      </v-card>

      <!-- <v-card class="card-painel mt-10">
        <tabela-entregadores></tabela-entregadores>
        <v-card-actions>
          <v-spacer></v-spacer>
          <div>
          </div>
        </v-card-actions>
      </v-card> -->

    </div>
    <modal-sucesso ref="success" :dialog="dialog"/>
  </div>

</template>

<script>
import { mapGetters } from 'vuex';

// import TabelaEntregadores from '../Tabelas/TabelaEntregadores.vue';
import NovoPedido from '../Modals/NovoPedido.vue';
import GerarRota from '../Modals/GerarRota.vue';
import ModalSucesso from '../Modals/ModalSucesso.vue';

import {
  isOut,
  isLate,
  isWarn,
} from '../../functions';
import AtualizarPedido from '../Modals/AtualizarPedido.vue';

export default {
  components: {
    // TabelaEntregadores,
    NovoPedido,
    GerarRota,
    ModalSucesso,
    AtualizarPedido,
  },
  name: 'Painel',
  beforeCreate() {
    this.$store.dispatch('getOrders');
  },
  computed: mapGetters(['activeOrders']),
  data() {
    return {
      dialog: false,
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

<style scoped>
  .card-painel {
    width: 95vw;
    min-height: 85vh;
  }

  .botao-painel {
    max-width: 25vw;
    width: 25%;
    margin-left: auto;
  }

  .modal-painel {
    width:80vw;
    height: 80vh;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
  }

  .modal-painel-body {
    flex-grow: fill;
  }

  .table-body {
    color:black;
    background-color: white;
  }
</style>
