"use client"

import { Link, useNavigate } from "react-router-dom"
import { Button } from "./ui/button"
import { useAuth } from "../hooks/useAuth"
import { ShoppingBag, User, LogOut, Menu } from "lucide-react"
import { useState } from "react"

export function Navbar() {
  const { isAuthenticated, user } = useAuth()
  const navigate = useNavigate()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const handleLogout = () => {
    localStorage.removeItem("token")
    window.location.href = "/"
  }

  return (
    <nav className="sticky top-0 z-50 border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <ShoppingBag className="h-8 w-8 text-primary" />
            <span className="text-2xl font-bold">Clixs</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden items-center gap-8 md:flex">
            <Link to="/items" className="text-sm font-medium transition-colors hover:text-primary">
              Browse Items
            </Link>
            <Link to="/contact" className="text-sm font-medium transition-colors hover:text-primary">
              Contact
            </Link>
            {isAuthenticated && (
              <>
                <Link to="/upload-images" className="text-sm font-medium transition-colors hover:text-primary">
                  Sell Item
                </Link>
                <Link to="/feedback" className="text-sm font-medium transition-colors hover:text-primary">
                  Feedback
                </Link>
              </>
            )}
          </div>

          {/* Desktop Actions */}
          <div className="hidden items-center gap-3 md:flex">
            {isAuthenticated ? (
              <>
                <Button variant="ghost" size="icon" onClick={() => navigate("/profile")}>
                  <User className="h-5 w-5" />
                </Button>
                <Button variant="ghost" size="sm" onClick={handleLogout}>
                  <LogOut className="mr-2 h-4 w-4" />
                  Logout
                </Button>
              </>
            ) : (
              <Button onClick={() => navigate("/register")}>Get Started</Button>
            )}
          </div>

          {/* Mobile Menu Button */}
          <Button variant="ghost" size="icon" className="md:hidden" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
            <Menu className="h-6 w-6" />
          </Button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="border-t border-border py-4 md:hidden">
            <div className="flex flex-col gap-4">
              <Link to="/items" className="text-sm font-medium" onClick={() => setMobileMenuOpen(false)}>
                Browse Items
              </Link>
              <Link to="/contact" className="text-sm font-medium" onClick={() => setMobileMenuOpen(false)}>
                Contact
              </Link>
              {isAuthenticated ? (
                <>
                  <Link to="/upload-images" className="text-sm font-medium" onClick={() => setMobileMenuOpen(false)}>
                    Sell Item
                  </Link>
                  <Link to="/feedback" className="text-sm font-medium" onClick={() => setMobileMenuOpen(false)}>
                    Feedback
                  </Link>
                  <Link to="/profile" className="text-sm font-medium" onClick={() => setMobileMenuOpen(false)}>
                    Profile
                  </Link>
                  <Button variant="outline" size="sm" onClick={handleLogout} className="justify-start bg-transparent">
                    <LogOut className="mr-2 h-4 w-4" />
                    Logout
                  </Button>
                </>
              ) : (
                <Button onClick={() => navigate("/register")} className="w-full">
                  Get Started
                </Button>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
