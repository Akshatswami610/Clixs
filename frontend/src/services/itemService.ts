import api from "@/lib/axios";

export const getItems = () => api.get("items/");
export const getItem = (id: number) =>
  api.get(`items/${id}/`);
