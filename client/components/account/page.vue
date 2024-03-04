<script>
export default {
  setup() {
    const auth = useAuth();
    const accounts = useAccounts();
    return { auth, accounts };
  },
  data() {
    return {};
  },
  methods: {
    async fetchAccounts() {
      await this.accounts.getAccounts();
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
