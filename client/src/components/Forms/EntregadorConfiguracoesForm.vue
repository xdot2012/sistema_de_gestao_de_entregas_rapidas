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
              @click="editarentregador = !editarentregador">
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-text>
            Telefone:
            <v-text-field
              :rules=regraTelefone
              v-model=entregadorInfo.phone
              :disabled=!editarentregador
              v-mask="'(##) ##### - ####'"
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
            <v-btn v-if="editarentregador" color="warning">Excluir</v-btn>
            <v-spacer />
            <v-btn color="primary" x-large>Ver Entregas</v-btn>
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
            <novo-entregador-form />
            <v-card-actions class="justify-end">
              <v-btn text @click="dialog.value = false">Close</v-btn>
            </v-card-actions>
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
} from '../../regras_input';
import NovoEntregadorForm from './NovoEntregadorForm.vue';

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
        name: 'Geralda Pereira da Silva',
        phone: '(99) 99999-9999',
        vehicle_type: 'Moto',
        last_order: '02/01/2022',
        capacity: 10,
      },
      entregadorID: null,
      editarentregador: false,
    };
  },
  methods: {
    clearSelectedDeliveryman() {
      this.entregadorID = null;
      this.entregadorInfo = {
        name: 'Geralda Pereira da Silva',
        phone: '(99) 99999-9999',
        vehicle_type: 'Moto',
        last_order: '02/01/2022',
        capacity: 10,
      };
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
      this.clearSelectedDeliveryman();
      this.entregadorInfo = {
        name: obj.name,
        phone: obj.phone_format,
        vehicle_type: obj.vehicle_type,
        capacity: obj.capacity,
        last_order: 'Nunca',
      };
      console.log(this.entregadorInfo);
      return val;
    },
  },
};
</script>

<style>
</style>
