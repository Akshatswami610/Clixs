import api from "@/lib/axios";

export const contact = (data: any) =>
  api.post("contact/", data);

export const feedback = (data: any) =>
  api.post("feedback/", data);

export const report = (data: any) =>
  api.post("reports/", data);
