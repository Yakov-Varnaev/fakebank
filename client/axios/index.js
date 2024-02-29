import axios from "axios";
import { HttpStatusCode } from "axios";
import { cloneDeep } from "lodash";
import decamelizeKeys from "decamelize-keys";

function onResponseError(error) {
  const auth = useAuth();
  const alert = useAlert();
  if (error.response.status === HttpStatusCode.Unauthorized) {
    auth.$reset();
    alert.reportWarning("Сессия истекла, пожалуйста, войдите заново");
    return Promise.reject(error);
  }

  if (error) {
    alert.reportError(error);
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

  console.log(request.data);
  return request;
}

function createAxios(config) {
  const instance = axios.create(config);
  instance.interceptors.request.use((value) => onRequestFullfilled(value));
  instance.interceptors.response.use(
    (res) => res,
    (error) => onResponseError(error),
  );
  return instance;
}

export const apiv1 = createAxios({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});
