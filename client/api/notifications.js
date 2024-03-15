const config = useRuntimeConfig();

const host = config.public.apiHost;

export const connect = () => {
  const socket = new WebSocket(
    `ws://${host}/notifications/ws`,
  );

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
};
