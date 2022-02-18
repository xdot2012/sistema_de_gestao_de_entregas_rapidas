<template>
  <v-dialog>
      <template v-slot:activator="{ on, attrs }">
        <v-btn class="flex-fill mx-2"
          x-large
          color="primary"
          v-bind="attrs" v-on="on">Novo Pedido</v-btn>
      </template>

      <template v-slot:default="dialog">
        <v-card class="pa-8 d-flex flex-column" width="100vw" min-height="90vh">
          <v-card-title class="d-flex">
              <div class="text-h5">Novo Pedido</div>
              <v-spacer />
              <v-btn icon text @click="dialog.value = false">
                <v-icon>mdi-close</v-icon>
              </v-btn>
          </v-card-title>

          <v-card-text class="flex-fill">
            <produtos-form v-if="!etapaPedido"/>
            <cliente-form v-else-if="etapaPedido==1" />
            <entrega-form v-else-if="etapaPedido==2" />
          </v-card-text>

          <v-card-actions class="justify-end mt-auto">
            <v-btn v-if="etapaPedido>0"
              x-large
              color="primary"
              @click="voltarEtapa(etapaPedido)">Voltar</v-btn>
            <v-spacer></v-spacer>
            <v-btn v-if="etapaPedido<=1"
              x-large
              color="primary"
              @click="proximaEtapa(etapaPedido)">Próximo</v-btn>
            <v-btn v-else
              x-large
              color="primary"
              @click="dialog.value = finalizarPedido()">
              Finalizar Pedido</v-btn>
          </v-card-actions>
        </v-card>
      </template>
  </v-dialog>
</template>

<script>
import ClienteForm from '../Forms/ClienteForm.vue';
import ProdutosForm from '../Forms/ProdutosForm.vue';
import EntregaForm from '../Forms/EntregaForm.vue';

export default {
  components: {
    ClienteForm,
    ProdutosForm,
    EntregaForm,
  },
  name: 'NovoPedido',
  data: () => ({
    etapaPedido: 0,
    value: null,
    confirmaPedido: null,
  }),
  methods: {
    finalizarPedido() {
      this.etapaPedido = 0;
      this.confirmaPedido = true;
      return false;
    },
    proximaEtapa(etapaPedido) {
      this.etapaPedido = etapaPedido + 1;
    },
    voltarEtapa(etapaPedido) {
      this.etapaPedido = etapaPedido - 1;
    },
  },
};
</script>

<style>
</style>
