<template>
  <v-app>
    <AppBar />
    <v-main>
      <slot />
    </v-main>
    <alert-container />
    <transaction-create-btn class="floating_transaction_btn" size="large" variant="tonal" color="success"
      v-if="this.$route.name != 'transactions'" />
  </v-app>
</template>

<style scoped>
.floating_transaction_btn {
  position: fixed;
  bottom: 20px;
  right: 20px;
  border: 2px solid lime;
}
</style>
