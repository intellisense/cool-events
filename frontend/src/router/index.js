import Vue from 'vue';
import Router from 'vue-router';
import store from '@/store';
import { Types } from '@/store/modules/auth/types';
import Login from '../pages/Login';
import Home from '../pages/Home';
import Signup from '../pages/Signup';

const requireAuthenticated = (to, from, next) => {
  store.dispatch(Types.actions.INITIALIZE)
    .then(() => {
      if (!store.getters[Types.getters.IS_AUTHENTICATED]) {
        next({ name: 'Login' });
      } else {
        next();
      }
    });
};

const requireUnauthenticated = (to, from, next) => {
  store.dispatch(Types.actions.INITIALIZE)
    .then(() => {
      if (store.getters[Types.getters.IS_AUTHENTICATED]) {
        next({ name: 'Home' });
      } else {
        next();
      }
    });
};

const redirectLogout = (to, from, next) => {
  store.dispatch(Types.actions.LOGOUT)
    .then(() => next({ name: 'Login' }));
};

Vue.use(Router);

export default new Router({
  saveScrollPosition: true,
  routes: [
    {
      path: '/',
      redirect: { name: 'Home' },
    },
    {
      path: '/home',
      name: 'Home',
      component: Home,
      beforeEnter: requireAuthenticated,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      beforeEnter: requireUnauthenticated,
    },
    {
      path: '/logout',
      name: 'Logout',
      beforeEnter: redirectLogout,
    },
    {
      path: '/signup',
      name: 'Signup',
      component: Signup,
      beforeEnter: requireUnauthenticated,
    },
  ],
});
