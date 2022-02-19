<template>
  <div>
    <cliente-configuracoes-form />
    <entregador-configuracoes-form />
  </div>
</template>

<script>
import ClienteConfiguracoesForm from '../Forms/ClienteConfiguracoesForm.vue';
import EntregadorConfiguracoesForm from '../Forms/EntregadorConfiguracoesForm.vue';

export default {
  components: { ClienteConfiguracoesForm, EntregadorConfiguracoesForm },
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
