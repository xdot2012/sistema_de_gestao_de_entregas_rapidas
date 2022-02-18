<template>
  <div class="d-flex">
    <div class="d-flex flex-column" style="width: 25%; height: 100%">
      <v-simple-table>
        <thead>
          <tr>
            <th colspan="3" class="mb-5 text-center primary white--text">
              <h2>Resumo do Pedido</h2>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in pedidoCliente" :key=item.id>
            <td>{{item.nome}}</td>
            <td>{{item.quantidade}}</td>
            <td>
              <v-btn
                @click="removeItem(item.id)"
                color="gray"
                icon
                small>
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </td>
          </tr>
        </tbody>
      </v-simple-table>
    </div>

    <div class="ml-10 d-flex justify-start flex-fill">
      <div class="d-flex flex-column flex-fill" >
        <h2>Resumo do Pedido:</h2>
        <v-divider />
        <h3>Cliente:</h3>
        <div class="d-flex justify-space-between">
          <h3>Nome do Cliente</h3>
          <h3>Telefone do Cliente</h3>
        </div>
        <v-divider />
        <div class="d-flex flex-column">
          <h3>Endereço de Entrega:</h3>
          <div class="d-flex justify-space-between">
            <h3>Rua</h3>
            <h3>Número</h3>
          </div>
          <div class="d-flex justify-space-between">
            <h3>Bairro</h3>
            <h3>Cidade</h3>
          </div>
        </div>
        <v-divider />
        <div class="d-flex justify-start">
          <div class="d-flex flex-column">
            <h3>Método de Pagamento:</h3>
              <v-radio-group v-model="metodoPagamento">
                <v-radio label="Já pago" value="pago"></v-radio>
                <v-radio label="Cartão Crédito" value="cartao_credito"></v-radio>
                <v-radio label="Cartão Débito" value="cartao_debito"></v-radio>
                <v-radio label="Dinheiro" value="dinheiro"></v-radio>
                <v-radio label="Pix" value="pix"></v-radio>
              </v-radio-group>
          </div>
          <div class="d-flex flex-column ml-10">
            <h3>Método de Entrega:</h3>
            <v-radio-group v-model="tipoEntrega">
              <v-radio label="Delivery" value="delivery"></v-radio>
              <v-radio label="Agendar Horário" value="agendar_horario"></v-radio>
              <v-radio label="Retirada no Local" value="retirada_local"></v-radio>
            </v-radio-group>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EntregaForm',
  data: () => ({
    metodoPagamento: null,
    tipoEntrega: null,
  }),
};
</script>
