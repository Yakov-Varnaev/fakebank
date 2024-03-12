<script>
export default {
  data() {
    return {
      form: {
        sender: "",
        recipient: "",
        amount: "",
      },
    };
  },
  methods: {
    close() {
      this.$emit("close");
    },
    save() {
      // this.$emit("save", this.form);
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
          <v-row>
            <v-col cols="12" sm="6">
              <v-text-field v-model="form.name" label="Name" required></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model="form.amount" label="Amount" required></v-text-field>
            </v-col>
            <v-col cols="12" sm="12">
              <v-text-field v-model="form.type" label="Type" required></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <button-block />
    </v-card-actions>
  </v-card>
</template>
