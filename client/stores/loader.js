import { defineStore } from "pinia";

export const useLoader = defineStore("loader", {
  state: () => ({
    loading: false,
  }),
  actions: {
    async withLoader(func, args) {
      this.start();
      let res = await func(args);
      this.stop();
      return res;
    },
    start() {
      this.loading = true;
    },
    stop() {
      this.loading = false;
    },
  },
});
