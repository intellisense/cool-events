import auth from '@/api/auth';
import constants from '@/utils/constants';
import { _types } from './types';

export const isProduction = process.env.NODE_ENV === 'production';

const actions = {
  [_types.actions.LOGIN]({ commit }, { email, password }) {
    return auth.login(email, password)
      .then(({ data }) => commit(_types.mutations.SET_TOKEN, data.key));
  },
  [_types.actions.LOGOUT]({ commit }) {
    return auth.logout()
      .finally(() => commit(_types.mutations.REMOVE_TOKEN));
  },
  [_types.actions.INITIALIZE]({ commit }) {
    const token = localStorage.getItem(constants.TOKEN_STORAGE_KEY);

    if (isProduction && token) {
      commit(_types.mutations.REMOVE_TOKEN);
    }

    if (!isProduction && token) {
      commit(_types.mutations.SET_TOKEN, token);
    }
  },
  [_types.actions.SIGNUP](_, { email, password1, password2 }) {
    return auth.signup(email, password1, password2);
  },
  [_types.actions.LOAD_USER]({ commit }) {
    return auth.getUserDetails()
      .then(({ data }) => commit(_types.mutations.SET_USER, data));
  },
};

export default actions;
