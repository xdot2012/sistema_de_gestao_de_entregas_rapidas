<template>
  <div>
    <v-divider></v-divider>
    <h2 class="mt-2">Informações do Entregador</h2>
    <div class="d-flex">
      <v-text-field class="mr-2"
      label="Nome"
      :rules="regraNomeCliente"
      v-model="nome"
      hide-details="auto"></v-text-field>

      <v-text-field label="Telefone"
      :rules="regraTelefone"
      v-model="telefone"
      v-mask="'(##) ##### - ####'"
      hide-details="auto"></v-text-field>
    </div>

    <v-divider class="mt-3"></v-divider>
    <h2 class="mt-1">Tipo de Veículo</h2>
    <div class="d-flex">
      <v-select
        :items="tiposVeiculo"
        v-model="veiculo"></v-select>
    </div>

    <v-text-field label="Capacidade do Veículo"
    :rules="regraNumero"
    v-model="capacidade"
    hide-details="auto"></v-text-field>

  </div>
</template>

<script>
import {
  regraTelefone,
  regraNomeCliente,
  regraNumero,
} from '../../regras_input';

export default {
  name: 'NovoClienteForm',
  data: () => ({
    tiposVeiculo: [
      'Carro',
      'Moto',
      'Bicicleta',
    ],
    nome: null,
    telefone: null,
    capacidade: null,
    veiculo: null,
    regraNomeCliente,
    regraTelefone,
    regraNumero,
  }),
};
</script>
