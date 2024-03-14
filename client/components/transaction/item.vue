<script>
export default {
  setup() {
    return { auth: useAuth() };
  },
  props: {
    transaction: {
      type: Object,
      required: true,
    },
  },
  data() {
    var kind = "income";

    if (this.transaction.sender_account.user.id === this.auth.user.id) {
      kind = "outcome";
    } else if (
      this.transaction.recipient_account.user.id ===
      this.transaction.recipient_account.user.id
    ) {
      kind = "self";
    }

    return {
      dialog: false,
      kind,
    };
  },
  methods: {
    parseBalance(balance) {
      return parseFloat(balance).toFixed(2);
    },
    parsedDate(date) {
      return new Date(date).toLocaleDateString();
    },
    parsedTime(date) {
      return new Date(date).toLocaleTimeString();
    },
  },
};
</script>

<template>
  <v-card variant="tonal" color="info">
    <v-card-title class="d-flex align-center">
      <span>{{ transaction.sender_account.user.email }}</span>
      <v-icon class="mx-2 text-caption">
        {{ kind === "income" ? "mdi-arrow-down" : "mdi-arrow-up" }}
      </v-icon>
      <span>{{ transaction.recipient_account.user.email }}</span>
      <v-spacer />
      <v-chip :color="kind === 'income' ? 'green' : 'red'" text-color="white" class="text-caption">
        {{ transaction.amount }}
      </v-chip>
      <v-spacer />
      <div class="d-flex flex-column align-center text-caption">
        <span>{{ parsedDate(transaction.time) }}</span>
        <span>{{ parsedTime(transaction.time) }}</span>
      </div>
    </v-card-title>
  </v-card>
</template>
