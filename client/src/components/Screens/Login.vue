<template>
   <v-app id="inspire">
      <v-main>
         <v-container fluid fill-height>
            <v-layout align-center justify-center>
               <v-flex xs12 sm8 md5>
                  <v-card class="elevation-12">
                    <v-toolbar class="elevation-0" dark color="primary">
                      <v-card-title>
                        <v-toolbar-title>Login Form</v-toolbar-title>
                      </v-card-title>
                    </v-toolbar>
                     <v-card-text class="pa-5">
                      <message></message>
                        <v-form>
                           <v-text-field
                            filled
                            name="username"
                            label="Username"
                            type="text"
                            v-model="username"
                            v-on:keydown.enter='loginUser'
                            required
                           ></v-text-field>
                           <v-text-field
                            filled
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
                     <v-card-actions class="flex-column pl-5 pr-5">
                        <v-btn
                        class="login-btn"
                        block
                        type="submit"
                        color="primary"
                        x-large
                        @click="loginUser">Login</v-btn>
                        <v-btn
                        class="mt-5 mb-2 mr-auto"
                        small
                        text
                        link
                        :to="{name:'EsqueciSenha'}"
                        @click="clearMessages()"> Esqueci minha Senha</v-btn>
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

<style scoped>
.login-form {
  width: 100%;
}

.login-btn {
  width: 80%;
}

</style>
