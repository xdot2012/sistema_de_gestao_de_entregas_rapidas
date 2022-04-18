<template>
  <v-dialog width="50%" >
      <template v-slot:activator="{ on, attrs }">
        <v-btn class="ma-2 mr-5"
          :disabled="orders.length==0"
          color="accent"
          v-bind="attrs" v-on="on">Atualizar Pedidos Selecionados</v-btn>
      </template>

      <template v-slot:default="dialog">
        <v-card class=" pa-8" >
          <v-card-title class="d-flex ">
            Atualizar Status de Pedido(s)
          </v-card-title>

          <v-card-text>
            <v-select
              v-model="value"
              :items="items"
              filled
            ></v-select>
          </v-card-text>

          <v-card-actions class="justify-end">
            <v-btn text @click="dialog.value = false">Fechar</v-btn>
            <v-spacer />
            <v-btn
              color="primary"
              :disabled="!value"
              @click="dialog.value = atualizarPedidos()">Atualizar</v-btn>
          </v-card-actions>
        </v-card>
      </template>
  </v-dialog>
</template>

<script>

export default {
  name: 'AtualizarPedido',
  props: ['orders', 'updateTable'],
  data() {
    return {
      dialog: null,
      value: null,
      items: [
        'Saiu Para Entrega',
        'Entregue',
        'Em Aguardo',
        'Cancelado',
      ],
      changeFunc: {
        'Saiu Para Entrega': 'deliverOrders',
        Entregue: 'finishOrders',
        'Em Aguardo': 'resetOrders',
        Cancelado: 'cancelOrders',
      },
    };
  },
  methods: {
    changeOrder() {
      this.value = null;
      this.updateTable();
    },
    atualizarPedidos() {
      const orders = this.orders.map((item) => item.pk);
      this.$store.dispatch(this.changeFunc[this.value], { orders, callback: this.changeOrder });
      return false;
    },
  },
};
</script>

<style>
</style>
