<script>
export default {
  setup() {
    const auth = useAuth();
    return { auth };
  },
  methods: {
    async performLogout() {
      await this.auth.logout();
    },
  },
};
</script>

<template>
  <v-btn color="red" v-bind="$attrs" @click="performLogout">
    <v-icon>mdi-logout</v-icon>
  </v-btn>
</template>
