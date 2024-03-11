<script>
export default {
  setup() {
    const transactions = useTransactions();
    return { transactions };
  },
  data() {
    return {};
  },
  methods: {
    async fetchTransactions() {
      await this.transactions.getTransactions();
    },
  },
  mounted() {
    this.fetchTransactions();
  },
  computed: {
    paginatorLength() {
      return Math.ceil(this.transactions.total / this.transactions.perPage);
    },
    page: {
      get() {
        return this.transactions.page;
      },
      set(value) {
        this.transactions.page = value;
        this.fetchTransactions();
      },
    },
  },
};
</script>

<template>
  <v-container>
    <transaction-list :transactions="transactions.transactions" />
    <v-pagination v-model="page" :length="paginatorLength" />
  </v-container>
</template>
