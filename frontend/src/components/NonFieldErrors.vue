<template>
  <v-list
    v-if="errors.length"
    dense
  >
    <v-list-item
      v-for="(error, i) in errors"
      :key="i"
      class="error--text"
    >
      <v-list-item-content>
        <v-list-item-title v-text="error" />
      </v-list-item-content>
    </v-list-item>
  </v-list>
</template>

<script>
export default {
  name: 'NonFieldErrors',
  props: {
    errors: {
      type: Array,
      default() {
        return [];
      },
    },
  },
};
</script>
