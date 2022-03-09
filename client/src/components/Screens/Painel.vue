<template>
  <div>
    <div class="mt-5 d-flex flex-column justify-content-center align-items-center">
      <v-card class="card-painel">
        <tabela-pedidos-ativos></tabela-pedidos-ativos>
        <v-card-actions>
          <v-spacer></v-spacer>
          <div>
          <v-btn @click="test">test</v-btn>
            <novo-pedido></novo-pedido>
          </div>
        </v-card-actions>
      </v-card>

      <v-card class="card-painel mt-10">
        <tabela-entregadores></tabela-entregadores>
        <v-card-actions>
          <v-spacer></v-spacer>
          <div>
            <gerar-rota></gerar-rota>
          </div>
        </v-card-actions>
      </v-card>

    </div>
    <modal-sucesso ref="success" :dialog="dialog"/>
  </div>

</template>

<script>
import { dateTimeToDate, getDifInMinutes } from '../../functions';
import TabelaPedidosAtivos from '../Tabelas/TabelaPedidosAtivos.vue';
import TabelaEntregadores from '../Tabelas/TabelaEntregadores.vue';
import NovoPedido from '../Modals/NovoPedido.vue';
import GerarRota from '../Modals/GerarRota.vue';
import ModalSucesso from '../Modals/ModalSucesso.vue';

export default {
  components: {
    TabelaPedidosAtivos,
    TabelaEntregadores,
    NovoPedido,
    GerarRota,
    ModalSucesso,
  },
  name: 'Painel',
  data() {
    return {
      dialog: false,
      overlay: false,
    };
  },
  methods: {
    test() {
      const orders = this.$store.getters.activeOrders;
      const lateOrders = orders.filter(
        (item) => {
          console.log(getDifInMinutes(Date.now(), dateTimeToDate(item.created_on)));
          return dateTimeToDate(item.created_on) - Date.now() <= 10;
        },
      );
      console.log(lateOrders);
    },
  },
};
</script>

<style scoped>
  .card-painel {
    width: 95vw;
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
</style>
