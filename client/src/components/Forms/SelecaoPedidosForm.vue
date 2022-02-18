<template>
  <div>
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
</template>

<script>
export default {
  name: 'SelecaoPedidosForm',
  data: () => ({
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
  }),
  methods: {
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
