import { Link } from "react-router-dom"
import { ShoppingBag, Mail, MessageSquare, Flag } from "lucide-react"

export function Footer() {
  return (
    <footer className="border-t border-border bg-card">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-4">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <Link to="/" className="flex items-center gap-2">
              <ShoppingBag className="h-8 w-8 text-primary" />
              <span className="text-2xl font-bold">Clixs</span>
            </Link>
            <p className="mt-4 text-sm text-muted-foreground leading-relaxed">
              Your trusted university marketplace for buying and selling electronics, books, cycles, and hostel items.
              Built by students, for students.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-sm font-semibold">Quick Links</h3>
            <ul className="mt-4 space-y-3">
              <li>
                <Link to="/items" className="text-sm text-muted-foreground hover:text-foreground">
                  Browse Items
                </Link>
              </li>
              <li>
                <Link to="/upload-images" className="text-sm text-muted-foreground hover:text-foreground">
                  Sell Item
                </Link>
              </li>
              <li>
                <Link to="/profile" className="text-sm text-muted-foreground hover:text-foreground">
                  My Profile
                </Link>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="text-sm font-semibold">Support</h3>
            <ul className="mt-4 space-y-3">
              <li>
                <Link
                  to="/contact"
                  className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground"
                >
                  <Mail className="h-4 w-4" />
                  Contact Us
                </Link>
              </li>
              <li>
                <Link
                  to="/feedback"
                  className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground"
                >
                  <MessageSquare className="h-4 w-4" />
                  Feedback
                </Link>
              </li>
              <li>
                <Link
                  to="/report"
                  className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground"
                >
                  <Flag className="h-4 w-4" />
                  Report Item
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-12 border-t border-border pt-8">
          <p className="text-center text-sm text-muted-foreground">
            © {new Date().getFullYear()} Clixs. Built for university communities.
          </p>
        </div>
      </div>
    </footer>
  )
}
