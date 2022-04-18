<template>
  <div>
    <tabela-historico />
    <div class="d-flex justify-end">
      <v-col cols="3">
        <buscar-pedido />
      </v-col>
    </div>
  </div>
</template>

<script>
import BuscarPedido from '../Modals/BuscarPedido.vue';
import TabelaHistorico from '../Tabelas/TabelaHistorico.vue';

export default {
  components: { TabelaHistorico, BuscarPedido },
  name: 'Historico',
  data() {
    return {
      drawer: null,
    };
  },
};
</script>
