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
      <transaction-item :transaction="transaction" v-for="transaction in transactions" class="mt-2" v-auto-animate />
    </v-list>
  </div>
</template>
