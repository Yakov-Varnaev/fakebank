<script setup>
definePageMeta({
  middleware: "authenticated-only",
});
</script>

<script>
export default {
  data() {
    return {
      tab: "accounts",
    };
  },
};
</script>

<template>
  <v-container> Index </v-container>
</template>
