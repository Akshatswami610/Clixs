import { Routes, Route } from "react-router-dom";
import ProtectedRoute from "@/components/ProtectedRoute";

<Route path="/" element={<HomePage />} />
<Route path="/items" element={<ItemsListPage />} />
<Route path="/items/:id" element={<ItemDetailPage />} />

<Route path="/login" element={<LoginPage />} />
<Route path="/signup" element={<SignupPage />} />

<Route element={<ProtectedRoute />}>
  <Route path="/upload-images" element={<UploadItemImagesPage />} />
  <Route path="/profile" element={<ProfilePage />} />
</Route>

<Route element={<ProtectedRoute admin />}>
  <Route path="/admin/contacts" element={<AdminContactsPage />} />
  <Route path="/admin/reports" element={<AdminReportsPage />} />
</Route>
