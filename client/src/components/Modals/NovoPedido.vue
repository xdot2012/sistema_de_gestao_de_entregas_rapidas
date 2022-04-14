<template>
  <v-dialog>
      <template v-slot:activator="{ on, attrs }">
        <v-btn class="flex-fill mx-2"
          x-large
          color="accent"
          v-bind="attrs" v-on="on"
          @click="clearMessages">Novo Pedido</v-btn>
      </template>

      <template v-slot:default="dialog">
        <v-card class="pa-8 d-flex flex-column" width="100vw" min-height="90vh">
          <v-card-title>
              <v-col cols=12>
                <v-row>
                  <h1 class="ml-auto">
                  Novo Pedido
                  </h1>
                  <v-btn
                  class="ml-auto"
                  icon
                  text
                  @click="dialog.value = false">
                    <v-icon>mdi-close</v-icon>
                  </v-btn>
                </v-row>
              </v-col>
          </v-card-title>

          <v-card-text class="flex-fill mt-5">
            <v-col cols=12 class="d-flex" v-if="!etapaPedido">
              <!-- SELEÇÃO DE PRODUTO -->
              <v-col cols=6 class="d-flex flex-column tabela-pedidos">
                <v-simple-table light>
                  <thead>
                    <tr>
                      <th colspan="3" class="mb-5 text-center primary white--text">
                        <h2>Pedido</h2>
                      </th>
                      <tr>
                    </tr>
                    <tr v-if="pedidoCliente.length>0">
                      <th>Nome</th>
                      <th>Quantidade</th>
                      <th class="text-end">Ações</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="item in pedidoCliente" :key=item.arrayID>
                      <td>{{item.name}}</td>
                      <td>{{item.quantity}}</td>
                      <td class="text-end">
                        <v-btn
                          @click="removeItem(item.id)"
                          color="accent"
                          icon
                          small>
                          <v-icon>mdi-delete</v-icon>
                        </v-btn>
                      </td>
                    </tr>
                  </tbody>
                </v-simple-table>
              </v-col>

              <v-col cols=6 class="ml-auto d-flex justify-end">
                <div cl="d-flex flex-column">
                  <h3>Descrição:</h3>
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
                      color="accent"
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
                      color="accent">
                      <v-icon>mdi-plus</v-icon>
                    </v-btn>
                    <v-btn
                      @click="adicionarItem()"
                      class="ml-5"
                      color="accent"
                      :disabled="!textoItem || !quantidadeItem"
                      >ADICIONAR AO PEDIDO
                    </v-btn>
                  </div>
                </div>
              </v-col>
              <!-- /SELEÇÃO DE PRODUTOS -->
            </v-col>

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
               :validSelection="clientValidation"
               :setDeliveryAddress="setClientAddress" />
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
                    <tr v-for="item in pedidoCliente" :key=item.arrayID>
                      <td>{{item.name}}</td>
                      <td>{{item.quantity}}</td>
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
                      <h3>Rua: {{clientAddress.street}}</h3>
                      <h3>Número: {{clientAddress.number}}</h3>
                    </div>
                    <div class="d-flex justify-space-between">
                      <h3>Bairro: {{clientAddress.district}}</h3>
                      <h3>Cidade: {{clientAddress.city_name}}</h3>
                    </div>
                  </div>
                  <v-divider />
                  <div class="d-flex justify-start">
                    <div class="d-flex flex-column">
                      <h3>Método de Pagamento:</h3>
                        <v-radio-group v-model="metodoPagamento">
                          <v-radio label="Cartão Crédito" value="CREDIT_CARD"></v-radio>
                          <v-radio label="Cartão Débito" value="DEBIT_CARD"></v-radio>
                          <v-radio label="Dinheiro" value="CASH"></v-radio>
                          <v-radio label="Pix" value="PIX"></v-radio>
                        </v-radio-group>
                    </div>
                    <div class="d-flex flex-column ml-10">
                      <h3>Método de Entrega:</h3>
                      <v-radio-group v-model="tipoEntrega">
                        <v-radio label="Delivery" value="DEFAULT"></v-radio>
                        <v-radio label="Agendar Horário" value="agendar_horario"></v-radio>
                        <v-radio label="Retirada no Local" value="PICKUP"></v-radio>
                      </v-radio-group>
                    </div>
                  </div>
                    <v-row>
                      <v-checkbox v-model="hasBeenPaid" label="O Pedido já foi pago."></v-checkbox>
                    </v-row>
                </div>
              </div>
              <!-- /ENTREGA -->
            </div>
          </v-card-text>

          <v-card-actions class="justify-end mt-auto">
            <v-btn v-if="etapaPedido>0"
              x-large
              color="default"
              @click="voltarEtapa()">Voltar</v-btn>
            <v-spacer></v-spacer>
            <v-col cols=3>
              <v-btn v-if="etapaPedido==0"
                block
                x-large
                color="primary"
                @click="proximaEtapa()"
                :disabled="!validaProdutos">Continuar</v-btn>
              <v-btn v-else-if="etapaPedido==1"
                block
                x-large
                color="primary"
                @click="proximaEtapa()"
                :disabled="!validaCliente">Continuar</v-btn>
              <v-btn v-else
                block
                x-large
                color="accent"
                @click="dialog.value = finalizarPedido()"
                :disabled="!metodoPagamento || !tipoEntrega">
                Finalizar Pedido</v-btn>
            </v-col>
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
    hasBeenPaid: false,
    clientAddress: {
      street: null,
      number: null,
      district: null,
      city_name: null,
      state_name: null,
      country_name: null,
      code: null,
      reference: null,
      latitude: null,
      longitude: null,
      altitude: null,
      pk: null,
    },
  }),
  methods: {
    clearMessages() {
      this.$store.dispatch('alertClear');
    },
    callback() {
      this.limparPedido();
    },
    limparPedido() {
      this.getClientBy = 'selecionar_cliente';
      this.etapaPedido = 0;
      this.clientID = null;
      this.value = null;
      this.confirmaPedido = null;
      this.pedidoCliente = [];
      this.textoItem = null;
      this.quantidadeItem = 1;
      this.metodoPagamento = null;
      this.tipoEntrega = null;
      this.validaProdutos = false;
      this.validaCliente = false;
      this.hasBeenPaid = false;
    },
    finalizarPedido() {
      const order = {
        client: this.clientID,
        address: this.clientAddress.pk,
        delivery_type: this.tipoEntrega,
        payment_method: this.metodoPagamento,
        is_paid: this.hasBeenPaid,
        products: this.pedidoCliente,
      };
      this.$store.dispatch('createOrder', { order, callback: this.callback });
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
        arrayID: this.pedidoCliente.length,
        name: this.textoItem,
        quantity: this.quantidadeItem,
      });
      this.pedidoCliente.reverse();
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
      this.clientAddress = data.main_address;
      this.proximaEtapa(this.etapaPedido);
    },
    clientValidation(val) {
      this.validaCliente = val;
    },
    setClientAddress(data) {
      this.clientAddress = data;
    },
  },
};
</script>

<style>
.tabela-pedidos {
  overflow-y: scroll;
  max-height: 50vh;
}

</style>
