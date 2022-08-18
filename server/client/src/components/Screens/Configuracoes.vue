<template>
  <div>
    <crud-cliente />
    <!-- <crud-entregador /> -->
  </div>
</template>

<script>
import CrudCliente from '../CrudCliente.vue';
// import CrudEntregador from '../CrudEntregador.vue';

export default {
  components: {
    CrudCliente,
    // CrudEntregador,
  },
  name: 'Configuracoes',
  beforeCreate() {
    this.$store.dispatch('getClients');
  },
  data() {
    return {
      tab: null,
      text: 'Beluga',
    };
  },
};
</script>

<style>
</style>
