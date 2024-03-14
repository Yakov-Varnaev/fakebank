import { apiv1 } from "~/axios";

export const fetchUsers = async (offset, limit, query = null) => {
  const params = { offset, limit };
  if (query) params.query = query;
  return await apiv1.get("/users", { params });
};
