<template>
   <v-app id="inspire">
      <v-main>
         <v-container fluid fill-height>
            <v-layout align-center justify-center>
               <v-flex xs12 sm8 md4>
                  <v-card class="elevation-12">
                     <v-toolbar dark color="primary">
                        <v-toolbar-title>Login form</v-toolbar-title>
                     </v-toolbar>
                     <v-card-text>
                      <message></message>
                        <v-form>
                           <v-text-field
                              name="username"
                              label="Username"
                              type="text"
                              v-model="username"
                              v-on:keydown.enter='loginUser'
                              required
                           ></v-text-field>
                           <v-text-field
                              id="password"
                              name="password"
                              label="Password"
                              type="password"
                              v-model="password"
                              v-on:keydown.enter='loginUser'
                              required
                           ></v-text-field>
                        </v-form>
                     </v-card-text>
                     <v-card-actions>
                        <v-btn text link :to="{name:'EsqueciSenha'}"> Esqueci minha Senha</v-btn>
                        <v-spacer></v-spacer>
                        <v-btn type="submit" color="primary" @click="loginUser">Login</v-btn>
                     </v-card-actions>
                  </v-card>
               </v-flex>
            </v-layout>
         </v-container>
      </v-main>
   </v-app>
</template>

<script>
import { mapGetters } from 'vuex';
import Message from '../Navigation/Message.vue';

export default {
  components: { Message },
  name: 'LoginForm',
  computed: mapGetters(['getAlertType', 'getMessage']),
  data() {
    return {
      username: null,
      password: null,
      message: 'asdasdas',
    };
  },
  methods: {
    async loginUser() {
      this.$store.dispatch('login', { username: this.username, password: this.password });
    },
  },
};
</script>
