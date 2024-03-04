<script setup>
definePageMeta({
  middleware: "authenticated-only",
});
</script>

<template>
  <account-page />
</template>
