<script>
import { useVuelidate } from "@vuelidate/core";
import { minLength, sameAs, required, email } from "@vuelidate/validators";

export default {
  setup() {
    return { v$: useVuelidate(), auth: useAuth() };
  },
  data() {
    return {
      registerData: {
        firstName: "",
        lastName: "",
        email: "",
        password: "",
      },
      errors: {
        firstName: [],
        lastName: [],
        email: [],
        password: [],
        detail: [],
      },
    };
  },
  validations() {
    return {
      registerData: {
        firstName: { required },
        lastName: { required },
        email: { required, email },
        password: { required, minLength: minLength(8) },
      },
    };
  },
  methods: {
    collectErrors(field) {
      const vuelidateErrors = [];
      if (this.v$.registerData[field]) {
        vuelidateErrors.push(
          ...this.v$.registerData[field].$errors.map((e) => e.$message),
        );
      }
      return [...vuelidateErrors, ...this.errors[field]];
    },
    async performRegister() {
      this.v$.registerData.$touch();
      if (this.v$.registerData.$invalid) {
        return;
      }
      this.auth.register(this.registerData);
    },
  },
  mounted() {
    console.log(this.$config.public.apiHost);
  },
};
</script>

<template>
  <v-card>
    <v-card-text>
      <v-form>
        <v-row>
          <v-col>
            <v-text-field label="First Name" v-model="registerData.firstName" @input="v$.registerData.firstName.$touch"
              @blur="v$.registerData.firstName.$touch" :error-messages="collectErrors('firstName')" class="mb-2" />
          </v-col>
          <v-col>
            <v-text-field label="Last Name" v-model="registerData.lastName" @input="v$.registerData.lastName.$touch"
              @blur="v$.registerData.lastName.$touch" :error-messages="collectErrors('lastName')" class="mb-2" />
          </v-col>
        </v-row>
        <v-text-field type="email" label="E-mail" v-model="registerData.email" @input="v$.registerData.email.$touch"
          @blur="v$.registerData.email.$touch" :error-messages="v$.registerData.email.$errors.map((e) => e.$message)"
          class="mb-2" />
        <v-text-field autocomplete="new-password" type="password" label="Пароль" v-model="registerData.password"
          @input="v$.registerData.password.$touch" @blur="v$.registerData.password.$touch"
          :error-messages="collectErrors('password')" class="mb-2" />
        <v-btn block type="submit" text="Sign up" color="primary" @click.prevent="performRegister" />
      </v-form>
    </v-card-text>
  </v-card>
</template>
