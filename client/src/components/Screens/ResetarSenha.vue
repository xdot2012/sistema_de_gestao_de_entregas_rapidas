<template>
   <v-app id="inspire">
      <v-main>
         <v-container fluid fill-height>
            <v-layout align-center justify-center>
               <v-flex xs12 sm8 md4>
                  <v-card class="elevation-12">
                     <v-toolbar dark color="primary">
                        <v-toolbar-title>Redefinir Senha</v-toolbar-title>
                     </v-toolbar>
                     <v-card-text>
                      <message></message>
                        <div>
                            <v-text-field
                              name="senha"
                              label="Digite a nova Senha"
                              type="password"
                              v-model="password"
                              v-on:keydown.enter='redefinirSenha'
                              required
                           ></v-text-field>
                        </div>
                     </v-card-text>
                     <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                        color="primary"
                        @click="redefinirSenha">Enviar Email</v-btn>
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
      password: null,
    };
  },
  methods: {
    redefinirSenha() {
      const parameters = this.$route.query;
      this.$store.dispatch('resetPassword', { token: parameters.token, password: this.password });
    },
  },
};
</script>
