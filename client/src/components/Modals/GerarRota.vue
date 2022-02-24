<template>
  <v-dialog>
      <template v-slot:activator="{ on, attrs }">
        <v-btn class="flex-fill mx-2"
          x-large
          color="primary"
          v-bind="attrs" v-on="on">Gerar Rota</v-btn>
      </template>

      <template v-slot:default="dialog">
        <v-card class="pa-8 d-flex flex-column" width="100vw" Resumo min-height="90vh">
          <v-card-title class="d-flex">
              <div class="text-h5">Gerar Rota</div>
              <v-spacer />
              <v-btn icon text @click="dialog.value = false">
                <v-icon>mdi-close</v-icon>
              </v-btn>
          </v-card-title>

          <v-card-text  class="flex-fill">
            <div v-if="!etapaPedido" class="d-flex">
              <div class="d-flex flex-column flex-fill" >
                <h2 class="text-center">X Pedidos em Espera</h2>
                <h3>Selecione Entregadores:</h3>
                <div class="d-flex flex-column">
                  <v-checkbox
                    :label="'Selecionar Todos'"
                    v-model="todosEntregadores"
                    @change="selecionaTodos()"/>
                  <v-checkbox
                    v-for="entregador in listaEntregadores" :key="entregador.id"
                    :label="entregador.nome"
                    v-model="entregador.selecionado"
                    @change="selecionaEntregador(entregador)"/>
                  </div>
                <h2 class="text-center">Capacidade Total: {{capacidadeTotal}} Produtos</h2>
              </div>
            </div>

            <div v-else-if="etapaPedido==1">
              <div class="d-flex">
                <div class="d-flex flex-column" style="width: 25%; height: 100%">
                  <h3>Seleção de Pedidos:</h3>
                    <v-radio-group v-model="metodoSelecaoPedidos">
                      <v-radio
                        @click="tempoDeEspera()"
                        label="Priorizar Tempo de Espera"
                        value="tempo_espera" />
                      <v-radio
                        @click="rotaMaisCurta()"
                        label="Priorizar Rota Mais Curta"
                        value="rota_mais_curta" />
                      <v-radio
                        label="Selecao Manual"
                        value="selecao_manual" />
                    </v-radio-group>
                </div>

                <div class="ml-auto d-flex justify-end" style="width:70%">
                  <v-simple-table>
                    <thead>
                      <tr>
                        <th>Selecionado</th>
                        <th>Pedido</th>
                        <th class="text-center"># Produtos</th>
                        <th>Distância</th>
                        <th>Tempo de Espera</th>
                        <th></th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="item in listaPedidos" :key=item.id>
                        <td>
                          <v-checkbox
                            v-model="item.selecionado"
                            :disabled="metodoSelecaoPedidos!='selecao_manual'"
                            @click="adicionaItem(item)"
                            />
                          </td>
                        <td>{{item.nome}}</td>
                        <td>{{item.quantidade}}</td>
                        <td>{{item.distancia}}</td>
                        <td>{{item.tempo_espera}}</td>
                      </tr>
                    </tbody>
                  </v-simple-table>
                </div>
              </div>
              <h2 class="mt-auto text-center">{{produtosSelecionados}} Produtos Selecionados</h2>
            </div>

            <div v-else-if="etapaPedido==2" >
              <h1 class="text-center">Rota Gerada com Sucesso!</h1>
              <v-simple-table>
                <thead>
                  <tr>
                    <th>Entregador</th>
                    <th>Pedido</th>
                    <th>Cliente</th>
                    <th>Endereço</th>
                    <th>Produtos</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="item in listaItems" :key="item.id">
                    <td>{{ item.entregador }}</td>
                    <td>{{ item.pedido }}</td>
                    <td>{{ item.cliente }}</td>
                    <td>{{ item.endereco }}</td>
                    <td>{{ item.produtos  }}</td>
                    </tr>
                </tbody>
              </v-simple-table>
            </div>
          </v-card-text>

          <v-card-actions class="justify-end mt-auto">
            <v-btn v-if="etapaPedido>0"
              x-large
              color="primary"
              @click="voltarEtapa(etapaPedido)">Voltar</v-btn>
            <v-spacer></v-spacer>
            <v-btn v-if="etapaPedido<=1"
              x-large
              color="primary"
              @click="proximaEtapa(etapaPedido)">Próximo</v-btn>
            <div v-else>
              <v-btn
                class="mr-5"
                x-large
                color="primary"
                @click="imprimeRota()">
                Imprimir Rota</v-btn>
              <v-btn
                x-large
                color="primary"
                @click="dialog.value = finalizarPedido()">
                Finalizar Pedido</v-btn>
            </div>
          </v-card-actions>
        </v-card>
      </template>
  </v-dialog>
</template>

<script>

export default {
  name: 'GerarRota',
  data: () => ({
    etapaPedido: 0,
    metodoPagamento: null,
    tipoEntrega: null,
    todosEntregadores: false,
    capacidadeTotal: 0,
    listaEntregadores: [
      {
        id: 1,
        nome: 'Josué',
        capacidade: '10',
        selecionado: null,
      },
      {
        id: 2,
        nome: 'Fernando',
        capacidade: '10',
        selecionado: null,
      },
      {
        id: 3,
        nome: 'Maria',
        capacidade: '10',
        selecionado: null,
      },
    ],
    nPedidos: 0,
    produtosSelecionados: 0,
    listaPedidos: [
      {
        selecionado: null, nome: 'Pedido1', quantidade: 2, distancia: '1km', tempo_espera: '30 min',
      },
      {
        selecionado: null, nome: 'Pedido1', quantidade: 2, distancia: '1km', tempo_espera: '30 min',
      },
    ],
    metodoSelecaoPedidos: null,
    listaItems: [{
      id: 1, entregador: 'Carlos', pedido: '123', cliente: 'José Pereira da Silva', endereco: 'Rua x, Bairro Y - Nº123', produtos: '1 Feijão com Batata',
    },
    {
      id: 2, entregador: 'José', pedido: '321', cliente: 'José Pereira da Silva', endereco: 'Rua x, Bairro Y - Nº123', produtos: '1 Feijão com Batata',
    },
    ],
  }),
  methods: {
    finalizarPedido() {
      this.etapaPedido = 0;
      this.confirmaPedido = true;
      return false;
    },
    proximaEtapa(etapaPedido) {
      this.etapaPedido = etapaPedido + 1;
    },
    voltarEtapa(etapaPedido) {
      this.etapaPedido = etapaPedido - 1;
    },
    imprimeRota() {
      return false;
    },
    elecionaEntregador(entregador) {
      if (!entregador.selecionado) {
        this.todosEntregadores = false;
        this.capacidadeTotal -= parseInt(entregador.capacidade, 10);
        return;
      }
      this.capacidadeTotal += parseInt(entregador.capacidade, 10);
    },
    selecionaTodos() {
      this.capacidadeTotal = 0;
      let count = 0;
      this.listaEntregadores = this.listaEntregadores.map((elem) => {
        count += parseInt(elem.capacidade, 10);
        return {
          id: elem.id,
          nome: elem.nome,
          capacidade: elem.capacidade,
          selecionado: this.todosEntregadores,
        };
      });
      if (this.todosEntregadores) {
        this.capacidadeTotal = count;
      }
    },
    adicionaItem(item) {
      if (item.selecionado) {
        this.produtosSelecionados += item.quantidade;
      } else {
        this.produtosSelecionados -= item.quantidade;
      }
    },
    rotaMaisCurta() {
      this.produtosSelecionados = 0;
      this.listaPedidos = this.listaPedidos.map((elem) => {
        this.produtosSelecionados += elem.quantidade;
        return {
          id: elem.id,
          nome: elem.nome,
          quantidade: elem.quantidade,
          distancia: elem.distancia,
          tempo_espera: elem.tempo_espera,
          selecionado: true,
        };
      });
    },
    tempoDeEspera() {
      this.produtosSelecionados = 0;
      this.listaPedidos = this.listaPedidos.map((elem) => {
        this.produtosSelecionados += elem.quantidade;
        return {
          id: elem.id,
          nome: elem.nome,
          quantidade: elem.quantidade,
          distancia: elem.distancia,
          tempo_espera: elem.tempo_espera,
          selecionado: true,
        };
      });
    },
  },
};
</script>

<style>
</style>
