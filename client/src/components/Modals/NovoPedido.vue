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
            <div class="d-flex" v-if="!etapaPedido">
              <!-- SELEÇÃO DE PRODUTO -->
              <div class="d-flex flex-column" style="width: 25%; height: 100%">
                <v-simple-table light>
                  <thead>
                    <tr>
                      <th colspan="3" class="mb-5 text-center primary white--text">
                        <h2>Resumo do Pedido</h2>
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="item in pedidoCliente" :key=item.id>
                      <td>{{item.nome}}</td>
                      <td>{{item.quantidade}}</td>
                      <td>
                        <v-btn
                          @click="removeItem(item.id)"
                          color="gray"
                          icon
                          small>
                          <v-icon>mdi-delete</v-icon>
                        </v-btn>
                      </td>
                    </tr>
                  </tbody>
                </v-simple-table>
              </div>

              <div class="ml-auto d-flex justify-end" style="width:70%">
                <div cl="d-flex flex-column">
                  <h3>Descrição do Produto:</h3>
                  <v-text-field
                    v-on:keyup.enter="onEnter()"
                    :rules="regraTexto"
                    v-model="textoItem">
                  </v-text-field>

                  <div class="d-flex align-center justify-end">
                    <v-btn
                      icon
                      @click="diminuirQuantidade()"
                      small
                      color="primary"
                      :disabled="quantidadeItem<=1">
                      <v-icon>mdi-minus</v-icon>
                    </v-btn>
                    <v-text-field
                      :rules="regraNumero"
                      style="max-width: 10%"
                      class="ml-3 mr-3"
                      v-model="quantidadeItem">
                    </v-text-field>
                    <v-btn
                      icon
                      @click="aumentarQuantidade()"
                      small
                      color="primary">
                      <v-icon>mdi-plus</v-icon>
                    </v-btn>
                    <v-btn
                      @click="adicionarItem()"
                      class="ml-5"
                      color="primary"
                      :disabled="!textoItem || !quantidadeItem"
                      >ADICIONAR AO PEDIDO
                    </v-btn>
                  </div>
                </div>
              </div>
              <!-- /SELEÇÃO DE PRODUTOS -->
            </div>

            <div v-else-if="etapaPedido==1" class="mt-5">
              <!-- SELEÇÃO CLIENTE -->
              <v-radio-group v-model="getClientBy" row>
                <v-radio label="Selecionar Cliente" color="primary" value="selecionar_cliente"
                ></v-radio>
                <v-radio label="Novo Cliente" color="primary" value="novo_cliente"
                ></v-radio>
              </v-radio-group>

              <novo-cliente-form
                v-if="getClientBy == 'novo_cliente'"
                :dialog="criarCliente"
                ref="clientCreate"  />
              <selecao-cliente-form v-else
               ref="clientSelect"
               :validSelection="clientValidation" />
              <!-- /SELEÇÃO CLIENTE -->
            </div>

            <div v-else-if="etapaPedido==2" class="d-flex">
              <!-- ENTREGA -->
              <div class="d-flex flex-column" style="width: 25%; height: 100%">
                <v-simple-table>
                  <thead>
                    <tr>
                      <th colspan="2" class="mb-5 text-center primary white--text">
                        <h2>Resumo do Pedido</h2>
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="item in pedidoCliente" :key=item.id>
                      <td>{{item.nome}}</td>
                      <td>{{item.quantidade}}</td>
                    </tr>
                  </tbody>
                </v-simple-table>
              </div>

              <div class="ml-10 d-flex justify-start flex-fill">
                <div class="d-flex flex-column flex-fill" >
                  <h2>Resumo do Pedido:</h2>
                  <v-divider />
                  <h3>Cliente:</h3>
                  <div class="d-flex justify-space-between">
                    <h3>Nome do Cliente: {{clientData.name}}</h3>
                    <h3>Telefone do Cliente: {{clientData.phone}}</h3>
                  </div>
                  <v-divider />
                  <div class="d-flex flex-column">
                    <h3>Endereço de Entrega:</h3>
                    <div class="d-flex justify-space-between">
                      <h3>Rua: {{clientData.street}}</h3>
                      <h3>Número: {{clientData.number}}</h3>
                    </div>
                    <div class="d-flex justify-space-between">
                      <h3>Bairro: {{clientData.district}}</h3>
                      <h3>Cidade: {{clientData.city_name}}</h3>
                    </div>
                  </div>
                  <v-divider />
                  <div class="d-flex justify-start">
                    <div class="d-flex flex-column">
                      <h3>Método de Pagamento:</h3>
                        <v-radio-group v-model="metodoPagamento">
                          <v-radio label="Já pago" value="pago"></v-radio>
                          <v-radio label="Cartão Crédito" value="cartao_credito"></v-radio>
                          <v-radio label="Cartão Débito" value="cartao_debito"></v-radio>
                          <v-radio label="Dinheiro" value="dinheiro"></v-radio>
                          <v-radio label="Pix" value="pix"></v-radio>
                        </v-radio-group>
                    </div>
                    <div class="d-flex flex-column ml-10">
                      <h3>Método de Entrega:</h3>
                      <v-radio-group v-model="tipoEntrega">
                        <v-radio label="Delivery" value="delivery"></v-radio>
                        <v-radio label="Agendar Horário" value="agendar_horario"></v-radio>
                        <v-radio label="Retirada no Local" value="retirada_local"></v-radio>
                      </v-radio-group>
                    </div>
                  </div>
                </div>
              </div>
              <!-- /ENTREGA -->
            </div>
          </v-card-text>

          <v-card-actions class="justify-end mt-auto">
            <v-btn v-if="etapaPedido>0"
              x-large
              color="primary"
              @click="voltarEtapa()">Voltar</v-btn>
            <v-spacer></v-spacer>
            <v-btn v-if="etapaPedido==0"
              x-large
              color="primary"
              @click="proximaEtapa()"
              :disabled="!validaProdutos">Próximo</v-btn>
            <v-btn v-else-if="etapaPedido==1"
              x-large
              color="primary"
              @click="proximaEtapa()"
              :disabled="!validaCliente">Próximo</v-btn>
            <v-btn v-else
              x-large
              color="primary"
              @click="dialog.value = finalizarPedido()"
              :disabled="!metodoPagamento || !tipoEntrega">
              Finalizar Pedido</v-btn>
          </v-card-actions>
        </v-card>
      </template>
  </v-dialog>
</template>

<script>
import { mapGetters } from 'vuex';

import NovoClienteForm from '../Forms/NovoClienteForm.vue';
import SelecaoClienteForm from '../Forms/SelecaoClienteForm.vue';

import {
  regraTexto,
  regraNumero,
} from '../../regras_input';

export default {
  computed: mapGetters(['getAllClients']),
  components: {
    NovoClienteForm,
    SelecaoClienteForm,
  },
  beforeCreate() {
    this.$store.dispatch('getClients');
  },
  name: 'NovoPedido',
  data: () => ({
    getClientBy: 'selecionar_cliente',
    etapaPedido: 0,
    clientID: null,
    value: null,
    confirmaPedido: null,
    regraTexto,
    regraNumero,
    pedidoCliente: [],
    textoItem: null,
    quantidadeItem: 1,
    metodoPagamento: null,
    tipoEntrega: null,
    validaProdutos: false,
    validaCliente: false,
  }),
  methods: {
    finalizarPedido() {
      this.etapaPedido = 0;
      this.confirmaPedido = true;
      return false;
    },
    proximaEtapa() {
      if (this.etapaPedido === 1) {
        if (this.getClientBy === 'selecionar_cliente') {
          this.clientID = this.$refs.clientSelect.getClient();
          this.clientData = this.$refs.clientSelect.getClientData();
        }
      }
      this.etapaPedido += 1;
    },
    voltarEtapa() {
      this.etapaPedido -= 1;
    },
    onEnter() {
      this.adicionarItem();
    },
    adicionarItem() {
      this.pedidoCliente.push({
        id: this.pedidoCliente.length,
        nome: this.textoItem,
        quantidade: this.quantidadeItem,
      });
      this.textoItem = null;
      this.quantidadeItem = 1;
      this.validaProdutos = true;
    },
    removeItem(id) {
      this.pedidoCliente = this.pedidoCliente.filter((item) => item.id !== id);
      if (this.pedidoCliente.length === 0) {
        this.validaProdutos = false;
      }
    },
    diminuirQuantidade() {
      this.quantidadeItem = parseInt(this.quantidadeItem, 10) - 1;
    },
    aumentarQuantidade() {
      this.quantidadeItem = parseInt(this.quantidadeItem, 10) + 1;
    },
    criarCliente(id, data) {
      this.clientID = id;
      this.clientData = data;
      this.proximaEtapa(this.etapaPedido);
    },
    clientValidation(val) {
      this.validaCliente = val;
    },
  },
};
</script>

<style>
</style>
