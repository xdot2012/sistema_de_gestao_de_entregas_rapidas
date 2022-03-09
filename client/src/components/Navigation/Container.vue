<template>
  <v-app>
  <v-navigation-drawer app v-model="drawer" absolute temporary class="sticky">
    <div class="drawer-content d-flex flex-column fill-height">
      <v-btn link :to="{name:'Painel'}" @click="drawer=false"
        x-large class="drawer-button mt-5" small color="primary">PAINEL</v-btn>
      <v-btn link :to="{name:'Historico'}" @click="drawer=false"
        x-large class="drawer-button" small color="primary">HISTÓRICO</v-btn>
      <v-btn link :to="{name:'Configuracoes'}" @click="drawer=false"
        x-large class="drawer-button" small color="primary">CONFIGURAÇÕES</v-btn>
      <v-spacer></v-spacer>
      <v-btn @click="logout"
       x-large class="drawer-button mb-5" small color="primary">SAIR</v-btn>

    </div>
  </v-navigation-drawer>

  <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>FoodBoard</v-toolbar-title>

      <v-spacer></v-spacer>

      <div class="head-container">
        <v-sheet light class="head-card flex-fill"
        color="white" elevation="1" height="80%" rounded width="100">
          <div class="head-dot red"></div>
          <div class="head-card-text">Atrasado: {{lateOrders.length}}</div>
        </v-sheet>
        <v-sheet light
          class="head-card flex-fill" color="white" elevation="1" height="80%" rounded width="100">
          <div class="head-dot yellow"></div>
          <div class="head-card-text">Aguardando: {{warnOrders.length - lateOrders.length}}</div>

        </v-sheet>
        <v-sheet light
          class="head-card flex-fill" color="white" elevation="1" height="80%" rounded width="100">
          <div class="head-dot green"></div>
          <div class="head-card-text">A Caminho: {{inRouteOrders.length}}</div>
        </v-sheet>
      </div>
  </v-app-bar>

  <!-- Sizes your content based upon application components -->
  <v-main>
    <message class="sticky mr-5 ml-5 mt-2 mb-2"></message>
    <!-- Provides the application the proper gutter -->
    <v-container fluid>
      <router-view></router-view>
    </v-container>
  </v-main>

</v-app>
</template>

<script>
import { mapGetters } from 'vuex';

import Message from './Message.vue';

export default {
  components: { Message },
  name: 'Container',
  computed: mapGetters(['inRouteOrders', 'lateOrders', 'warnOrders']),
  data() {
    return {
      drawer: null,
      items: [
        { title: 'Home', icon: 'mdi-view-dashboard' },
        { title: 'About', icon: 'mdi-forum' },
      ],
    };
  },
  methods: {
    logout() {
      this.drawer = null;
      this.$store.dispatch('logout');
    },
  },
};
</script>

<style scoped>
  .head-container {
    height: 80%;
    width: 60%;
    margin-left: 2rem;
    display: flex;
    flex-direction: row;
    align-items: center;
  }

  .head-card {
    margin-left: 10px;
    display: flex;
    flex-direction: row;
    align-items: center;
  }

  .head-dot {
    margin-left: 5px;
    height: 30px;
    width: 30px;
    border-radius: 50%;
  }

  .head-dot .red {
    background-color: red;
  }

  .head-dot .green {
    background-color: green;
  }

  .head-dot .yellow {
    background-color: yellow;
  }

  .head-card-text {
    margin-left: 1rem;
  }

  .drawer-button {
    width:95%;
    margin-left: 2.5%;
    margin-top: 0.5rem;
  }

  .a {
  text-decoration: none;
  }

  .container {
    max-width: none;
  }

  .sticky {
    position: fixed;
    width: 97.5%;
    z-index:777;
  }
  </style>
