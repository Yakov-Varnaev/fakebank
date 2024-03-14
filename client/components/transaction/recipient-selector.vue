<script>
export default {
  setup() {
    return {
      auth: useAuth(),
    };
  },
  props: {
    forbiddenAccounts: {
      type: Array,
      required: false,
      default: () => [],
    },
  },
  data() {
    return {
      user: null,
      account: null,
    };
  },
  computed: {},
  watch: {
    user() {
      this.account = null;
    },
    forbiddenAccounts() {
      if (this.user?.id === this.auth.user.id) this.account = null;
    },
    account(selected) {
      this.$emit("update", selected);
    },
  },
};
</script>

<template>
  <v-row>
    <v-col>
      <user-autocomplete v-model="user" />
    </v-col>
    <v-col>
      <account-autocomplete v-model="account" :user_id="user?.id" :forbiddenAccounts="forbiddenAccounts" />
    </v-col>
  </v-row>
</template>
