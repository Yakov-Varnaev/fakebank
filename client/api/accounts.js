import { apiv1 } from "~/axios";

export const fetchAccounts = async (
  offset,
  limit,
  user_id = null,
  query = null,
) => {
  const params = { offset, limit };
  if (query !== null) {
    params.query = query;
  }
  if (user_id !== null) {
    params.user_id = user_id;
  }

  return await apiv1.get("/accounts", { params });
};
