import { fetchUsers } from "~/api/users";

export const useUsers = defineStore("users", {
  state: () => ({
    total: 0,
    page: 1,
    perPage: 10,
  }),
  actions: {
    async fetchUsers(query = null) {
      const offset = (this.page - 1) * this.perPage;
      try {
        const { data } = await fetchUsers(offset, this.perPage, query);
        return data;
      } catch (error) {
        useAlert().reportError(
          `Failed to get users: ${error.response?.status}`,
        );
        return { data: [], total: 0 };
      }
    },
    async search(query) {
      const { data } = await useLoader().withLoader(
        async () => await this.fetchUsers(query),
      );
      return data;
    },
  },
});
