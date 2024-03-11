import { defineStore } from "pinia";
import { apiv1 } from "~/axios";

export const useTransactions = defineStore("transactions", {
  state: () => ({
    total: 0,
    page: 1,
    perPage: 10,
    transactions: [],
  }),
  actions: {
    async withLoader(fn) {
      await useLoader().withLoader(fn);
    },
    async setPage(page) {
      this.page = page;
      await this.getTransactions();
    },
    async _getTransactions() {
      try {
        const offset = (this.page - 1) * this.perPage;
        const { data } = await apiv1.get("/transactions/my", {
          params: { limit: this.perPage, offset },
        });
        this.transactions = data.data;
        this.total = data.total;
      } catch (error) {
        const alert = useAlert();
        console.log(error);
        alert.reportError(
          `Failed to get transactions: ${error.response?.status}`,
        );
      }
    },
    async getTransactions() {
      await this.withLoader(this._getTransactions);
    },
    async create(payload) {
      return await this.withLoader(async () => {
        try {
          const { data } = await apiv1.post("/transactions/", payload);
          if (this.transactions.length < this.perPage) {
            this.transactions.unshift(data);
          } else {
            await this.getTransactions();
          }
        } catch ({ response }) {
          const alert = useAlert();
          alert.reportError(`Failed to create transaction: ${response.status}`);
        }
      });
    },
    async update(id, transaction) {
      return await this.withLoader(async () => {
        try {
          const { data } = await apiv1.put(`/transactions/${id}/`, transaction);
          const index = this.transactions.findIndex((a) => a.id === id);
          this.transactions[index] = data;
        } catch ({ response }) {
          useAlert().reportError(
            `Failed to update transaction: ${response.status}`,
          );
        }
      });
    },
  },
});
