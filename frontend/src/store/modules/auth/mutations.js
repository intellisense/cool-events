import session from '@/api/session';
import constants from '@/utils/constants';
import { _types } from './types';

const isProduction = process.env.NODE_ENV === 'production';

const mutations = {
  [_types.mutations.SET_TOKEN](state, token) {
    if (!isProduction) localStorage.setItem(constants.TOKEN_STORAGE_KEY, token);
    session.defaults.headers.Authorization = `Token ${token}`;
    state.token = token;
  },
  [_types.mutations.REMOVE_TOKEN](state) {
    localStorage.removeItem(constants.TOKEN_STORAGE_KEY);
    delete session.defaults.headers.Authorization;
    state.token = null;
  },
  [_types.mutations.SET_USER](state, user) {
    state.user = user;
  },
};

export default mutations;
