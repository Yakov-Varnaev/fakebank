<script>
export default {
  props: {
    isSubmitDisabled: {
      type: Boolean,
    },
  },
};
</script>
<template>
  <v-row no-gutters>
    <v-col class="mx-1">
      <submit-btn
        variant="tonal"
        block
        @click="$emit('submit')"
        :disabled="isSubmitDisabled"
      />
    </v-col>
    <v-col class="mx-1">
      <cancel-btn variant="tonal" block @click="$emit('cancel')" />
    </v-col>
  </v-row>
</template>
