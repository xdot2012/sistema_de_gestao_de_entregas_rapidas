<template>
  <v-app id="inspire">
    <v-main>
        <v-container fluid >
          <v-layout align-center justify-start flex-column>
              <h1 class="mt-2 ml-2">A Página não foi Encontrada!</h1>
              <v-btn class="mt-5" link :to="{name:'Painel'}">Voltar</v-btn>
          </v-layout>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'PageNotFound',
};
</script>
