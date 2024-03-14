<script>
export default {
  setup() {
    const accounts = useAccounts();
    return { accounts };
  },
  props: {
    account: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      dialog: false,
    };
  },
  methods: {
    async deleteAccount() {
      await this.accounts.delete(this.account.id);
    },
    parseBalance(balance) {
      return parseFloat(balance).toFixed(2);
    },
  },
};
</script>

<template>
  <v-card>
    <v-card-title class="d-flex align-center">
      {{ account.name }}

      <div class="ml-auto">
        <v-chip class="mr-3" variant="outlined">
          {{ parseBalance(account.balance) }}
        </v-chip>
        <v-dialog v-model="dialog">
          <template v-slot:activator="{ props: activatorProps }">
            <v-btn v-bind="activatorProps" icon flat>
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
          </template>
          <template v-slot:default="{ isActive }">
            <account-form :account="account" @close="dialog = !dialog" />
          </template>
        </v-dialog>
        <v-btn icon text flat class="text-red" @click="deleteAccount">
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </div>
    </v-card-title>
  </v-card>
</template>
