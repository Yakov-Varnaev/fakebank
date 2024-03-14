<script>
export default {
  setup() {
    return {
      auth: useAuth(),
    };
  },
  data() {
    return {
      sender: null,
      recipient: null,
    };
  },
  computed: {
    forbiddenAccounts() {
      return this.sender ? [this.sender?.id] : [];
    },
  },
  methods: {
    close() {
      this.$emit("close");
    },
    submit() {
      console.log();
      // this.$emit("submit", this.data);
    },
    setRecipient(account) {
      this.recipient = account;
    },
  },
  watch: {
    sender() {
      this.recipient = null;
    },
  },
};
</script>

<template>
  <v-card>
    <v-card-title> Transaction Form </v-card-title>
    <v-card-text>
      <v-form>
        <v-container>
          <account-autocomplete v-model="sender" :user_id="auth.user.id" />
          <transaction-recipient-selector v-model="recipient" :forbiddenAccounts="forbiddenAccounts" />
        </v-container>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <button-block @cancel="close" @submit="submit" />
    </v-card-actions>
  </v-card>
</template>
