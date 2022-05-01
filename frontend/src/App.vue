<template>
  <v-app>
    <nav>
      <v-app-bar color="primary">
        <v-app-bar-nav-icon
          class="white--text"
          @click.stop="drawer = !drawer"
        />
        <v-toolbar-title class="white--text">
          <span>{{ appTitle }}</span>
        </v-toolbar-title>
        <v-spacer />
        <v-menu offset-y>
          <v-btn text>
            <v-icon left>
              expand_more
            </v-icon>
            <span>Menu</span>
          </v-btn>
          <v-list
            nav
            dense
          >
            <v-list-item
              v-for="item in menuItems"
              :key="item.title"
              :to="item.link"
            >
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-app-bar>

      <v-navigation-drawer
        v-model="drawer"
        class="primary"
        absolute
        bottom
        temporary
      >
        <v-list>
          <v-list-item
            v-for="item in menuItems"
            :key="item.title"
            router
            :to="item.link"
          >
            <v-list-item-action>
              <v-icon class="white--text">
                {{ item.icon }}
              </v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title class="white--text">
                {{ item.title }}
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
    </nav>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex';
import { Types } from '@/store/modules/auth/types';

export default {
  name: 'App',
  data() {
    return {
      appTitle: 'Cool Events',
      drawer: false,
    };
  },
  computed: {
    ...mapGetters({
      isAuthenticated: Types.getters.IS_AUTHENTICATED,
    }),
    menuItems() {
      let menuItems;
      if (this.isAuthenticated) {
        menuItems = [
          { title: 'Upcoming Events', icon: 'mdi-calendar-multiple', link: { name: 'UpcomingEvents' } },
          { title: 'My Events', icon: 'mdi-calendar-heart', link: { name: 'MyEvents' } },
          { title: 'Logout', icon: 'mdi-logout', link: { name: 'Logout' } },
        ];
      } else {
        menuItems = [
          { title: 'Login', icon: 'mdi-login', link: { name: 'Login' } },
          { title: 'Signup', icon: 'mdi-account', link: { name: 'Signup' } },
        ];
      }
      return menuItems;
    },
  },
};
</script>
