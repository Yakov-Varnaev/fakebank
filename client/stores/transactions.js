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
      return await useLoader().withLoader(fn);
    },
    async setPage(page) {
      this.page = page;
      await this.getTransactions();
    },
    async _getTransactions(query = {}) {
      try {
        const offset = (this.page - 1) * this.perPage;
        const { data } = await apiv1.get("/transactions/my", {
          params: { limit: this.perPage, offset, ...query },
        });
        return data;
      } catch (error) {
        const alert = useAlert();
        alert.reportError(
          `Failed to get transactions: ${error.response?.status}`,
        );
      }
    },
    async getTransactions() {
      const data = await this.withLoader(async () =>
        await this._getTransactions()
      );
      this.transactions = data.data;
      this.total = data.total;
    },
    async searchTransactions(query) {
      const data = await this.withLoader(async () =>
        this._getTransactions(query)
      );
      return data.data;
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
