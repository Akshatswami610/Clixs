import api from "@/lib/axios";

export const getContacts = () =>
  api.get("admin/contact/");

export const getReports = () =>
  api.get("admin/reports/");

export const getFeedback = () =>
  api.get("admin/feedback/");
