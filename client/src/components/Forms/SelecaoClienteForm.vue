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
        <div v-if="addEndereco">
          <novo-endereco-form :onFinish="getNewAddress"/>
        </div>
        <div v-else>
          <v-autocomplete
            :disabled="editarEndereco || addEndereco"
            v-model="selectedAddressID"
            :items="selectedClientInfo.addresses"
            dense
            filled
            label="Endereço"
            item-text="format"
            item-value="pk"
            ></v-autocomplete>
          <div
            class="d-flex">
            <v-text-field
            class="mr-3"
            style="max-width: 25%"
            label="CEP"
            v-mask="'#####-###'"
            v-model="selectedAddress.code"
            :rules="regraCEP"
            :readonly="!editarEndereco"></v-text-field>
          </div>

          <div class="d-flex">
            <v-text-field
            class="mr-3"
            style="max-width: 75%"
            label="Rua"
            v-model="selectedAddress.street"
            :readonly="!editarEndereco"></v-text-field>

            <v-text-field
            class="mr-3"
            style="max-width: 25%"
            label="Número"
            v-model="selectedAddress.number"
            :rules="regraNumero"
            :readonly="!editarEndereco"></v-text-field>
          </div>

          <div class="d-flex">
            <v-text-field
            class="mr-3"
            style="max-width: 50%"
            label="Bairro"
            v-model="selectedAddress.district"
            :readonly="!editarEndereco"></v-text-field>

            <v-text-field
            class="mr-3"
            style="max-width: 50%"
            label="Cidade/Estado"
            v-model="selectedAddress.city_name"
            :readonly="!editarEndereco"></v-text-field>
          </div>
        </div>

      <div class="d-flex">
        <v-spacer></v-spacer>
        <v-btn v-if="!editarEndereco"
          :disabled="!selectedAddressID"
          @click="editarEndereco=!editarEndereco"
          class="ml-auto"
          color="primary"
          large>Editar Endereço</v-btn>
        <v-btn v-else
          @click="salvarEndereco()"
          class="ml-auto"
          color="primary"
          large>Salvar Alterações</v-btn>
        <v-btn
          v-if="!addEndereco"
          @click="novoEndereco()"
          class="ml-5"
          color="primary"
          large>Adicionar Outro Endereço</v-btn>
        <v-btn
          v-else
          :disabled="!validatedAddress"
          @click="adicionarEndereco()"
          class="ml-5"
          color="primary"
          large>Salvar Endereço</v-btn>
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
import NovoEnderecoForm from './NovoEnderecoForm.vue';

export default {
  components: { NovoEnderecoForm },
  computed: mapGetters(['getAllClients']),
  props: ['validSelection'],
  name: 'SelecaoClienteForm',
  data: () => ({
    selectedClientInfo: {
      name: null,
      phone: null,
      formated_phone: null,
      pk: null,
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
    regraNomeCliente,
    regraTelefone,
    regraNumero,
    regraCEP,
    selectedAddress: {
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
    },
    selectedAddressID: null,
    addEndereco: false,
    validatedAddress: false,
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
    novoEndereco() {
      this.editarEndereco = false;
      this.addEndereco = true;
      this.selectedAddressID = null;
      this.selectedAddress = {
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
      };
    },
    adicionarEndereco() {
      this.$store.dispatch('addClientAddress', {
        address: this.selectedAddress,
        client: this.clienteSelecao,
        callback: this.setAddress,
      });
      this.addEndereco = false;
    },
    getNewAddress(data) {
      this.validatedAddress = true;
      this.selectedAddress = data;
    },
    setAddress(data) {
      this.selectedAddressID = data.pk;
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
      const [firstAddress] = obj.addresses;

      if (firstAddress?.pk) {
        this.selectedAddressID = firstAddress.pk;
      } else {
        this.selectedAddressID = null;
      }
      this.validSelection(true);
      return val;
    },
    selectedAddressID: function onChange(val) {
      if (!val) {
        this.selectedAddress = {
          altitude: null,
          city_name: null,
          client: null,
          code: null,
          country_name: null,
          district: null,
          street: null,
          latitude: null,
          longitude: null,
        };
        return null;
      }
      const obj = this.selectedClientInfo.addresses.find(
        (item) => item.pk === val,
      );
      this.selectedAddress = obj;
      return val;
    },
  },
};
</script>
