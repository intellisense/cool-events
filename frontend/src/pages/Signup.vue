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
        <v-card class="elevation-12">
          <v-toolbar
            dark
            color="primary"
          >
            <v-toolbar-title>Signup</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form
              v-if="!signupCompleted"
              ref="form"
              @submit.prevent="signup()"
            >
              <v-text-field
                v-model="formData.email"
                :rules="rules.email"
                :error-messages="getErrors('email')"
                name="email"
                label="Email"
                type="email"
                placeholder="email"
                required
              />
              <v-text-field
                v-model="formData.password1"
                :rules="rules.password1"
                :error-messages="getErrors('password1')"
                name="password1"
                label="Password"
                type="password"
                placeholder="password"
                required
              />
              <v-text-field
                v-model="formData.password2"
                :rules="rules.password2"
                :error-messages="getErrors('password2')"
                name="password2"
                label="Confirm Password"
                type="password"
                placeholder="Confirm password"
                required
              />
              <NonFieldErrors
                v-if="!registering"
                :errors="getNonFieldErrors()"
              />
              <v-btn
                type="submit"
                class="mt-4"
                color="primary"
                value="signup"
                :disabled="registering"
              >
                Signup
              </v-btn>
              <div class="d-inline-block float-right mt-6">
                Already have an account?
                <router-link :to="{ name: 'Login'}">
                  Login
                </router-link>
              </div>
            </v-form>
            <template v-else>
              <div class="text-success">
                Registration completed.
              </div>
              <v-btn
                class="mt-4"
                color="primary"
                value="login"
                :to="{ name: 'Login'}"
              >
                Login
              </v-btn>
            </template>
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
  name: 'Signup',
  components: {
    NonFieldErrors,
  },
  mixins: [ValidationResponseHandler],
  data() {
    return {
      formData: {
        email: '',
        password1: '',
        password2: '',
      },
      registering: false,
      signupCompleted: false,
      rules: {
        email: [
          (v) => !!v || 'E-mail is required',
        ],
        password1: [
          (v) => !!v || 'Password is required',
        ],
        password2: [
          (v) => !!v || 'Password confirmation is required',
        ],
      },
    };
  },
  methods: {
    signup() {
      this.clearErrors();
      if (!this.$refs.form.validate()) return;
      this.registering = true;
      this.$store.dispatch(Types.actions.SIGNUP, { ...this.formData })
        .then(() => { this.signupCompleted = true; })
        .catch((error) => this.syncErrors(error))
        .finally(() => { this.registering = false; });
    },
  },
};
</script>
