<script>
export default {
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
    account() {
      this.$emit("update", this.account);
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
      <account-autocomplete v-model="account" :user_id="user?.id" />
    </v-col>
  </v-row>
</template>
