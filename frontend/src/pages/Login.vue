<template>
  <v-container
    fluid
    fill-height
  >
    <v-layout
      align-center
      justify-center
    >
      <v-flex
        xs12
        sm8
        md4
      >
        <v-card
          class="elevation-12"
          :loading="true"
        >
          <v-toolbar
            dark
            color="primary"
          >
            <v-toolbar-title>Login</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form
              ref="form"
              @submit.prevent="login()"
            >
              <v-text-field
                v-model="formData.email"
                :rules="rules.email"
                :error-messages="getErrors('email')"
                name="email"
                label="Email"
                type="text"
                placeholder="email"
                required
              />
              <v-text-field
                v-model="formData.password"
                :rules="rules.password"
                :error-messages="getErrors('password')"
                name="password"
                label="Password"
                type="password"
                placeholder="password"
                required
              />
              <NonFieldErrors
                v-if="!authenticating"
                :errors="getNonFieldErrors()"
              />
              <v-btn
                type="submit"
                class="mt-4"
                color="primary"
                value="login"
                :disabled="authenticating"
              >
                Login
              </v-btn>
              <div class="d-inline-block float-right mt-6">
                Don't have an account?
                <router-link :to="{ name: 'Signup'}">
                  Signup
                </router-link>
              </div>
            </v-form>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { Types } from '@/store/modules/auth/types';
import ValidationResponseHandler from '@/mixins/ValidationResponseHandler';
import NonFieldErrors from '../components/NonFieldErrors';

export default {
  name: 'Login',
  components: {
    NonFieldErrors,
  },
  mixins: [ValidationResponseHandler],
  data() {
    return {
      formData: {
        email: '',
        password: '',
      },
      rules: {
        email: [
          (v) => !!v || 'E-mail is required',
        ],
        password: [
          (v) => !!v || 'Password is required',
        ],
      },
      authenticating: false,
    };
  },
  methods: {
    login() {
      this.clearErrors();
      if (!this.$refs.form.validate()) return;
      this.authenticating = true;
      this.$store.dispatch(Types.actions.LOGIN, { ...this.formData })
        .then(() => this.$router.push({ name: 'Home' }))
        .catch((error) => this.syncErrors(error))
        .finally(() => { this.authenticating = false; });
    },
  },
};
</script>
