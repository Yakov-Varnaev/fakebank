<script>
export default {
  setup() {
    return { alertStore: useAlert() };
  },
  computed: {
    alerts() {
      return this.alertStore.alerts;
    },
  },
};
</script>

<template>
  <div class="alerts_container ma-5">
    <AlertMessage v-for="alert in alerts" :type="alert.type" :text="alert.text" :key="alert.id" class="mt-2"
      :alert="alert" />
  </div>
</template>

<style scoped>
.alerts_container {
  bottom: 0;
  right: 0;
  position: absolute;
  width: 30vh;
  max-height: 400px;
}
</style>
