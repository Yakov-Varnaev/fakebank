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
  <layout-paged>
    <template v-slot:content>
      <transaction-list :transactions="transactions.transactions" />
    </template>
    <template v-slot:pagination>
      <v-pagination v-model="page" :length="paginatorLength" />
    </template>
  </layout-paged>
</template>
