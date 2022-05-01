<template>
  <Events
    :username="user.username"
    title="My Events"
  />
</template>

<script>
import { mapState } from 'vuex';
import Events from '../components/Events';

export default {
  name: 'MyEvents',
  components: {
    Events,
  },
  computed: {
    ...mapState('auth', ['user']),
  },
};
</script>
