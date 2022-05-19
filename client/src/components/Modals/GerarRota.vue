<template>
  <v-dialog>
      <template v-slot:activator="{ on, attrs }">
        <v-btn class="flex-fill mx-2"
          :disabled="waitingOrders.length==0"
          x-large
          block
          color="accent"
          v-bind="attrs" v-on="on">Gerar Rota</v-btn>
      </template>

      <template v-slot:default="dialog">
        <v-card class="pa-8 d-flex flex-column" width="100vw" Resumo min-height="90vh">
          <v-card-title class="d-flex text-h5">
              <v-spacer />
              Gerar Rota
              <v-spacer />
              <v-btn icon text @click="dialog.value = false">
                <v-icon>mdi-close</v-icon>
              </v-btn>
          </v-card-title>

          <v-card-text  class="flex-fill">
            <div v-if="!etapaPedido" class="d-flex">
              <div class="d-flex flex-column flex-fill" >
                <h2 class="text-center">{{ waitingOrders.length }} Pedidos em Espera</h2>
                <v-text-field label="Digite a Capacidade de Entrega"
                  type="number"
                  v-model="capacidadeTotal"
                  hide-details="auto"
                  required
                  v-on:keydown.enter='selecionaCapacidade'
                ></v-text-field>
                <!-- <h3>Selecione Entregadores:</h3>
                <div class="d-flex flex-column">
                  <v-checkbox
                    :label="'Selecionar Todos'"
                    v-model="todosEntregadores"
                    @change="selecionaTodos()"/>
                  <v-checkbox
                    v-for="entregador in getAllDeliveryman" :key="entregador.pk"
                    :label="entregador.name"
                    v-model="entregador.selecionado"
                    @change="selecionaEntregador(entregador)"/>
                  </div>
                <h2 class="text-center">Capacidade Total: {{capacidadeTotal}} Produtos</h2> -->
              </div>
            </div>

            <div v-else-if="etapaPedido==1">
              <div class="d-flex">
                <div class="d-flex flex-column" style="width: 25%; height: 100%">
                  <h3>Seleção de Pedidos:</h3>
                    <v-radio-group v-model="metodoSelecaoPedidos">
                      <v-radio
                        @click="tempoDeEspera()"
                        label="Priorizar Tempo de Espera"
                        value="tempo_espera" />
                      <v-radio
                        @click="rotaMaisCurta()"
                        label="Priorizar Menor Distância"
                        value="rota_mais_curta" />
                      <v-radio
                        label="Selecao Manual"
                        value="selecao_manual"
                        @click="limparSelecao()" />
                    </v-radio-group>
                </div>

                <div class="ml-auto d-flex justify-end" style="width:70%">
                  <v-simple-table>
                    <thead>
                      <tr>
                        <th>Selecionado</th>
                        <th>Pedido</th>
                        <th class="text-center">Produtos</th>
                        <th>Distância</th>
                        <th>Tempo de Espera</th>
                        <th></th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="item in ordersWithPriority" :key=item.pk>
                        <td>
                          <v-checkbox
                            v-model="item.selected"
                            :disabled="metodoSelecaoPedidos!='selecao_manual'"
                            @click="adicionaItem(item)"
                            />
                          </td>
                        <td>#{{item.pk}}</td>
                        <td>
                          <div v-for="product in item.products" :key="product.pk">
                            x{{product.quantity}} - {{product.name}}
                          </div>
                        </td>
                        <td>{{item.address.distance}} m</td>
                        <td>{{item.waiting_time}} minutos</td>
                      </tr>
                    </tbody>
                  </v-simple-table>
                </div>
              </div>
              <h2 class="mt-auto text-center">
                {{produtosSelecionados}}/{{capacidadeTotal}} Produtos Selecionados</h2>
            </div>

            <div v-else-if="etapaPedido==2" >
              <h1 class="text-center">Rota Gerada com Sucesso!</h1>
              <v-simple-table>
                <thead>
                  <tr>
                    <th>#</th>
                    <!-- <th>Entregador</th> -->
                    <th>Número do Pedido</th>
                    <th>Cliente</th>
                    <th>Endereço</th>
                    <th>Produtos</th>
                    <th>Foi Paga?</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="item in ordersInPath" :key="item.index">
                    <!-- <td>{{ item.entregador }}</td> -->
                    <!-- <td>{{ item.index }} </td> -->
                    <td>{{ item.pk }}</td>
                    <td>{{ item.client_name }}</td>
                    <td>{{ item.address.format }}</td>
                    <td>
                      <v-chip
                        dark
                        v-for="product in item.products" :key="product.pk"
                      >
                        x{{product.quantity}} - {{ product.name }}
                      </v-chip>
                    </td>
                    <td>
                      <v-icon color="success" v-if="item.is_paid"> mdi-check</v-icon>
                      <v-icon color="error" v-else>mdi-close</v-icon>
                    </td>
                    </tr>
                </tbody>
              </v-simple-table>

              <l-map style="height: 350px" :zoom="zoom" :center="polylineData[0]">
                <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
                <l-marker
                  v-for="location in getPath"
                  v-bind:key="location.index"
                  :lat-lng="location.point">
                <l-popup>
                  <h3>{{getMapPopUpTitle(location, getPath.length)}}</h3>
                  <div v-for="order in location.orders" v-bind:key="order.pk">
                    (#{{ order.pk }}) {{ order.client_name }}, {{ order.address.format }}</div>
                </l-popup>
                </l-marker>
                <l-polyline
                  v-for="leg in polylineLegData"
                  v-bind:key="leg.polilyne"
                  :lat-lngs="leg.polyline"
                  :color="getColor(leg.key)">
                </l-polyline>
              </l-map>
            </div>
          </v-card-text>

          <v-card-actions class="justify-end mt-auto">
            <v-col cols="2">
              <v-btn v-if="etapaPedido>0"
                x-large
                block
                color="default"
                @click="voltarEtapa(etapaPedido)">Voltar</v-btn>
            </v-col>
            <v-spacer />
            <v-col cols="3">
              <v-btn
                v-if="etapaPedido==0"
                :disabled="!capacidadeTotal>0"
                x-large
                block
                color="primary"
                @click="proximaEtapa(etapaPedido)">Próximo
              </v-btn>
              <v-btn
                v-else-if="etapaPedido==1"
                :disabled="!produtosSelecionados>0"
                x-large
                block
                color="primary"
                @click="proximaEtapa(etapaPedido)">Próximo
              </v-btn>
            <v-row v-else>
              <v-col cols="6">
                <v-btn
                  class="mr-5"
                  x-large
                  block
                  color="primary"
                  @click="imprimeRota()">
                  Imprimir Rota</v-btn>
              </v-col>
              <v-col cols="6">
                <v-btn
                  x-large
                  block
                  color="primary"
                  @click="dialog.value = finalizarPedido()">
                  Finalizar</v-btn>
              </v-col>
            </v-row>
          </v-col>
        </v-card-actions>
      </v-card>
    </template>
  </v-dialog>
</template>

<script>
import { mapGetters } from 'vuex';
import {
  LMap,
  LTileLayer,
  LPolyline,
  LMarker,
  LPopup,
} from 'vue2-leaflet';

import {
  sortOrdersByTime,
  sortOrdersByDistance,
  printJSONRoute,
  getMapPopUpTitle,
} from '../../functions';

export default {
  components: {
    LMap,
    LTileLayer,
    LPolyline,
    LMarker,
    LPopup,
  },
  name: 'GerarRota',
  computed: mapGetters([
    'getAllDeliveryman',
    'waitingOrders',
    'ordersWithPriority',
    'getPath',
    'ordersInPath',
    'polylineData',
    'polylineStepData',
    'polylineLegData',
  ]),
  beforeCreate() {
    this.$store.dispatch('getCitys');
  },
  data: () => ({
    getMapPopUpTitle,
    printJSONRoute,
    url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attribution: '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
    zoom: 15,
    etapaPedido: 0,
    metodoPagamento: null,
    tipoEntrega: null,
    todosEntregadores: false,
    capacidadeTotal: 0,
    nPedidos: 0,
    produtosSelecionados: 0,
    ordensSelecionadas: [],
    listaEntregadores: [],
    metodoSelecaoPedidos: null,
    polilyneColors: [
      '#2629de',
      '#26de29',
      '#26cbde',
      '#de7926',
    ],
  }),
  methods: {
    getColor(index) {
      if (index === this.$store.getters.polylineLegData.length - 1) {
        return '#d61e1e';
      }
      if (index < this.$store.getters.polylineLegData.length - 1) {
        if (index < this.polilyneColors.length) {
          return this.polilyneColors[index];
        }
      }
      let randomColor = `#${Math.floor(Math.random() * 16777215).toString(16)}`;
      while (randomColor in this.polilyneColors) {
        randomColor = `#${Math.floor(Math.random() * 16777215).toString(16)}`;
      }
      return randomColor;
    },
    onFinish() {
      this.clearForm();
    },
    clearForm() {
      this.etapaPedido = 0;
      this.metodoPagamento = null;
      this.tipoEntrega = null;
      this.todosEntregadores = false;
      this.capacidadeTotal = 0;
      this.nPedidos = 0;
      this.produtosSelecionados = 0;
      this.ordensSelecionadas = [];
      this.listaEntregadores = [];
      this.metodoSelecaoPedidos = null;
    },
    finalizarPedido() {
      this.etapaPedido = 0;
      this.confirmaPedido = true;
      const orders = this.$store.getters.ordersInPath.map((item) => item.pk);
      this.$store.dispatch('deliverOrders', { orders, callback: this.onFinish });
      return false;
    },
    showRoute() {
      this.etapaPedido += 1;
    },
    proximaEtapa() {
      if (this.etapaPedido === 1) {
        const orderList = this.$store.getters.ordersWithPriority.filter(
          (item) => item.selected === true,
        );
        const orders = orderList.map((item) => item.pk);
        this.$store.dispatch('generatePath', { orders, callback: this.showRoute });
      } else {
        this.etapaPedido += 1;
      }
    },
    voltarEtapa() {
      this.etapaPedido -= 1;
    },
    getOrderStatus(order) {
      if (order.ispaid) {
        return 'Sim';
      }
      return 'Não';
    },
    imprimeRota() {
      const jsonData = this.$store.getters.ordersInPath.map((item) => ({
        '#': item.index,
        numero: item.pk,
        cliente: item.client_name,
        endereco: item.address.format,
        produtos: item.products.map((product) => `x${product.quantity} - ${product.name}`),
        paga: this.getOrderStatus(item),
      }));
      const headers = ['#', 'numero', 'cliente', 'endereco', 'produtos', 'paga'];
      this.printJSONRoute(jsonData, headers);
      return false;
    },
    selecionaEntregador(entregador) {
      if (!entregador.selecionado) {
        this.todosEntregadores = false;
        this.capacidadeTotal -= parseInt(entregador.capacity, 10);
        return;
      }
      this.capacidadeTotal += parseInt(entregador.capacity, 10);
    },
    selecionaTodos() {
      this.capacidadeTotal = 0;
      let count = 0;

      this.listaEntregadores = this.$store.getters.getAllDeliveryman.map((elem) => {
        count += parseInt(elem.capacity, 10);
        return Object.assign(elem, { selecionado: this.todosEntregadores });
      });
      if (this.todosEntregadores) {
        this.capacidadeTotal = count;
      }
    },
    limparSelecao() {
      this.produtosSelecionados = 0;
      for (let i = 0; i < this.$store.getters.ordersWithPriority.length; i += 1) {
        this.$store.getters.ordersWithPriority[i].selected = false;
      }
      this.ordensSelecionadas = [];
    },
    adicionaItem(item) {
      if (item.selected) {
        this.ordensSelecionadas.push(item);
        this.produtosSelecionados += item.quantity;
      } else {
        const index = this.ordensSelecionadas.findIndex((order) => order.pk === item.pk);
        if (index !== -1) {
          this.ordensSelecionadas.splice(index, 1);
        }
        this.produtosSelecionados -= item.quantity;
      }
    },
    rotaMaisCurta() {
      this.produtosSelecionados = 0;
      this.$store.getters.ordersWithPriority.sort(sortOrdersByDistance);
      for (let i = 0; i < this.$store.getters.ordersWithPriority.length; i += 1) {
        if (this.produtosSelecionados
          + this.$store.getters.ordersWithPriority[i].quantity <= this.capacidadeTotal) {
          this.produtosSelecionados += this.$store.getters.ordersWithPriority[i].quantity;
          this.$store.getters.ordersWithPriority[i].selected = true;
        } else {
          this.$store.getters.ordersWithPriority[i].selected = false;
        }
      }
    },
    tempoDeEspera() {
      this.produtosSelecionados = 0;
      this.$store.getters.ordersWithPriority.sort(sortOrdersByTime);
      for (let i = 0; i < this.$store.getters.ordersWithPriority.length; i += 1) {
        if (this.produtosSelecionados
          + this.$store.getters.ordersWithPriority[i].quantity <= this.capacidadeTotal) {
          this.produtosSelecionados += this.$store.getters.ordersWithPriority[i].quantity;
          this.$store.getters.ordersWithPriority[i].selected = true;
        } else {
          this.$store.getters.ordersWithPriority[i].selected = false;
        }
      }
    },
    selecionaCapacidade() {
      if (this.capacidadeTotal > 0) {
        this.proximaEtapa();
      }
    },
  },
  watch: {
    capacidadeTotal: function onChange(val) {
      if (typeof (val) === 'string') {
        this.capacidadeTotal = parseInt(val, 10);
      }
    },
  },
};
</script>

<style>
</style>
