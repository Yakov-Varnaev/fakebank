import axios from "axios";
import { HttpStatusCode } from "axios";
import { cloneDeep } from "lodash";
import decamelizeKeys from "decamelize-keys";

function onResponseError(error) {
  const auth = useAuth();
  const alert = useAlert();
  console.log(error);
  if (error.response.status === HttpStatusCode.Unauthorized) {
    auth.$reset();
    alert.reportWarning("Session expired, please login again.");
    navigateTo("/signin");
    return Promise.reject(error);
  }

  return Promise.reject(error);
}

const requestCaseMiddleware = (data, enable = true) =>
  enable ? decamelizeKeys(data, { deep: true }) : data;

function onRequestFullfilled(request) {
  request = cloneDeep(request);

  if (!(request.data instanceof FormData)) {
    request.data = requestCaseMiddleware(request.data);
  }

  return request;
}

function createAxios(config) {
  console.log(useRuntimeConfig().public.apiHost);
  const instance = axios.create(config);
  instance.interceptors.request.use((value) => onRequestFullfilled(value));
  instance.interceptors.response.use(
    (res) => res,
    (error) => onResponseError(error),
  );
  return instance;
}

export const apiv1 = createAxios({
  baseURL: "http://" + useRuntimeConfig().public.apiHost,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});
