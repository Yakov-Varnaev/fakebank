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
  <v-container>
    <v-tabs v-model="tab" bg-color="primary">
      <v-tab value="accounts">Account</v-tab>
      <v-tab value="transactions">Transactions</v-tab>
    </v-tabs>

    <v-card-text>
      <v-window v-model="tab">
        <v-window-item value="accounts"> <account-tab /></v-window-item>
        <v-window-item value="transactions"> <transaction-tab /></v-window-item>
      </v-window>
    </v-card-text>
  </v-container>
</template>
