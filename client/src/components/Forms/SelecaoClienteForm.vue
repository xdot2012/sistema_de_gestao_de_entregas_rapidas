<template>
  <div>
    <v-autocomplete
    v-model="clienteSelecao"
    :items="getAllClients"
    dense
    filled
    label="Cliente"
    item-text="name"
    item-value="pk"
    ></v-autocomplete>
    <v-divider></v-divider>
    <div v-if="clienteSelecao">
      <h2 class="mt-3">Cliente:</h2>
        <div class="d-flex">
          <v-text-field class="mr-2"
          label="Nome Cliente"
          v-model="selectedClientInfo.name"
          :rules="regraNomeCliente"
          :readonly="!editarNomeTelefone"></v-text-field>

          <v-text-field label="Telefone do Cliente"
          v-model="selectedClientInfo.phone"
          v-mask="'(##) ##### - ####'"
          :rules="regraTelefone"
          :readonly="!editarNomeTelefone"></v-text-field>
        </div>

        <div class="d-flex">
          <v-spacer></v-spacer>
          <v-btn v-if="!editarNomeTelefone"
            @click="editarNomeTelefone=!editarNomeTelefone"
            class="ml-auto"
            color="primary"
            large>Editar</v-btn>
          <v-btn v-else
            @click="salvarNomeTelefone()"
            class="ml-auto"
            color="primary"
            large>Salvar Alterações</v-btn>
          <v-snackbar
            v-model="nomeTelefoneEditado"
            :timeout="2000"
            absolute
            bottom
            left
            >Atualizado com Sucesso
          </v-snackbar>
        </div>

        <v-divider class="mt-3"></v-divider>
        <h2 class="mt-1">Endereço de Entrega</h2>
        <div class="d-flex">
          <v-text-field
          class="mr-3"
          style="max-width: 25%"
          label="CEP"
          v-mask="'#####-###'"
          v-model="selectedClientInfo.code"
          :rules="regraCEP"
          :readonly="!editarEndereco"></v-text-field>
        </div>

        <div class="d-flex">
          <v-autocomplete
          class="mr-3"
          style="max-width: 75%"
          label="Rua"
          v-model="selectedClientInfo.street"
          :items="opcoesRua"
          :readonly="!editarEndereco"></v-autocomplete>

          <v-text-field
          class="mr-3"
          style="max-width: 25%"
          label="Número"
          v-model="selectedClientInfo.number"
          :rules="regraNumero"
          :readonly="!editarEndereco"></v-text-field>
        </div>

        <div class="d-flex">
          <v-autocomplete
          class="mr-3"
          style="max-width: 50%"
          label="Bairro"
          v-model="selectedClientInfo.district"
          :items="opcoesBairro"
          :readonly="!editarEndereco"></v-autocomplete>

          <v-autocomplete
          class="mr-3"
          style="max-width: 50%"
          label="Cidade/Estado"
          v-model="selectedClientInfo.city_name"
          :items="opcoesCidadeEstado"
          :readonly="!editarEndereco"></v-autocomplete>
        </div>

      <div class="d-flex">
        <v-spacer></v-spacer>
        <v-btn v-if="!editarEndereco"
          @click="editarEndereco=!editarEndereco"
          class="ml-auto"
          color="primary"
          large>Alterar Endereço</v-btn>
        <v-btn v-else
          @click="salvarEndereco()"
          class="ml-auto"
          color="primary"
          large>Salvar Alterações</v-btn>
        <v-snackbar
        v-model="enderecoEditado"
        :timeout="2000"
        absolute
        bottom
        left
        >Atualizado com Sucesso
        </v-snackbar>
      </div>

    </div>
  </div>
</template>
<script>
import { mapGetters } from 'vuex';

import {
  regraTelefone,
  regraNomeCliente,
  regraNumero,
  regraCEP,
} from '../../regras_input';

export default {
  computed: mapGetters(['getAllClients']),
  props: ['validSelection'],
  name: 'SelecaoClienteForm',
  data: () => ({
    selectedClientInfo: {
      name: null,
      phone: null,
      formated_phone: null,
      pk: null,
      address: null,
    },
    editarEndereco: false,
    editarNomeTelefone: false,
    enderecoEditado: false,
    nomeTelefoneEditado: false,
    nomeCliente: null,
    clienteSelecao: null,
    telefoneCliente: null,
    enderecoEntregaCidadeEstado: null,
    enderecoEntregaNumero: null,
    enderecoEntregaRua: null,
    enderecoEntregaBairro: null,
    enderecoEntregaCEP: null,
    opcoesRua: [
      'Rua 1',
      'Rua 2',
      'Rua 3',
    ],
    opcoesBairro: [
      'Bairro 1',
      'Bairro 2',
      'Bairro 3',
    ],
    opcoesCidadeEstado: [
      'Cidade 1',
      'Cidade 2',
      'Cidade 3',
    ],
    opcoesClientes: [
      'Cláudia',
      'José',
      'Maria',
      'Roberto',
    ],
    regraNomeCliente,
    regraTelefone,
    regraNumero,
    regraCEP,
  }),
  methods: {
    salvarNomeTelefone() {
      this.editarNomeTelefone = !this.editarNomeTelefone;
      this.nomeTelefoneEditado = true;
    },
    salvarEndereco() {
      this.editarEndereco = !this.editarEndereco;
      this.enderecoEditado = true;
    },
    getClient() {
      return this.clienteSelecao;
    },
    getClientData() {
      return this.selectedClientInfo;
    },
  },
  watch: {
    clienteSelecao: function onChange(val) {
      if (!val) {
        this.validSelection(false);
        return null;
      }
      const obj = this.$store.getters.getAllClients.find(
        (item) => item.pk === val,
      );
      this.selectedClientInfo = obj;
      this.validSelection(true);
      return val;
    },
  },
};
</script>
