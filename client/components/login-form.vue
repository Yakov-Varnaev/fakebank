<script setup>
import { useVuelidate } from "@vuelidate/core";
import { required, email } from "@vuelidate/validators";

const formData = reactive({
  username: "",
  password: "",
});

const errors = reactive({
  username: [],
  password: [],
  detail: [],
});

const rules = computed(() => {
  return {
    username: { required, email },
    password: { required },
  };
});

const v$ = useVuelidate(rules, formData);
const auth = useAuth();

async function performLogin() {
  await auth.login(formData);
}

const isFormValid = computed(() => {
  return Object.keys(formData).every((key) => formData[key]) && !v$.$errors;
});

function collectErrors(field) {
  const vuiledateErrors = [];
  if (v$[field]) {
    vuelidateErrors.push(...this.v$[field].$errors.map((e) => e.$message));
  }
  return [...vuelidateErrors, ...this.errors[field]];
}
</script>

<template>
  <v-card>
    <v-card-text>
      <v-form>
        <v-text-field
          type="email"
          label="E-mail"
          v-model="formData.username"
          class="mb-2"
        />
        <v-text-field
          type="password"
          label="Пароль"
          v-model="formData.password"
          class="mb-2"
        />
        <v-btn
          block
          type="submit"
          text="Sign in"
          color="primary"
          @click.prevent="performLogin"
        />
      </v-form>
    </v-card-text>
  </v-card>
</template>
