<script>
export default {
  props: {
    transactions: {
      type: Array,
      required: true,
    },
  },
};
</script>

<template>
  <div v-auto-animate>
    <v-list v-auto-animate>
      <transaction-create-item />
      <v-divider class="mt-3" />
      <transaction-item :transaction="transaction" v-for="transaction in transactions" :key="transaction.id"
        class="mt-2" v-auto-animate />
    </v-list>
  </div>
</template>
