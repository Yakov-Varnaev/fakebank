<script>
export default {
  setup() {
    return { alertStore: useAlert() };
  },
  props: {
    alert: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      active: true,
    };
  },
  mounted() {
    setTimeout(() => {
      this.active = false;
      this.alertStore.removeAlert(this.alert.id);
    }, 5000);
  },
};
</script>
<template>
  <v-alert v-bind="$attrs" v-show="active" :closable="true" />
</template>
