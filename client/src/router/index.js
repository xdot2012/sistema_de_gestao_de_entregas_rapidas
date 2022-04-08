import Vue from 'vue';
import Router from 'vue-router';
import Container from '../components/Navigation/Container.vue';

import Painel from '../components/Screens/Painel.vue';
import Configuracoes from '../components/Screens/Configuracoes.vue';
import Historico from '../components/Screens/Historico.vue';
import Login from '../components/Screens/Login.vue';
import PageNotFound from '../components/Screens/PageNotFound.vue';
import EsqueciMinhaSenha from '../components/Screens/EsqueciMinhaSenha.vue';

Vue.use(Router);

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      // Navigation
      path: '',
      component: Container,
      meta: {
        requiresAuth: true,
      },
      children: [
        {
          name: 'Painel',
          path: '/',
          component: Painel,
        },
        {
          name: 'Configuracoes',
          path: '/configuracoes',
          component: Configuracoes,
        },
        {
          name: 'Historico',
          path: '/historico',
          component: Historico,
        },
      ],
    },
    {
      path: '/auth',
      name: 'Login',
      component: Login,
    },
    {
      path: '/redefinirSenha',
      name: 'RedefinirSenha',
      component: EsqueciMinhaSenha,
    },
    {
      path: '*',
      component: PageNotFound,
    },
  ],
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  if (to.matched.some((record) => record.meta.requiresAuth) && !token) {
    next({ name: 'Login' });
    return;
  }
  next();
});

export default router;
