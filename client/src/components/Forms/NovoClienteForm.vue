<template>
  <div class="d-flex flex-column fill-height" style="max-height: 90%">
    <h2 class="mt-2">Informações do Cliente</h2>
    <v-form
      ref="form"
      v-model="valid"
      lazy-validation>
      <v-row>
        <v-text-field class="mr-2"
        label="Nome Cliente"
        :rules="regraNomeCliente"
        v-model="nomeCliente"
        hide-details="auto"
        required
        ></v-text-field>

        <v-text-field label="Telefone do Cliente"
        :rules="regraTelefone"
        v-model="telefoneCliente"
        v-mask="'(##)#####-####'"
        hide-details="auto"
        required
        ></v-text-field>
      </v-row>

      <v-divider class="mt-3"></v-divider>
      <h2 class="mt-1">Endereço de Entrega</h2>
      <v-row>
        <v-text-field
        class="mr-3"
        style="max-width: 25%"
        label="CEP"
        v-mask="'#####-###'"
        :rules="regraCEP"
        v-model="enderecoEntregaCEP"
        hide-details="auto"
        required
        ></v-text-field>
      </v-row>

      <v-row>
        <v-autocomplete
        class="mr-3"
        label="Rua"
        v-model="enderecoEntregaRua"
        :items="opcoesRua"
        dense
        filled
        required
        :rules="[v => !!v || 'Item is required']"
        ></v-autocomplete>

        <v-text-field
        class="mr-3"
        style="max-width: 10%"
        label="Número"
        :rules="regraNumero"
        v-model="enderecoEntregaNumero"
        hide-details="auto"
        required
        ></v-text-field>
      </v-row>

      <v-row>
        <v-autocomplete
        class="mr-3"
        style="max-width: 30%"
        label="Bairro"
        v-model="enderecoEntregaBairro"
        :items="opcoesBairro"
        dense
        filled
        :rules="[v => !!v || 'Item is required']"
        ></v-autocomplete>
        <v-autocomplete
        v-model="enderecoEntregaCidadeEstado"
        :items="opcoesCidadeEstado"
        dense
        filled
        label="Cidade/Estado"
        :rules="[v => !!v || 'Item is required']"
        ></v-autocomplete>
      </v-row>

      <v-row>
        <v-text-field
        class="mr-3"
        label="Referência"
        v-model="enderecoEntregaReferencia"
        hide-details="auto"
        ></v-text-field>
      </v-row>

      <v-row class="d-flex align-end justify-end fill-height">
          <v-btn
            :disabled="!valid"
            color="primary"
            x-large
            @click="validate">
              Cadastrar Cliente
          </v-btn>
      </v-row>
    </v-form>
  </div>
</template>

<script>
import {
  regraTelefone,
  regraNomeCliente,
  regraNumero,
  regraCEP,
  regraTexto,
} from '../../regras_input';

export default {
  name: 'NovoClienteForm',
  props: ['dialog'],
  data: () => ({
    valid: false,
    clienteSelecao: null,
    nomeCliente: null,
    telefoneCliente: null,
    enderecoEntregaCidadeEstado: null,
    enderecoEntregaNumero: null,
    enderecoEntregaRua: null,
    enderecoEntregaBairro: null,
    enderecoEntregaCEP: null,
    enderecoEntregaReferencia: null,
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
    regraTexto,
  }),
  methods: {
    callback() {
      this.reset();
      this.dialog();
    },
    validate() {
      if (this.$refs.form.validate()) {
        this.criarCliente();
      }
    },
    reset() {
      this.$refs.form.reset();
    },
    resetValidation() {
      this.$refs.form.resetValidation();
    },
    criarCliente() {
      const formatPhone = this.telefoneCliente.replace(' ', '').replace('(', '').replace(')', '').replace('-', '');
      const client = {
        name: this.nomeCliente,
        phone: formatPhone,
        number: this.enderecoEntregaNumero,
        street: this.enderecoEntregaRua,
        district: this.enderecoEntregaBairro,
        code: this.enderecoEntregaCEP,
        country_name: this.enderecoEntregaCidadeEstado,
        state_name: this.enderecoEntregaCidadeEstado,
        city_name: this.enderecoEntregaCidadeEstado,
        reference: this.enderecoEntregaReferencia,
      };
      this.$store.dispatch('createClient', { client, callback: this.callback });
    },
  },
};
</script>
