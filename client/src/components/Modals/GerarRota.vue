<template>
  <v-dialog>
      <template v-slot:activator="{ on, attrs }">
        <v-btn class="flex-fill mx-2"
          x-large
          color="primary"
          v-bind="attrs" v-on="on">Gerar Rota</v-btn>
      </template>

      <template v-slot:default="dialog">
        <v-card class="pa-8 d-flex flex-column" width="100vw" Resumo min-height="90vh">
          <v-card-title class="d-flex">
              <div class="text-h5">Gerar Rota</div>
              <v-spacer />
              <v-btn icon text @click="dialog.value = false">
                <v-icon>mdi-close</v-icon>
              </v-btn>
          </v-card-title>

          <v-card-text class="flex-fill">
            <selecao-entregador-form v-if="!etapaPedido" />
            <selecao-pedidos-form v-else-if="etapaPedido==1" />
            <rota-gerada v-else-if="etapaPedido==2" />
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
            <div v-else>
              <v-btn
                class="mr-5"
                x-large
                color="primary"
                @click="imprimeRota()">
                Imprimir Rota</v-btn>
              <v-btn
                x-large
                color="primary"
                @click="dialog.value = finalizarPedido()">
                Finalizar Pedido</v-btn>
            </div>
          </v-card-actions>
        </v-card>
      </template>
  </v-dialog>
</template>

<script>
import RotaGerada from '../Forms/RotaGerada.vue';
import SelecaoEntregadorForm from '../Forms/SelecaoEntregadorForm.vue';
import SelecaoPedidosForm from '../Forms/SelecaoPedidosForm.vue';

export default {
  components: {
    SelecaoEntregadorForm,
    SelecaoPedidosForm,
    RotaGerada,
  },
  name: 'GerarRota',
  data: () => ({
    etapaPedido: 0,
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
    imprimeRota() {
      return false;
    },
  },
};
</script>

<style>
</style>
