<script setup>
definePageMeta({
  layout: "centered",
  middleware: "anon-only",
});
</script>

<template>
  <v-col md="4">
    <register-form />
    <v-btn block elevation="0" to="/signin" class="mt-2">Sign in</v-btn>
  </v-col>
</template>
