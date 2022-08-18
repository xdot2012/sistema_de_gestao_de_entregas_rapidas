<template>
    <v-card class="pa-8">
    <v-card-title class="d-flex ">
      <div class="text-h5">Entregadores</div>
    </v-card-title>

    <v-card-text class="d-flex">
      <div class="col-6">
        <h1>Selecione o Entregador</h1>
        <v-autocomplete
          v-model="entregadorID"
          :items="getAllDeliveryman"
          label="Entregador"
          item-text="name"
          item-value="pk"
          :search-input.sync="entregadorBusca"
        ></v-autocomplete>
      </div>
      <div class="col-6">
        <v-card>
          <v-card-title>
              <v-text-field
                :rules=regraNomeCliente
                v-model=entregadorInfo.name
                :disabled=!editarentregador
              ></v-text-field>
            <v-spacer />
            <v-btn
              fab
              depressed
              @click="editarentregador = !editarentregador"
              :disabled="!entregadorID">
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-text>
            Telefone:
            <v-text-field
              :rules=regraTelefone
              v-model=entregadorInfo.phone
              :disabled=!editarentregador
              v-mask="'(##)#####-####'"
              >
            </v-text-field>
            Tipo de Veículo:
            <v-select
              :items="tiposVeiculo"
              :rules=regraTexto
              :disabled=!editarentregador
              v-model=entregadorInfo.vehicle_type
            >
            </v-select>
            Capacidade do Veículo:
            <v-text-field
              :rules=regraNumero
              v-model=entregadorInfo.capacity
              :disabled=!editarentregador
            >
            </v-text-field>
            <div class="d-flex justify-end">
              Última Entrega: {{ entregadorInfo.last_order }} <br />
            </div>
          </v-card-text>
          <v-card-actions >
            <v-btn
              v-if="editarentregador"
              color="warning"
              @click="deleteDeliveryman">Excluir</v-btn>
            <v-spacer />
            <v-btn v-if="!editarentregador" color="primary" x-large>Ver Entregas</v-btn>
            <v-btn
              v-else
              color="primary"
              x-large
              @click="updateDeliveryman">Salvar Alterações</v-btn>
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
            v-bind="attrs" v-on="on">Cadastrar novo Entregador</v-btn>
        </template>

        <template v-slot:default="dialog">
          <v-card class=" pa-8">
              <v-card-title class="justify-end">
                <h2>Cadastrar Entregador</h2>
                <v-spacer />
                <v-btn
                text
                fab
                @click="dialog.value=false">
                  <v-icon>mdi-close</v-icon>
                </v-btn>
              </v-card-title>
            <novo-entregador-form :dialog="() => dialog.value = false"/>
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
  regraNumero,
} from '../regras_input';
import NovoEntregadorForm from './Forms/NovoEntregadorForm.vue';

export default {
  components: { NovoEntregadorForm },
  name: 'EntregadorConfiguracaoForm',
  computed: mapGetters(['getAllDeliveryman']),
  data() {
    return {
      tiposVeiculo: [
        'CAR',
        'BYKE',
        'MOTORCYCLE',
      ],
      regraNumero,
      regraNomeCliente,
      regraTelefone,
      regraTexto,
      entregadorBusca: '',
      entregadorInfo: {
        name: '',
        phone: '',
        vehicle_type: '',
        last_order: '',
        capacity: '',
      },
      entregadorID: null,
      editarentregador: false,
    };
  },
  methods: {
    clearSelectedDeliveryman() {
      this.entregadorID = null;
      this.entregadorInfo = {
        name: '',
        phone: '',
        vehicle_type: '',
        last_order: '',
        capacity: '',
      };
      this.editarentregador = false;
    },
    updateDeliveryman() {
      const formatPhone = this.entregadorInfo.phone.replace(' ', '').replace('(', '').replace(')', '').replace('-', '');
      const deliveryman = {
        name: this.entregadorInfo.name,
        phone: formatPhone,
        vehicle_type: this.entregadorInfo.vehicle_type,
        capacity: this.entregadorInfo.capacity,
      };
      this.$store.dispatch('updateDeliveryman', { deliveryman, deliverymanID: this.entregadorID, callback: this.onEdit });
    },
    deleteDeliveryman() {
      this.$store.dispatch('deleteDeliveryman', { deliverymanID: this.entregadorID, callback: this.onDelete });
    },
    onEdit() {
      this.editarentregador = false;
    },
    onDelete() {
      this.clearSelectedDeliveryman();
    },
  },
  watch: {
    entregadorID: function onChange(val) {
      if (!val) {
        return null;
      }
      const obj = this.$store.getters.getAllDeliveryman.find(
        (item) => item.pk === val,
      );
      this.entregadorInfo = {
        name: obj.name,
        phone: obj.phone_format,
        vehicle_type: obj.vehicle_type,
        capacity: obj.capacity,
        last_order: 'Nunca',
      };
      return val;
    },
  },
};
</script>

<style>
</style>
