<script>
export default {
  setup() {
    const transactions = useTransactions();
    return { transactions };
  },
  props: {
    transaction: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      dialog: false,
    };
  },
  methods: {
    parseBalance(balance) {
      return parseFloat(balance).toFixed(2);
    },
  },
};
</script>

<template>
  <v-card color="light">
    <v-card-title class="d-flex align-center">
      {{ transaction.time }} | {{ transaction.sender_account.user.email }} sent
      {{ transaction.amount }} to {{ transaction.recipient_account.user.email }}
    </v-card-title>
  </v-card>
</template>
