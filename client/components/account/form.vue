<script>
import { useVuelidate } from "@vuelidate/core";
import { required, minValue } from "@vuelidate/validators";
export default {
  setup() {
    return { v$: useVuelidate(), accounts: useAccounts() };
  },
  props: {
    account: {
      type: Object,
      required: false,
      default: {},
    },
  },
  data() {
    return {
      accountData: {
        name: "",
        balance: parseFloat(0).toFixed(2),
        ...this.account,
      },
      isEdit: Object.keys(this.account).length > 0,
    };
  },
  validations() {
    return {
      accountData: {
        name: { required },
        balance: { required, minValue: minValue(0) },
      },
    };
  },
  methods: {
    close() {
      this.$emit("close");
    },
    async submit() {
      if (this.isEdit) {
        await this.updateAccount();
      } else {
        await this.createAccount();
      }
      this.close();
    },
    async updateAccount() {
      await this.accounts.update(this.account.id, this.accountData);
    },
    async createAccount() {
      await this.accounts.create(this.accountData);
    },
  },
  computed: {
    isValid() {
      return !this.v$.accountData.$invalid;
    },
  },
};
</script>

<template>
  <v-card>
    <v-card-title>
      {{ isEdit ? "Edit Account" : "Create Account" }}
    </v-card-title>
    <v-card-text>
      <v-form>
        <v-text-field label="Name" v-model="accountData.name" @input="v$.accountData.name.$touch"
          @blur="v$.accountData.name.$touch" :error-messages="v$.accountData.name.$errors.map((e) => e.$message)" />
        <v-text-field label="Balance" v-model="accountData.balance" type="number" @input="v$.accountData.balance.$touch"
          @blur="v$.accountData.balance.$touch" :error-messages="v$.accountData.balance.$errors.map((e) => e.$message)
        " />
      </v-form>
    </v-card-text>
    <v-card-actions>
      <button-block @submit="submit" @cancel="close" :isSubmitDisabled="!isValid" />
    </v-card-actions>
  </v-card>
</template>
