<template>
    <div class="mt-5">
      <v-radio-group v-model="cliente_pedido" row>
        <v-radio label="Selecionar Cliente" color="primary" value="selecionar_cliente"
        ></v-radio>
        <v-radio label="Novo Cliente" color="primary" value="novo_cliente"
        ></v-radio>
      </v-radio-group>

      <novo-cliente-form v-if="cliente_pedido == 'novo_cliente'" />
      <selecao-cliente-form v-else />
  </div>
</template>

<script>
import NovoClienteForm from './NovoClienteForm.vue';
import SelecaoClienteForm from './SelecaoClienteForm.vue';

export default {
  components: { NovoClienteForm, SelecaoClienteForm },
  name: 'NovoCliente',
  data: () => ({
    cliente_pedido: 'selecionar_cliente',
  }),
};
</script>
