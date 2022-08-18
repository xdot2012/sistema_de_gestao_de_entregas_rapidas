<template>
    <v-form
      ref="form"
      v-model="valid"
      lazy-validation>
    <h2 class="mt-2">Informações do Entregador</h2>
    <v-row>
      <v-text-field class="mr-2"
      label="Nome"
      :rules="regraNomeCliente"
      v-model="name"
      hide-details="auto"
      required></v-text-field>

      <v-text-field label="Telefone"
      :rules="regraTelefone"
      v-model="phone"
      v-mask="'(##)#####-####'"
      hide-details="auto"
      required></v-text-field>
    </v-row>

    <v-divider class="mt-3"></v-divider>
    <h2 class="mt-1">Tipo de Veículo</h2>
    <v-row>
      <v-select
        :items="tiposVeiculo"
        v-model="vehicle_type"
        required></v-select>

        <v-text-field label="Capacidade do Veículo"
        :rules="regraNumero"
        v-model="capacity"
        hide-details="auto"
        required></v-text-field>
    </v-row>

    <v-row class="d-flex align-end justify-end fill-height">
      <v-btn
        :disabled="!valid"
        color="primary"
        x-large
        @click="validate">
          Cadastrar Entregador
      </v-btn>
    </v-row>

  </v-form>
</template>

<script>
import {
  regraTelefone,
  regraNomeCliente,
  regraNumero,
} from '../../regras_input';

export default {
  name: 'NovoClienteForm',
  props: ['dialog'],
  data: () => ({
    valid: null,
    tiposVeiculo: [
      'CAR',
      'MOTORCYCLE',
      'BIKE',
    ],
    name: null,
    phone: null,
    capacity: null,
    vehicle_type: null,
    regraNomeCliente,
    regraTelefone,
    regraNumero,
  }),
  methods: {
    callback() {
      this.reset();
      this.dialog();
    },
    validate() {
      if (this.$refs.form.validate()) {
        this.criarEntregador();
      }
    },
    reset() {
      this.$refs.form.reset();
    },
    resetValidation() {
      this.$refs.form.resetValidation();
    },
    criarEntregador() {
      const formatPhone = this.phone.replace(' ', '').replace('(', '').replace(')', '').replace('-', '');
      const deliveryman = {
        name: this.name,
        phone: formatPhone,
        vehicle_type: this.vehicle_type,
        capacity: this.capacity,
      };
      this.$store.dispatch('createDeliveryman', { deliveryman, callback: this.callback });
    },
  },
};
</script>
