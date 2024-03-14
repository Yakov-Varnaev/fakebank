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
    forbiddenAccounts: {
      type: Array,
      required: false,
      default: () => [],
    },
  },
  data() {
    return {
      query: "",
      options: [],
      selectedAccount: null,
    };
  },
  methods: {
    async fetch() {
      this.options = await this.accounts.search(this.user_id, this.query);
    },
    filterAccounts(options) {
      return options.filter((account) => {
        return !this.forbiddenAccounts.includes(account.id);
      });
    },
    setQuery(query) {
      debounce(() => {
        this.query = query;
      }, 300)();
    },
    cleanQuery() {
      this.query = "";
    },
  },
  watch: {
    selectedAccount(selected) {
      this.$emit("update", selected);
    },
    user_id() {
      this.fetch();
    },
    forbiddenAccounts() {
      this.selectedAccount = null;
      this.query = "";
    },
  },
  computed: {
    filteredAccounts() {
      return this.filterAccounts(this.options);
    },
    search() {
      return this.query;
    },
  },
  mounted() {
    if (this.user_id) this.fetch();
  },
};
</script>

<template>
  <v-autocomplete no-filter v-model="selectedAccount" :search-input.sync="query" @change="query = ''"
    :items="filteredAccounts" item-title="name" return-object label="Account" :disabled="!user_id" />
</template>
