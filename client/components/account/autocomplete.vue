<script>
import { debounce } from "lodash";

export default {
  setup() {
    return {
      accounts: useAccounts(),
    };
  },
  props: {
    user_id: {
      required: false,
      type: String,
      default: null,
    },
    label: {
      required: false,
      type: String,
      default: "Account",
    },
  },
  data() {
    return {
      query: "",
      selectedAccount: null,
      options: [],
    };
  },
  methods: {
    async fetch() {
      const data = await this.accounts.search(this.user_id, this.query);
      this.options = data;
    },
    setQuery(query) {
      debounce(() => {
        this.query = query;
      }, 300)();
    },
  },
  watch: {
    selectedAccount(oldSelection, newSelection) {
      this.$emit("update", newSelection);
    },
    user_id() {
      this.fetch();
    },
  },
  mounted() {
    if (this.user_id) this.fetch();
  },
};
</script>

<template>
  <v-autocomplete no-filter v-model="selectedAccount" @update:search="setQuery" :items="options" item-title="name"
    return-object label="Account" :disabled="!user_id" />
</template>
