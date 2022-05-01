<template>
  <div v-if="isUserLoaded">
    <router-view />
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { Types } from '@/store/modules/auth/types';

export default {
  name: 'MainWrapper',
  computed: {
    ...mapGetters({ isUserLoaded: Types.getters.IS_USER_LOADED }),
  },
  mounted() {
    this.loadUserDetails();
  },
  methods: {
    loadUserDetails() {
      this.$store.dispatch(Types.actions.LOAD_USER);
    },
  },
};
</script>
