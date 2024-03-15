<script>
import { connect } from "~/api/notifications";
export default {
  mounted() {
    connect();
  },
};
</script>

<template>
  <div></div>
</template>
