<script>
export default {
  setup() {
    return {
      auth: useAuth(),
    };
  },
  data() {
    return {
      data: {
        sender: null,
        recipient: null,
      },
    };
  },
  methods: {
    close() {
      this.$emit("close");
    },
    submit() {
      console.log(this.data);
      // this.$emit("submit", this.data);
    },
  },
};
</script>

<template>
  <v-card>
    <v-card-title> Transaction Form </v-card-title>
    <v-card-text>
      <v-form>
        <v-container>
          <account-autocomplete v-model="data.sender" :user_id="auth.user.id" />
          <transaction-recipient-selector v-model="data.recipient" />
        </v-container>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <button-block @cancel="close" @submit="submit" />
    </v-card-actions>
  </v-card>
</template>
