import { _types } from './types';

const getters = {
  [_types.getters.IS_AUTHENTICATED]: (state) => !!state.token,
  [_types.getters.IS_USER_LOADED]: (state) => !!state.user,
};
export default getters;
