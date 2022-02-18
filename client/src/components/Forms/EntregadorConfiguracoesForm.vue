<template>
    <v-card class="pa-8">
    <v-card-title class="d-flex ">
      <div class="text-h5">Entregadores</div>
    </v-card-title>

    <v-card-text class="d-flex">
      <div class="col-6">
        <h1>Selecione o Entregador</h1>
        <v-select
          :items="entregadoresLista"
          label="Entregador"
        ></v-select>
      </div>
      <div class="col-6">
        <v-card>
          <v-card-title>
              <v-text-field
                :rules=regraNomeCliente
                v-model=entregadorInfo.nome
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
              v-model=entregadorInfo.telefone
              :disabled=!editarentregador
              v-mask="'(##) ##### - ####'"
              >
            </v-text-field>
            Tipo de Veículo:
            <v-select
              :items="tiposVeiculo"
              :rules=regraTexto
              :disabled=!editarentregador
              v-model=entregadorInfo.tipo_veiculo
            >
            </v-select>
            Capacidade do Veículo:
            <v-text-field
              :rules=regraNumero
              v-model=entregadorInfo.capacidade
              :disabled=!editarentregador
            >
            </v-text-field>
            <div class="d-flex justify-end">
              Última Entrega: {{ entregadorInfo.ultimo_pedido }} <br />
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
  data() {
    return {
      tiposVeiculo: [
        'Carro',
        'Moto',
        'Bicicleta',
      ],
      regraNumero,
      regraNomeCliente,
      regraTelefone,
      regraTexto,
      entregadoresLista: [
        'Carlos',
        'Geralda',
        'Maria',
      ],
      entregadorInfo: {
        nome: 'Geralda Pereira da Silva',
        telefone: '(99) 99999-9999',
        tipo_veiculo: 'Moto',
        ultimo_pedido: '02/01/2022',
        capacidade: 10,
      },
      editarentregador: false,
    };
  },
};
</script>

<style>
</style>
