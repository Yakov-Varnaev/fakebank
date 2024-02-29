<script setup>
definePageMeta({
  layout: "centered",
  middleware: "anon-only",
});
</script>

<template>
  <v-col md="4">
    <login-form />
    <v-btn block elevation="0" to="/signup" class="mt-2">Sign up</v-btn>
  </v-col>
</template>
