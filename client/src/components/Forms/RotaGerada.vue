<template>
  <div>
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
</template>

<script>
export default {
  name: 'RotaGerada',
  data: () => ({
    metodoPagamento: null,
    listaItems: [{
      id: 1, entregador: 'Carlos', pedido: '123', cliente: 'José Pereira da Silva', endereco: 'Rua x, Bairro Y - Nº123', produtos: '1 Feijão com Batata',
    },
    {
      id: 2, entregador: 'José', pedido: '321', cliente: 'José Pereira da Silva', endereco: 'Rua x, Bairro Y - Nº123', produtos: '1 Feijão com Batata',
    },
    ],
  }),
};
</script>
