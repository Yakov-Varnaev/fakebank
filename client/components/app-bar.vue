<script>
export default {
  setup() {
    const auth = useAuth();
    const loader = useLoader();
    return { auth, loader };
  },
};
</script>
<template>
  <v-app-bar>
    <v-app-bar-title> FakeBank </v-app-bar-title>

    <v-spacer></v-spacer>

    <template v-slot:append v-if="auth.loggedIn && !loader.isLoading">
      <span>{{ auth.user?.first_name }} {{ auth.user?.last_name }}</span>
      <logout-btn />
    </template>
  </v-app-bar>
</template>
