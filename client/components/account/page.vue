<script>
export default {
  setup() {
    const accounts = useAccounts();
    return { accounts, auth: useAuth() };
  },
  data() {
    return {};
  },
  methods: {
    async fetchAccounts() {
      await this.accounts.getAccounts(this.auth.user.id);
    },
  },
  mounted() {
    this.fetchAccounts();
  },
  computed: {
    paginatorLength() {
      return Math.ceil(this.accounts.total / this.accounts.perPage);
    },
    page: {
      get() {
        return this.accounts.page;
      },
      set(value) {
        this.accounts.page = value;
        this.fetchAccounts();
      },
    },
  },
};
</script>

<template>
  <v-container>
    <account-list :accounts="accounts.accounts" />
    <v-pagination v-model="page" :length="paginatorLength" />
  </v-container>
</template>
