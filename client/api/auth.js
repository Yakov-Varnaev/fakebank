import { apiv1 } from "~/axios";

export const login = async (loginData) => {
  useRuntimeConfig().public.apiHost;
  let formData = new FormData();
  Object.keys(loginData).forEach((key) => {
    formData.append(key, loginData[key]);
  });
  return await apiv1.post("/auth/login", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export const logout = async () => {
  return await apiv1.post("/auth/logout");
};

export const register = async (registerData) => {
  return await apiv1.post("/auth/register", registerData);
};

export const getMe = async () => {
  return await apiv1.get("/users/me");
};
