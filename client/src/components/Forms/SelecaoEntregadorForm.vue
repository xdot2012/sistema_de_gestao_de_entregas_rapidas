<template>
  <div class="d-flex">
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
</template>

<script>
export default {
  name: 'EntregaForm',
  data: () => ({
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
  }),
  methods: {
    selecionaEntregador(entregador) {
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
  },
};
</script>
