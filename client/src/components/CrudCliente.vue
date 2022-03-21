<template>
    <v-card class="pa-8">
    <v-card-title class="d-flex">
      <v-tabs v-model="tab">
        <div class="text-h5">Clientes</div>
        <v-spacer></v-spacer>
        <div class="mr-10">Filtrar por:</div>
        <v-tab href="#tab-1">Nome</v-tab>
        <v-tab href="#tab-2">Telefone</v-tab>
        <v-tab href="#tab-3">Endereço</v-tab>
      </v-tabs>
    </v-card-title>

    <v-card-text class="d-flex">
      <v-tabs-items class="col-6" v-model="tab">
        <v-tab-item value="tab-1">
          <div >
            <h1>Digite o nome do cliente </h1>
            <v-autocomplete
              class="mt-5"
              v-model="selectedClientID"
              :search-input.sync="nomeBusca"
              :items="getAllClients"
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
              :items="getAllClients"
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
              :items="getAllClients"
              dense
              label="Endereço do Cliente"
              item-text="address"
              item-value="pk"
            ></v-autocomplete>
          </div>
        </v-tab-item>
      </v-tabs-items>
      <div class="col-6">
        <v-card>
          <v-card-title>
              <v-text-field
                :rules=regraNomeCliente
                v-model=selectedClientInfo.name
                :disabled=!editarCliente
              ></v-text-field>
            <v-spacer />

            <v-btn
              v-if="!editarCliente"
              :disabled="!selectedClientID"
              fab
              depressed
              @click="editarCliente = !editarCliente">
              <v-icon>
                mdi-pencil
              </v-icon>
            </v-btn>

            <v-btn
              v-else
              fab
              depressed
              @click="editarCliente = !editarCliente">
              <v-icon>mdi-close</v-icon>
            </v-btn>

          </v-card-title>
          <v-card-text>
            Telefone:
            <v-text-field
              :rules=regraTelefone
              v-model=selectedClientInfo.phone
              :disabled=!editarCliente
              v-mask="'(##) ##### - ####'"
              >
            </v-text-field>
            Endereço Principal:
            <v-textarea
              :disabled=!editarCliente
              v-model=selectedClientInfo.address
            >
            </v-textarea>
            <div class="d-flex justify-end">
              Último Pedido: {{ selectedClientInfo.last_order }} <br />
            </div>
          </v-card-text>
          <v-card-actions >
            <v-btn
              v-if="editarCliente && selectedClientID"
              color="warning"
              @click="deleteClient">
              Excluir Cliente
            </v-btn>
            <v-spacer />
            <v-btn
              v-if="!editarCliente"
              color="primary"
              x-large
              :disabled="!selectedClientID">Ver Pedidos</v-btn>
            <v-btn v-else color="primary" x-large @click="updateClient">Salvar Alterações</v-btn>
          </v-card-actions>
        </v-card>
      </div>
    </v-card-text>

    <v-card-actions class="justify-center">
      <v-dialog max-width="95%">
        <template v-slot:activator="{ on, attrs }">
          <v-btn class="flex-fill mx-2"
            x-large
            color="primary"
            v-bind="attrs" v-on="on">Cadastrar novo Cliente</v-btn>
        </template>

        <template v-slot:default="dialog">
          <v-card class="pa-8" height="90vh">
              <v-card-title class="justify-end">
                <h2>Cadastrar Cliente</h2>
                <v-spacer />
                <v-btn
                text
                fab
                @click="dialog.value=false">
                  <v-icon>mdi-close</v-icon>
                </v-btn>
              </v-card-title>
            <novo-cliente-form :dialog="() => dialog.value = false"/>
          </v-card>
        </template>
      </v-dialog>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex';

import {
  regraNomeCliente,
  regraTelefone,
  regraTexto,
} from '../regras_input';
import { formatAddress } from '../functions';
import NovoClienteForm from './Forms/NovoClienteForm.vue';

export default {
  components: { NovoClienteForm },
  name: 'Configuracoes',
  computed: mapGetters(['getAllClients']),
  data() {
    return {
      tab: null,
      text: 'Beluga',
      regraNomeCliente,
      regraTelefone,
      regraTexto,
      telefoneBusca: '',
      enderecoBusca: '',
      nomeBusca: '',
      selectedClientID: null,
      selectedClientInfo: {
        name: '',
        pk: null,
        phone: '',
        address: '',
        last_order: '',
      },
      editarCliente: false,
    };
  },
  methods: {
    clearSelectedClient() {
      this.selectedClientID = null;
      this.selectedClientInfo = {
        name: '',
        pk: null,
        phone: '',
        address: '',
        last_order: '',
      };
      this.editarCliente = false;
      this.nomeBusca = '';
      this.telefoneBusca = '';
      this.enderecoBusca = '';
    },
    updateClient() {
      this.$store.dispatch('updateClient', { client: this.selectedClientInfo, clientID: this.selectedClientID, callback: this.onEdit });
    },
    deleteClient() {
      this.$store.dispatch('deleteClient', { clientID: this.selectedClientID, callback: this.onDelete });
    },
    onDelete() {
      this.clearSelectedClient();
    },
    onEdit() {

    },
  },
  watch: {
    selectedClientID: function onChange(val) {
      if (!val) {
        return null;
      }
      const obj = this.$store.getters.getAllClients.find(
        (item) => item.pk === val,
      );
      this.selectedClientInfo = {
        name: obj.name,
        phone: obj.phone_format,
        address: formatAddress(obj),
        last_order: 'Nunca',
      };
      return val;
    },
  },
};
</script>

<style>
</style>
