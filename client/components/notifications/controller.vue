<script setup>
const config = useRuntimeConfig();
const socket = new WebSocket(`ws://${config.public.apiHost}/notifications/ws`);

const alertStore = useAlert();

socket.onopen = (event) => {
  console.log("WebSocket connection opened:", event);
};

socket.onmessage = (event) => {
  let notification = JSON.parse(event.data);
  alertStore.reportInfo(notification.message);
};

socket.onclose = (event) => {
  console.log("WebSocket connection closed:", event);
};

socket.onerror = (event) => {
  console.error("WebSocket error:", event);
};
</script>

<template>
  <div></div>
</template>
