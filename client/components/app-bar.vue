<script>
export default {
  setup() {
    const auth = useAuth();
    const loader = useLoader();
    return { auth, loader };
  },
  data() {
    return {
      authenticatedLinks: [
        { title: "Accounts", to: "/accounts" },
        { title: "Transactions", to: "/transactions" },
      ],
    };
  },
};
</script>

<template>
  <v-app-bar>
    <v-app-bar-title>
      <v-btn text nuxt to="/">FakeBank</v-btn>
    </v-app-bar-title>

    <v-spacer></v-spacer>

    <template v-slot:append v-if="auth.loggedIn && !loader.isLoading">
      <v-btn v-for="link in authenticatedLinks" :key="link.title" :to="link.to" nuxt text class="mr-1">
        {{ link.title }}
      </v-btn>
      <v-divider vertical inset class="mr-4" />
      <span>{{ auth.user?.first_name }} {{ auth.user?.last_name }}</span>
      <logout-btn />
      <notifications-controller />
    </template>
  </v-app-bar>
</template>
