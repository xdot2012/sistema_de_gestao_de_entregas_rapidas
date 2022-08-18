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
          v-mask="'(##)#####-####'"
          :rules="regraTelefone"
          :readonly="!editarNomeTelefone"></v-text-field>
        </div>

        <div class="d-flex">
          <v-spacer></v-spacer>
          <div v-if="!editarNomeTelefone">
          <v-btn
            @click="editarNomeTelefone=!editarNomeTelefone"
            class="ml-auto"
            color="accent"
            large>Editar</v-btn>
          </div>
          <div v-else>
          <v-btn
            @click="editarNomeTelefone=!editarNomeTelefone"
            class="ml-auto mr-5"
            color="Default"
            large>Cancelar</v-btn>
          <v-btn
            @click="salvarNomeTelefone()"
            color="accent"
            large>Salvar Alterações</v-btn>
          </div>
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

      <div>
        <div v-if="editarEndereco" class="d-flex flex-row justify-space-between">
          <v-btn
            :disabled="!selectedAddressID"
            @click="excluirEndereco"
            color="error"
            large>Excluir Endereço</v-btn>

            <div>
              <v-btn
                class="mr-5"
                @click="editarEndereco = !editarEndereco"
                color="default"
                large>Cancelar
              </v-btn>
              <v-btn
                @click="salvarEndereco()"
                color="accent"
                large>Salvar Alterações
              </v-btn>
            </div>
        </div>
        <div v-else-if="!addEndereco" class="d-flex flex-row justify-end">
          <v-btn
          :disabled="!selectedAddressID"
          @click="editarEndereco=!editarEndereco"
          class="ml-auto"
          color="accent"
          large>Editar Endereço</v-btn>
          <v-btn
            @click="novoEndereco()"
            class="ml-5"
            color="accent"
            large>Adicionar Outro Endereço
          </v-btn>
        </div>
        <div class="d-flex flex-row justify-end" v-else>
          <v-btn
            @click="addEndereco = !addEndereco"
            class="ml-5"
            color="default"
            large>Cancelar</v-btn>
          <v-btn
            :disabled="!validatedAddress"
            @click="adicionarEndereco()"
            class="ml-5"
            color="accent"
            large>Salvar Endereço</v-btn>
          </div>
      </div>
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
</template>
<script>
import { mapGetters } from 'vuex';

import {
  regraTelefone,
  regraNomeCliente,
  regraNumero,
  regraCEP,
} from '../../regras_input';
import { formatPhone } from '../../functions';
import NovoEnderecoForm from './NovoEnderecoForm.vue';

export default {
  components: { NovoEnderecoForm },
  computed: mapGetters(['getAllClients']),
  props: ['validSelection', 'setDeliveryAddress'],
  name: 'SelecaoClienteForm',
  data: () => ({
    formatPhone,
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
    salvarnomeTelefonSucesso() {
      this.nomeTelefoneEditado = true;
    },
    salvarNomeTelefone() {
      this.editarNomeTelefone = !this.editarNomeTelefone;
      const client = {
        name: this.selectedClientInfo.name,
        phone: this.formatPhone(this.selectedClientInfo.phone),
      };
      this.$store.dispatch('updateClient', {
        client,
        clientID: this.selectedClientInfo.pk,
        callback: this.salvarnomeTelefonSucesso,
      });
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
    excluirEndereco() {
      this.$store.dispatch('excluirEndereco', { addressID: this.selectedAddressID, clientID: this.clienteSelecao });
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
      this.setDeliveryAddress(this.selectedAddress);
      return val;
    },
  },
};
</script>
