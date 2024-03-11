<script>
export default {
  data() {
    return {
      dialog: false,
    };
  },
};
</script>

<template>
  <div>
    <v-btn v-bind="$attrs">
      <slot name="btn_text"> Make Transfer </slot>
    </v-btn>
    <v-dialog v-model="dialog">
      <template v-slot:default="{ isActive }">
        <v-card>
          <transaction-form @close="dialog = !dialog" />
        </v-card>
      </template>
    </v-dialog>
  </div>
</template>
