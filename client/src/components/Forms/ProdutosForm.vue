<template>
  <div class="d-flex">
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
  </div>
</template>

<script>
import {
  regraTexto,
  regraNumero,
} from '../../regras_input';

import ItemPedido from '../../classes_input';

export default {
  name: 'ProdutosForm',
  data: () => ({
    regraTexto,
    regraNumero,
    pedidoCliente: [],
    textoItem: null,
    quantidadeItem: 1,
  }),
  methods: {
    onEnter() {
      this.adicionarItem();
    },
    adicionarItem() {
      this.pedidoCliente.push(new ItemPedido(
        this.pedidoCliente.length,
        this.textoItem,
        this.quantidadeItem,
      ));
      this.textoItem = null;
      this.quantidadeItem = 1;
    },
    removeItem(id) {
      this.pedidoCliente = this.pedidoCliente.filter((item) => item.id !== id);
    },
    diminuirQuantidade() {
      this.quantidadeItem = parseInt(this.quantidadeItem, 10) - 1;
    },
    aumentarQuantidade() {
      this.quantidadeItem = parseInt(this.quantidadeItem, 10) + 1;
    },

  },
};
</script>
