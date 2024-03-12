<template>
  <v-app>
    <AppBar />
    <v-main>
      <slot />
    </v-main>
    <alert-container />
    <div v-auto-animate>
      <transaction-create-btn
        class="floating_transaction_btn"
        size="large"
        variant="tonal"
        color="success"
        v-if="this.$route.name != 'transactions'"
      />
    </div>
  </v-app>
</template>

<style scoped>
.floating_transaction_btn {
  position: fixed;
  bottom: 20px;
  left: 20px;
}
</style>
