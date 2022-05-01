import Vue from 'vue';
import vuetify from '@/plugins/vuetify';
import router from '@/router';
import store from '@/store';
import { formatDateTime } from '@/utils/helpers';
import App from './App';

Vue.filter('formatDateTime', formatDateTime);

new Vue({
  vuetify,
  router,
  store,
  render: (h) => h(App),
}).$mount('#app');
