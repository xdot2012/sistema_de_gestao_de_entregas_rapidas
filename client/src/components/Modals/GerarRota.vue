<template>
  <v-dialog>
      <template v-slot:activator="{ on, attrs }">
        <v-btn class="flex-fill mx-2"
          :disabled="waitingOrders.length==0"
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

          <v-card-text  class="flex-fill">
            <div v-if="!etapaPedido" class="d-flex">
              <div class="d-flex flex-column flex-fill" >
                <h2 class="text-center">{{ waitingOrders.length }} Pedidos em Espera</h2>
                <v-text-field label="Digite a Capacidade de Entrega"
                  type="number"
                  v-model="capacidadeTotal"
                  hide-details="auto"
                  required
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
                        <td>{{item.distance}}</td>
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
                    v-for="item in getPath" :key="item.index">
                    <!-- <td>{{ item.entregador }}</td> -->
                    <td>{{ item.index }} </td>
                    <td>{{ item.order.pk }}</td>
                    <td>{{ item.order.client_name }}</td>
                    <td>{{ item.order.address.format }}</td>
                    <td>
                      <v-chip
                        dark
                        v-for="product in item.order.products" :key="product.pk"
                      >
                        x{{product.quantity}} - {{ product.name }}
                      </v-chip>
                    </td>
                    <td>
                      <v-icon color="success" v-if="item.order.ispaid"> mdi-check</v-icon>
                      <v-icon color="error" v-else>mdi-close</v-icon>
                    </td>
                    </tr>
                </tbody>
              </v-simple-table>
            </div>
          </v-card-text>

          <v-card-actions class="justify-end mt-auto">
            <v-btn v-if="etapaPedido>0"
              x-large
              color="default"
              @click="voltarEtapa(etapaPedido)">Voltar</v-btn>
            <v-spacer></v-spacer>
            <v-btn v-if="etapaPedido==0"
              :disabled="!capacidadeTotal>0"
              x-large
              color="primary"
              @click="proximaEtapa(etapaPedido)">Próximo</v-btn>
            <v-btn v-else-if="etapaPedido==1"
              :disabled="!produtosSelecionados>0"
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
                Finalizar</v-btn>
            </div>
          </v-card-actions>
        </v-card>
      </template>
  </v-dialog>
</template>

<script>
import { mapGetters } from 'vuex';

import { sortOrdersByTime, sortOrdersByDistance } from '../../functions';

export default {
  name: 'GerarRota',
  computed: mapGetters(['getAllDeliveryman', 'waitingOrders', 'ordersWithPriority', 'getPath']),
  beforeCreate() {
    this.$store.dispatch('getCitys');
  },
  data: () => ({
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
  }),
  methods: {
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
      const orders = this.$store.getters.getOrdersInPath.map((order) => order.pk);
      this.$store.dispatch('deliverOrders', { orders, callback: this.onFinish });
      return false;
    },
    showRoute() {
      this.etapaPedido += 1;
    },
    proximaEtapa(etapaPedido) {
      if (etapaPedido === 1) {
        const orderList = this.$store.getters.ordersWithPriority.filter(
          (item) => item.selected === true,
        );
        const orders = orderList.map((item) => item.pk);
        this.$store.dispatch('generatePath', { orders, callback: this.showRoute });
      } else {
        this.etapaPedido = etapaPedido + 1;
      }
    },
    voltarEtapa(etapaPedido) {
      this.etapaPedido = etapaPedido - 1;
    },
    imprimeRota() {
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
