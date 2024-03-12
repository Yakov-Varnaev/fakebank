<script>
export default {
  props: {
    accounts: {
      type: Object,
      required: true,
    },
  },
  methods: {},
};
</script>

<template>
  <v-list elevation="0" class="px-3" v-auto-animate>
    <account-create-item />
    <account-item
      :account="account"
      v-for="account in accounts"
      :key="account.id"
      class="mt-2"
    />
  </v-list>
</template>
