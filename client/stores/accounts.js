import { defineStore } from "pinia";
import { apiv1 } from "~/axios";

export const useAccounts = defineStore("accounts", {
  state: () => ({
    total: 0,
    page: 1,
    perPage: 10,
    accounts: [],
  }),
  actions: {
    async withLoader(fn) {
      await useLoader().withLoader(fn);
    },
    // make pagination work
    async setPage(page) {
      this.page = page;
      await this.getAccounts();
    },
    async _getAccounts() {
      try {
        const offset = (this.page - 1) * this.perPage;
        const { data } = await apiv1.get("/accounts/my", {
          params: { limit: this.perPage, offset },
        });
        this.accounts = data.data;
        this.total = data.total;
      } catch (error) {
        const alert = useAlert();
        console.log(error);
        alert.reportError(`Failed to get accounts: ${error.response?.status}`);
      }
    },
    async getAccounts() {
      await this.withLoader(this._getAccounts);
    },
    async create(payload) {
      return await this.withLoader(async () => {
        try {
          const { data } = await apiv1.post("/accounts/", payload);
          if (this.accounts.length < this.perPage) {
            this.accounts.unshift(data);
          } else {
            await this.getAccounts();
          }
        } catch ({ response }) {
          const alert = useAlert();
          alert.reportError(`Failed to create account: ${response.status}`);
        }
      });
    },
    async update(id, account) {
      return await this.withLoader(async () => {
        try {
          const { data } = await apiv1.put(`/accounts/${id}/`, account);
          const index = this.accounts.findIndex((a) => a.id === id);
          this.accounts[index] = data;
        } catch ({ response }) {
          useAlert().reportError(
            `Failed to update account: ${response.status}`,
          );
        }
      });
    },
    async delete(id) {
      return await this.withLoader(async () => {
        try {
          await apiv1.delete(`/accounts/${id}/`);
          if (this.total > this.perPage) {
            await this.getAccounts();
          } else {
            this.accounts = this.accounts.filter((a) => a.id !== id);
          }
        } catch ({ response }) {
          useAlert().reportError(
            `Failed to delete account: ${response.status}`,
          );
        }
      });
    },
  },
});
