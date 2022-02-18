<template>
  <v-dialog max-width="95%">
      <template v-slot:activator="{ on, attrs }">
        <v-btn class="flex-fill mx-2"
          x-large
          color="primary"
          v-bind="attrs" v-on="on">BUSCAR PEDIDO</v-btn>
      </template>

      <template v-slot:default="dialog">
        <v-card class=" pa-8">
          <v-card-title class="d-flex ">
            <v-tabs v-model="tab">
              <div class="text-h5">Buscar Pedido</div>
              <v-spacer></v-spacer>
              <div class="mr-10">Filtrar pedidos por:</div>
              <v-tab href="#tab-1">Nome</v-tab>
              <v-tab href="#tab-2">Telefone</v-tab>
              <v-tab href="#tab-3">Endereço</v-tab>
              <v-tab href="#tab-4">Data/Hora</v-tab>
            </v-tabs>
          </v-card-title>

          <v-card-text>
            <v-tabs-items v-model="tab">
              <v-tab-item value="tab-1">Nome</v-tab-item>
              <v-tab-item value="tab-2">Telefone</v-tab-item>
              <v-tab-item value="tab-3">Endereço</v-tab-item>
              <v-tab-item value="tab-4">Data/Hora</v-tab-item>
            </v-tabs-items>

            <div class="mt-5">
              Pedidos Encontrados:
            </div>
          </v-card-text>

          <v-card-actions class="justify-end">
            <v-btn text @click="dialog.value = false">Close</v-btn>
          </v-card-actions>
        </v-card>
      </template>
  </v-dialog>
</template>

<script>
export default {
  name: 'BuscarPedido',
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
