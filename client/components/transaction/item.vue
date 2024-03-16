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
      error: { icon: "mdi-close-circle-outline", color: "red" },
      done: { icon: "mdi-check-circle-outline", color: "success" },
    };

    const row = {
      prepend: prepend_icons[this.transaction.status],
      color: colors[kind],
      sender_email: this.transaction.sender_account.user.email,
      sender_account: this.transaction.sender_account.name,
      recipient_email: this.transaction.recipient_account.user.email,
      recipient_account: this.transaction.recipient_account.name,
      amount: this.parseBalance(this.transaction.amount),
      date: this.parsedDate(this.transaction.time),
      time: this.parsedTime(this.transaction.time),
    };

    return {
      dialog: false,
      kind,
      row,
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
  <v-card elevation="0">
    <v-card-title>
      <v-row align="center" justify="between">
        <v-col cols="1">
          <v-icon class="mr-2" :color="row.prepend.color">
            {{ row.prepend.icon }}
          </v-icon>
        </v-col>

        <v-col cols="3" align="center">
          <span> {{ row.sender_account }}({{ row.sender_email }}) </span>
        </v-col>
        <v-col cols="1" align="center">
          <div>
            <v-icon class="mx-2 text-caption" :color="row.color">
              mdi-arrow-right
            </v-icon>
          </div>
        </v-col>
        <v-col cols="3" align="center">
          <span>{{ row.recipient_email }}({{ row.recipient_account }})</span>
        </v-col>

        <v-col />

        <v-col align="center">
          <v-chip :color="row.color" class="text-caption ml-auto">
            {{ row.amount }}
          </v-chip>
        </v-col>

        <v-col />

        <v-col align="end" cols="1">
          <div class="d-flex flex-column align-center text-caption">
            <span>{{ row.date }}</span>
            <span>{{ row.time }}</span>
          </div>
        </v-col>
      </v-row>
    </v-card-title>
  </v-card>
</template>
