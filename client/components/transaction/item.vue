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
    }
    if (
      this.transaction.sender_account.user.id ===
      this.transaction.recipient_account.user.id
    ) {
      kind = "self";
    }
    const colors = {
      income: "green",
      outcome: "red",
      self: "blue",
    };
    const prepend_icons = {
      pending: { icon: "mdi-clock-outline", color: "warning" },
      error: { icon: "mdi-alert-outline", color: "red" },
      done: { icon: "mdi-check-outline", color: "success" },
    };
    console.log(this.transaction.status);

    return {
      dialog: false,
      kind,
      color: colors[kind],
      prepend: prepend_icons[this.transaction.status],
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
  <v-card variant="tonal" :color="prepend.color">
    <v-card-title class="d-flex align-center">
      <v-icon class="mr-2" :color="prepend.color">
        {{ prepend.icon }}
      </v-icon>
      <span>{{ transaction.sender_account.user.email }}</span>
      <v-icon class="mx-2 text-caption">
        {{ kind === "income" ? "mdi-arrow-down" : "mdi-arrow-up" }}
      </v-icon>
      <span>{{ transaction.recipient_account.user.email }}</span>
      <v-chip :color="color" text-color="white" class="text-caption ml-auto">
        {{ transaction.amount }} | {{ kind }}
      </v-chip>
      <div class="d-flex flex-column align-center text-caption ml-16">
        <span>{{ parsedDate(transaction.time) }}</span>
        <span>{{ parsedTime(transaction.time) }}</span>
      </div>
    </v-card-title>
  </v-card>
</template>
