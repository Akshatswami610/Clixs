"use client"

import { useState, useEffect } from "react"
import { authService, type User } from "../services/authService"

export function useAuth() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem("token")
    if (token) {
      authService
        .getProfile()
        .then((userData) => setUser(userData))
        .catch(() => localStorage.removeItem("token"))
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  return {
    user,
    isAuthenticated: !!user,
    isAdmin: user?.role === "admin",
    loading,
    setUser,
  }
}
