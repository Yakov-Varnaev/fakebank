import { apiv1 } from "~/axios";

export const createTransaction = async (payload) => {
  return await apiv1.post("/transactions", payload);
};
