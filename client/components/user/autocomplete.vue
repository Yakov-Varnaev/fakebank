<script>
import { debounce } from "lodash";

export default {
  setup() {
    return {
      users: useUsers(),
    };
  },
  data() {
    return {
      query: "",
      selected: null,
      options: [],
    };
  },
  methods: {
    async fetch() {
      const data = await this.users.search(this.query);
      this.options = data;
    },
    setQuery(query) {
      debounce(() => {
        this.query = query;
      }, 300)();
    },
  },
  watch: {
    selected(oldSelection, newSelection) {
      this.$emit("update", newSelection);
    },
  },
  mounted() {
    this.fetch();
  },
};
</script>

<template>
  <v-autocomplete v-bind="$attrs" no-filter v-model="selected" @update:search="setQuery" :items="options"
    item-title="email" return-object label="User" />
</template>
