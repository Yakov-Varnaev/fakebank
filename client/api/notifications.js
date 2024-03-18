const config = useRuntimeConfig();

const host = config.public.apiHost;

export const connect = () => {
  const socket = new WebSocket(
    `ws://${host}/api/notifications/ws`,
  );

  const alertStore = useAlert();

  socket.onopen = (event) => {
    console.log("WebSocket connection opened:", event);
  };

  socket.onmessage = async (event) => {
    let notification = JSON.parse(event.data);
    const user_id = useAuth().user.id;
    console.log(user_id);
    console.log("Update accounts");
    await useAccounts().getAccounts(user_id);
    console.log("Update transactions");
    await useTransactions().getTransactions();
    alertStore.reportInfo(notification.message);
  };

  socket.onclose = (event) => {
    console.log("WebSocket connection closed:", event);
  };

  socket.onerror = (event) => {
    console.error("WebSocket error:", event);
  };
};
