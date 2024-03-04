<script>
export default {
  data() {
    return {
      transactions: [
        {
          id: 1,
          sender: "John Doe",
          recipient: "Jane Doe",
          amount: 100,
          oldBalance: 1000,
          newBalance: 900,
        },
      ],
    };
  },
};
</script>

<template>
  <v-list>
    <transaction-create-item />
    <transaction-item :transaction="transaction" v-for="transaction in transactions" class="mt-2" />
  </v-list>
</template>
