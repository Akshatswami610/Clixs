import api from "@/lib/axios";

export type User = {
  id: number;
  email: string;
};

export const authService = {
  signup: (data: any) => api.post("auth/register/", data),
  getProfile: () => api.get("auth/profile/"),
};
