<script>
export default {
  data() {
    return {
      recipient_user: null, // the user to send the money to
      form: {
        sender: "", // one of the user's accounts
        recipient: "", // recipient_user's account
        amount: "",
      },
    };
  },
  methods: {
    close() {
      this.$emit("close");
    },
    async submit() {
      console.log(this.form);
      this.close();
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
          <v-auto-complete
            v-model="recipient_user"
            :items="['user1', 'user2', 'user3']"
            label="Recipient"
            item-text="name"
            item-value="id"
          />
        </v-container>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <button-block @cancel="close" @submit="submit" />
    </v-card-actions>
  </v-card>
</template>
