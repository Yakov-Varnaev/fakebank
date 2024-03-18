const config = useRuntimeConfig();

const host = config.public.apiHost;

export const connect = () => {
  const socket = new WebSocket(
    `ws://${host}/api/notifications/ws`,
  );

  socket.onmessage = async (event) => {
    let notification = JSON.parse(event.data);
    const user_id = useAuth().user.id;
    await useAccounts().getAccounts(user_id);
    await useTransactions().getTransactions();
    useAlert().reportInfo(notification.message);
  };

  socket.onerror = (event) => {
    useAlert().reportError("Oops. Notifications are broken :/.");
  };
};
