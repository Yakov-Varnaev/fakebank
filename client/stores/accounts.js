import { defineStore } from "pinia";
import { fetchAccounts } from "~/api/accounts";
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
      return await useLoader().withLoader(fn);
    },
    async setPage(page) {
      this.page = page;
      await this.getAccounts();
    },
    async fetch(user_id, query = null) {
      try {
        const offset = (this.page - 1) * this.perPage;
        const { data } = await fetchAccounts(
          offset,
          this.perPage,
          user_id,
          query,
        );
        return data;
      } catch (error) {
        const alert = useAlert();
        alert.reportError(`Failed to get accounts: ${error.response?.status}`);
        return { data: [], total: 0 };
      }
    },
    async getAccounts(user_id) {
      const { data, total } = await this.withLoader(
        async () => await this.fetch(user_id),
      );
      this.accounts = data;
      this.total = total;
    },
    async search(user_id, query) {
      const { data } = await this.withLoader(
        async () => await this.fetch(user_id, query),
      );
      return data;
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
