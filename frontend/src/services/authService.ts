import api from "@/lib/axios";

export const signup = (data: any) =>
  api.post("auth/register/", data);

export const getProfile = () =>
  api.get("auth/profile/");
