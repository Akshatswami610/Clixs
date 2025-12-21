import { Routes, Route } from "react-router-dom";

import HomePage from "./pages/HomePage";
import ItemsListPage from "./pages/marketplace/ItemsListPage";
import ItemDetailPage from "./pages/marketplace/ItemDetailPage";
import RegisterPage from "./pages/auth/RegisterPage";
import ProfilePage from "./pages/auth/ProfilePage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/items" element={<ItemsListPage />} />
      <Route path="/items/:id" element={<ItemDetailPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/profile" element={<ProfilePage />} />
    </Routes>
  );
}

export default App;
