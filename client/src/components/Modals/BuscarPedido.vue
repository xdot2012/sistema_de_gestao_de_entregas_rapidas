<template>
  <v-dialog max-width="95%">
      <template v-slot:activator="{ on, attrs }">
        <v-btn class="flex-fill mx-2"
          x-large
          block
          color="accent"
          v-bind="attrs" v-on="on">BUSCAR PEDIDO</v-btn>
      </template>

      <template v-slot:default="dialog">
        <v-card class=" pa-8 " width="100vw" min-height="90vh">
            <v-row>
              <div class="ml-auto text-h4">
              Buscar Pedido
              </div>
              <v-btn
              class="ml-auto"
              icon
              text
              @click="dialog.value = false">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-row>
            <v-card-title class="d-flex">
              <v-tabs v-model="tab">
                <v-spacer></v-spacer>
                <div class="mr-10">Filtrar pedidos por:</div>
                <v-tab href="#tab-1">Nome</v-tab>
                <v-tab href="#tab-2">Telefone</v-tab>
                <v-tab href="#tab-3">Endereço</v-tab>
                <v-tab href="#tab-4">Data</v-tab>
              </v-tabs>
            </v-card-title>

          <v-card-text>
            <v-row>
              <v-col cols="6">
                <v-tabs-items v-model="tab">
                  <v-tab-item value="tab-1">
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
                        item-text="address"
                        item-value="pk"
                      ></v-autocomplete>
                    </div>
                  </v-tab-item>

                  <v-tab-item value="tab-4">
                    <v-col cols="6">
                      <h1>Selecione a Data</h1>
                      <v-date-picker
                        full-width
                        v-model="dataBusca" />
                    </v-col>
                  </v-tab-item>
                </v-tabs-items>
              </v-col>

              <v-col cols="6">
                <div v-if="!ordersFound.length">
                  Nenhum Pedido Encontrado
                </div>
                <div v-else>
                  <div class="mt-5">
                    Pedidos Encontrados:
                  </div>
                  <v-simple-table light>
                      <thead>
                        <tr v-if="ordersFound.length>0">
                          <th>#</th>
                          <th>Hora do Pedido</th>
                          <th>Produtos</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="item in ordersFound" :key=item.pk>
                          <td>{{item.pk}}</td>
                          <td>{{item.date}}</td>
                          <td>
                            <v-chip v-for="product in item.products" :key="product.pk">
                              x{{ product.quantity }} - {{ product.name }}
                            </v-chip>
                          </td>
                        </tr>
                      </tbody>
                    </v-simple-table>
                </div>
              </v-col>
            </v-row>
          </v-card-text>

        </v-card>
      </template>
  </v-dialog>
</template>

<script>
import { mapGetters } from 'vuex';

import { stringToDate, calendarDate } from '../../functions';

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
  methods: {
    formatOrders(orders) {
      const formatedOrders = orders.map((item) => Object.assign(
        item, { date: stringToDate(item.created_on) },
      ));
      return formatedOrders;
    },
  },
  watch: {
    selectedClientID: function onChange(val) {
      if (!val) {
        return null;
      }
      const orders = this.$store.getters.allOrders.filter(
        (item) => item.client === val,
      );

      this.ordersFound = this.formatOrders(orders);
      return val;
    },
    dataBusca: function onChange(val) {
      if (!val) {
        return null;
      }
      const orders = this.$store.getters.allOrders.filter(
        (item) => calendarDate(item.created_on) === val,
      );
      this.ordersFound = this.formatOrders(orders);
      return val;
    },
  },
};
</script>

<style>
</style>
