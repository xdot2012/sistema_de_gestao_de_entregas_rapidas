<template>
  <div>
    <tabela-historico />
    <buscar-pedido />
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
