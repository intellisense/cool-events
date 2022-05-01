import { removeNamespace } from '@/utils/helpers';

const Types = {
  actions: {
    LOGIN: 'auth/LOGIN',
    LOGOUT: 'auth/LOGOUT',
    INITIALIZE: 'auth/INITIALIZE',
    SIGNUP: 'auth/SIGNUP',
    LOAD_USER: 'auth/LOAD_USER',
  },
  mutations: {
    SET_TOKEN: 'auth/SET_TOKEN',
    REMOVE_TOKEN: 'auth/REMOVE_TOKEN',
    SET_USER: 'auth/SET_USER',
  },
  getters: {
    IS_AUTHENTICATED: 'auth/isAuthenticated',
    IS_USER_LOADED: 'auth/isUserLoaded',
  },
};

const _types = removeNamespace('auth/', Types);

export {
  Types,
  _types,
};
