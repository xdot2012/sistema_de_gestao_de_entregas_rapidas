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
              v-model="nomeBusca"
              :items="clientLista"
              dense
              label="Cliente"
            ></v-autocomplete>
          </div>
        </v-tab-item>
        <v-tab-item value="tab-2">
            <div>
            <h1>Digite o número de Telefone</h1>
            <v-autocomplete
              v-model="telefoneBusca"
              :items="clientLista"
              label="Digite o Número"
            ></v-autocomplete>
          </div>
        </v-tab-item>
        <v-tab-item value="tab-3">
          <div>
            <h1>Digite o Endereço</h1>
            <v-autocomplete
              v-model="enderecoBusca"
              :items="clientLista"
              label="Digite o Número"
            ></v-autocomplete>
          </div>
        </v-tab-item>
      </v-tabs-items>
      <div class="col-6">
        <v-card>
          <v-card-title>
              <v-text-field
                :rules=regraNomeCliente
                v-model=clientInfo.nome
                :disabled=!editarCliente
              ></v-text-field>
            <v-spacer />
            <v-btn
              fab
              depressed
              @click="editarCliente = !editarCliente">
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-text>
            Telefone:
            <v-text-field
              :rules=regraTelefone
              v-model=clientInfo.telefone
              :disabled=!editarCliente
              v-mask="'(##) ##### - ####'"
              >
            </v-text-field>
            Endereço Principal:
            <v-text-field
              :rules=regraTexto
              :disabled=!editarCliente
              v-model=clientInfo.endereco
            >
            </v-text-field>
            <div class="d-flex justify-end">
              Último Pedido: {{ clientInfo.ultimo_pedido }} <br />
            </div>
          </v-card-text>
          <v-card-actions >
            <v-btn v-if="editarCliente" color="warning">Excluir Cliente</v-btn>
            <v-spacer />
            <v-btn color="primary" x-large>Ver Pedidos</v-btn>
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
import {
  regraNomeCliente,
  regraTelefone,
  regraTexto,
} from '../../regras_input';
import NovoClienteForm from './NovoClienteForm.vue';

export default {
  components: { NovoClienteForm },
  name: 'Configuracoes',
  data() {
    return {
      tab: null,
      text: 'Beluga',
      regraNomeCliente,
      regraTelefone,
      regraTexto,
      telefoneBusca: null,
      enderecoBusca: null,
      nomeBusca: null,
      clientLista: [
        'Carlos',
        'Geralda',
        'Maria',
      ],
      clientInfo: {
        nome: 'Geralda Pereira da Silva',
        telefone: '(99) 99999-9999',
        endereco: 'Rua x, Bairro y. Cidade XYZ/XX',
        ultimo_pedido: '02/01/2022',
      },
      editarCliente: false,
    };
  },
};
</script>

<style>
</style>
