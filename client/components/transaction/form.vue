<script>
import { apiv1 } from "@/axios";

export default {
  data() {
    return {
      user_search: "",
      users: [],
      recipient_user: null, // the user to send the money to
      form: {
        sender: "", // one of the user's accounts
        recipient: "", // recipient_user's account
        amount: "",
      },
    };
  },
  computed: {},
  methods: {
    close() {
      this.$emit("close");
    },
    async fetchUsers() {
      const { data } = await apiv1.get("/users", {
        params: { search: this.user_search },
      });
      console.log(data);
      this.users = data.data;
    },
    async submit() {
      console.log(this.form);
      this.close();
    },
    setUserSearch(event) {
      this.user_search = event;
    },
  },
  mounted() {
    this.fetchUsers();
  },
  watch: {
    async user_search(new_search, old_search) {
      await this.fetchUsers();
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
          <v-autocomplete
            no-filter
            v-model="recipient_user"
            :items="users"
            :search="user_search"
            label="Recipient"
            item-title="email"
            return-object
            @update:search="setUserSearch"
          />
        </v-container>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <button-block @cancel="close" @submit="submit" />
    </v-card-actions>
  </v-card>
</template>
