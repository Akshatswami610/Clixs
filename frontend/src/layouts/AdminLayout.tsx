import { Outlet, Link, useLocation } from "react-router-dom"
import { Button } from "../components/ui/button"
import { Mail, Flag, MessageSquare, Home } from "lucide-react"

export function AdminLayout() {
  const location = useLocation()

  const isActive = (path: string) => location.pathname === path

  return (
    <div className="flex min-h-screen bg-background">
      {/* Sidebar */}
      <aside className="w-64 border-r border-border bg-card">
        <div className="flex h-16 items-center border-b border-border px-6">
          <h2 className="text-lg font-bold">Admin Panel</h2>
        </div>
        <nav className="space-y-2 p-4">
          <Link to="/">
            <Button variant={isActive("/") ? "secondary" : "ghost"} className="w-full justify-start">
              <Home className="mr-2 h-4 w-4" />
              Back to Home
            </Button>
          </Link>
          <Link to="/admin/contacts">
            <Button variant={isActive("/admin/contacts") ? "secondary" : "ghost"} className="w-full justify-start">
              <Mail className="mr-2 h-4 w-4" />
              Contacts
            </Button>
          </Link>
          <Link to="/admin/reports">
            <Button variant={isActive("/admin/reports") ? "secondary" : "ghost"} className="w-full justify-start">
              <Flag className="mr-2 h-4 w-4" />
              Reports
            </Button>
          </Link>
          <Link to="/admin/feedback">
            <Button variant={isActive("/admin/feedback") ? "secondary" : "ghost"} className="w-full justify-start">
              <MessageSquare className="mr-2 h-4 w-4" />
              Feedback
            </Button>
          </Link>
        </nav>
      </aside>

      {/* Main Content */}
      <div className="flex-1">
        <Outlet />
      </div>
    </div>
  )
}
