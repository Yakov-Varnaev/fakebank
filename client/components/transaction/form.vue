<script>
import { useVuelidate } from "@vuelidate/core";
import { required, minValue } from "@vuelidate/validators";

export default {
  setup() {
    return {
      transactions: useTransactions(),
      auth: useAuth(),
      v$: useVuelidate(),
    };
  },
  data() {
    return {
      sender: null,
      recipient: null,
      amount: 0,
    };
  },
  validations() {
    return {
      sender: { required },
      recipient: { required },
      amount: { required, minValue: minValue(10) },
    };
  },
  computed: {
    forbiddenAccounts() {
      return this.sender ? [this.sender?.id] : [];
    },
    isAmountActive() {
      return this.sender && this.recipient;
    },
    isUserDisabled() {
      return this.sender ? false : true;
    },
  },
  methods: {
    close() {
      this.$emit("close");
    },
    submit() {
      const data = {
        sender: this.sender.id,
        recipient: this.recipient?.id,
        amount: parseFloat(this.amount),
      };
      console.log(data);
      this.transactions.create(data);
    },
    setRecipient(account) {
      this.recipient = account;
    },
  },
  watch: {
    sender() {
      this.recipient = null;
    },
    recipient(value) {
      console.log("form", value);
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
          <account-autocomplete v-model="sender" :user_id="auth.user.id" @input="v$.sender.$touch"
            @blur="v$.sender.$touch" :error-messages="v$.sender.$errors.map((e) => e.$message)" />
          <transaction-recipient-selector v-model="recipient" :forbiddenAccounts="forbiddenAccounts"
            :isUserDisabled="isUserDisabled" @input="v$.recipient.$touch" @blur="v$.recipient.$touch"
            :error-messages="v$.recipient.$errors.map((e) => e.$message)" />
          <v-text-field label="Amount" v-model="amount" type="number" :disabled="!isAmountActive"
            @input="v$.amount.$touch" @blur="v$.amount.$touch"
            :error-messages="v$.amount.$errors.map((e) => e.$message)" />
        </v-container>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <button-block @cancel="close" @submit="submit" />
    </v-card-actions>
  </v-card>
</template>
