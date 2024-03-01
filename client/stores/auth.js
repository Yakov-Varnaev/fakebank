import { defineStore } from "pinia";
import {
  getMe,
  login as apiLogin,
  logout as apiLogout,
  register as apiRegister,
} from "@/api/auth.js";
import { useLoader } from "~/stores/loader";
import { HttpStatusCode } from "axios";

const initialState = () => ({
  loggedIn: false,
  user: null,
});

export const useAuth = defineStore("auth", {
  state: initialState,
  actions: {
    reset() {
      Object.assign(this, initialState());
    },
    async _register(registerData) {
      try {
        await apiRegister(registerData);
      } catch (error) {
        console.log(error);
        return { errors: error.response.data };
      }
      navigateTo({ name: "signin" });
      return {};
    },
    async _login(loginData, report = true) {
      const alerts = useAlert();
      try {
        await apiLogin(loginData);
        this.loggedIn = true;
        if (report) {
          alerts.reportInfo("Welcome!");
        }
      } catch ({ response }) {
        if (response.status === HttpStatusCode.BadRequest) {
          return { errors: response.data };
        } else if (response.status === HttpStatusCode.Unauthorized) {
          alerts.reportError("Invalid credentials");
          return {};
        }
        alerts.reportError(`Something went wrong! ${response.status}`);
        return {};
      }
      await this.getMe();
      navigateTo({ name: "index" });
      return {};
    },
    async _logout() {
      const alert = useAlert();
      try {
        await apiLogout();
      } catch (error) {
        console.log(error);
      }
      this.reset();
      alert.reportWarning("You have been logged out!");
      navigateTo({ name: "signin" });
    },
    async logout() {
      const loader = useLoader();
      loader.start();
      await this._logout();
      loader.stop();
    },
    async login(loginData) {
      const loader = useLoader();
      loader.start();
      await this._login(loginData);
      loader.stop();
    },
    async register(registerData) {
      const loader = useLoader();
      loader.start();
      let resp = await this._register(registerData);
      loader.stop();
      return resp;
    },
    async getMe() {
      const alerts = useAlert();
      try {
        const { data } = await getMe();
        this.user = data;
      } catch (error) {
        alerts.reportError("Can't get user data. " + error.message);
      }
    },
  },
  persist: true,
});
