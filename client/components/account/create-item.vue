<script>
export default {
  data() {
    return {
      overlay: false,
    };
  },
};
</script>

<template>
  <v-dialog v-model="overlay">
    <template v-slot:activator="{ props: activatorProps }">
      <v-btn v-bind="activatorProps" block variant="tonal" color="success" size="large">
        Create Account
      </v-btn>
    </template>

    <template v-slot:default="{ isActive }">
      <v-row>
        <v-col offset-md="4" md="4">
          <account-form @close="overlay = !overlay" />
        </v-col>
      </v-row>
    </template>
  </v-dialog>
</template>
