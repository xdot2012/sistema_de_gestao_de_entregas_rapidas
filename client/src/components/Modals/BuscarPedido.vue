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
              <v-tab href="#tab-4">Data</v-tab>
            </v-tabs>
          </v-card-title>

          <v-card-text>
            <v-tabs-items v-model="tab">
              <v-tab-item value="tab-1">
                <div >
                  <h1>Digite o nome do cliente </h1>
                  <v-autocomplete
                    class="mt-5"
                    v-model="selectedClientID"
                    :search-input.sync="nomeBusca"
                    :items="getAutoCompleteClientName"
                    dense
                    label="Cliente"
                    item-text="name"
                    item-value="pk"
                  ></v-autocomplete>
                </div>
              </v-tab-item>
              <v-tab-item value="tab-2">
                  <div>
                  <h1>Digite o número de Telefone</h1>
                  <v-autocomplete
                    class="mt-5"
                    v-model="selectedClientID"
                    :search-input.sync="telefoneBusca"
                    :items="getAutoCompleteClientName"
                    dense
                    label="Telefone do Cliente"
                    item-text="phone_format"
                    item-value="pk"
                  ></v-autocomplete>
                </div>
              </v-tab-item>
              <v-tab-item value="tab-3">
                <div>
                  <h1>Digite o Endereço</h1>
                  <v-autocomplete
                    class="mt-5"
                    v-model="selectedClientID"
                    :search-input.sync="enderecoBusca"
                    :items="getAutoCompleteClientName"
                    dense
                    label="Endereço do Cliente"
                    item-text="main_address.format"
                    item-value="pk"
                  ></v-autocomplete>
                </div>
              </v-tab-item>

              <v-tab-item value="tab-4">
                <div>
                  <h1>Selecione a Data</h1>
                  <v-date-picker
                    full-width
                    v-model="dataBusca" />
                  <v-autocomplete
                    class="mt-5"
                    v-model="selectedClientID"
                    :search-input.sync="enderecoBusca"
                    :items="activeOrders"
                    dense
                    label="Data do Pedido"
                    item-text="created_on"
                    item-value="pk"
                  ></v-autocomplete>
                </div>
              </v-tab-item>
            </v-tabs-items>
            <div class="mt-5">
              Pedidos Encontrados:
            </div>
            <div v-if="!ordersFound.length">
              Nenhum Pedido Encontrado
            </div>
            <div v-else>
              <div v-for="item in ordersFound" :key="item.pk">
                {{item.date}}
                <div v-for="product in item.products" :key="product.pk">
                  x{{ product.quantity }} - {{ product.name }}
                </div>
              </div>
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
import { mapGetters } from 'vuex';

import { stringToDate } from '../../functions';

export default {
  name: 'BuscarPedido',
  computed: mapGetters(['activeOrders', 'getAutoCompleteClientName']),
  beforeCreate() {
    this.$store.dispatch('getHistory');
    this.$store.dispatch('getClients');
  },
  data() {
    return {
      tab: null,
      selectedClientID: null,
      nomeBusca: null,
      telefoneBusca: null,
      enderecoBusca: null,
      dataBusca: null,
      ordersFound: [],
    };
  },
  watch: {
    selectedClientID: function onChange(val) {
      if (!val) {
        return null;
      }
      const orders = this.$store.getters.allOrders.filter(
        (item) => item.client === val,
      );

      this.ordersFound = orders.map((item) => Object.assign(
        item, { date: stringToDate(item.created_on) },
      ));
      return val;
    },
  },
};
</script>

<style>
</style>
