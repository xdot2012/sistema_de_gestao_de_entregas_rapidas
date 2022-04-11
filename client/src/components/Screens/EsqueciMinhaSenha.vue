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
                        <v-form>
                           <v-text-field
                              name="email"
                              label="Digite seu Email"
                              type="text"
                              v-model="email"
                              v-on:keydown.enter='redefinirSenha'
                              required
                           ></v-text-field>
                        </v-form>
                     </v-card-text>
                     <v-card-actions>
                        <v-btn
                        type="submit"
                        link
                        :to="{name:'Login'}">Voltar</v-btn>
                        <v-spacer></v-spacer>
                        <v-btn
                        type="submit"
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
      email: null,
    };
  },
  methods: {
    redefinirSenha() {
      this.$store.dispatch('passwordResetEmail', { email: this.email });
    },
  },
};
</script>
