<script>
export default {
  setup() {
    return {
      auth: useAuth(),
    };
  },
  data() {
    return {
      dialog: false,
    };
  },
};
</script>

<template>
  <div v-if="auth.loggedIn">
    <v-btn v-bind="$attrs" @click="dialog = !dialog">
      <slot name="btn_text"> Make Transfer </slot>
    </v-btn>
    <v-dialog v-model="dialog">
      <template v-slot:default="{ isActive }">
        <v-row>
          <v-col offset-md="4" md="4">
            <v-card>
              <transaction-form @close="dialog = !dialog" />
            </v-card>
          </v-col>
        </v-row>
      </template>
    </v-dialog>
  </div>
</template>
