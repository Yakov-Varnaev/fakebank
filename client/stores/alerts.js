import { defineStore } from "pinia";

export const useAlert = defineStore("alert", {
  state: () => ({
    alerts: [],
  }),
  actions: {
    addAlert(alert) {
      alert.id = Date.now();
      alert.numeric = this.alerts.length + 1;
      this.alerts = [...this.alerts, alert];
    },
    reportError(text) {
      this.addAlert({
        type: "error",
        text: text,
      });
    },
    reportInfo(text) {
      this.addAlert({
        type: "info",
        text: text,
      });
    },
    reportWarning(text) {
      this.addAlert({
        type: "warning",
        text: text,
      });
    },
    reportDev(text) {
      this.addAlert({
        text,
        color: "secondary",
        icon: "mdi-bug",
      });
    },
    removeAlert(id) {
      this.alerts = this.alerts.filter((a) => a.id !== id);
    },
  },
});
