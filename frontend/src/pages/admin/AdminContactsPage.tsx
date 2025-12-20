"use client"

import { useState, useEffect } from "react"
import { Card, CardContent } from "../../components/ui/card"
import { Button } from "../../components/ui/button"
import { Badge } from "../../components/ui/badge"
import type { AdminContact } from "../../services/adminService"
import { Mail, Calendar, User, CheckCircle } from "lucide-react"

// Dummy data
const dummyContacts: AdminContact[] = [
  {
    id: "1",
    name: "Sarah Johnson",
    email: "sarah@stanford.edu",
    subject: "Issue with item listing",
    message:
      "I'm having trouble uploading images for my MacBook listing. The upload button doesn't seem to be working properly.",
    createdAt: "2024-01-15T10:30:00Z",
    status: "pending",
  },
  {
    id: "2",
    name: "Mike Chen",
    email: "mike@mit.edu",
    subject: "Payment question",
    message:
      "How do payments work on Clixs? Is there an escrow system or do buyers pay sellers directly? Want to ensure safe transactions.",
    createdAt: "2024-01-14T14:20:00Z",
    status: "resolved",
  },
  {
    id: "3",
    name: "Emily Davis",
    email: "emily@berkeley.edu",
    subject: "Account verification",
    message: "My account hasn't been verified yet. I submitted my university email 3 days ago. Can you help?",
    createdAt: "2024-01-13T09:15:00Z",
    status: "pending",
  },
]

export function AdminContactsPage() {
  const [contacts, setContacts] = useState<AdminContact[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<"all" | "pending" | "resolved">("all")

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setContacts(dummyContacts)
      setLoading(false)
    }, 500)
  }, [])

  const filteredContacts = contacts.filter((contact) => {
    if (filter === "all") return true
    return contact.status === filter
  })

  const pendingCount = contacts.filter((c) => c.status === "pending").length

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
      </div>
    )
  }

  return (
    <div className="p-8">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Contact Submissions</h1>
          <p className="mt-2 text-muted-foreground">Manage and respond to user inquiries ({pendingCount} pending)</p>
        </div>
      </div>

      {/* Filters */}
      <div className="mb-6 flex gap-2">
        <Button variant={filter === "all" ? "default" : "outline"} size="sm" onClick={() => setFilter("all")}>
          All ({contacts.length})
        </Button>
        <Button variant={filter === "pending" ? "default" : "outline"} size="sm" onClick={() => setFilter("pending")}>
          Pending ({pendingCount})
        </Button>
        <Button variant={filter === "resolved" ? "default" : "outline"} size="sm" onClick={() => setFilter("resolved")}>
          Resolved ({contacts.length - pendingCount})
        </Button>
      </div>

      {/* Contacts List */}
      <div className="space-y-4">
        {filteredContacts.length === 0 ? (
          <Card>
            <CardContent className="p-12 text-center">
              <Mail className="mx-auto h-12 w-12 text-muted-foreground" />
              <p className="mt-4 text-muted-foreground">No contact submissions found</p>
            </CardContent>
          </Card>
        ) : (
          filteredContacts.map((contact) => (
            <Card key={contact.id} className="overflow-hidden">
              <CardContent className="p-6">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="mb-3 flex items-center gap-3">
                      <h3 className="text-lg font-semibold">{contact.subject}</h3>
                      <Badge variant={contact.status === "pending" ? "default" : "secondary"}>
                        {contact.status === "pending" ? "Pending" : "Resolved"}
                      </Badge>
                    </div>
                    <p className="mb-4 text-sm leading-relaxed text-muted-foreground">{contact.message}</p>
                    <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                      <div className="flex items-center gap-2">
                        <User className="h-4 w-4" />
                        {contact.name}
                      </div>
                      <div className="flex items-center gap-2">
                        <Mail className="h-4 w-4" />
                        {contact.email}
                      </div>
                      <div className="flex items-center gap-2">
                        <Calendar className="h-4 w-4" />
                        {new Date(contact.createdAt).toLocaleDateString()}
                      </div>
                    </div>
                  </div>
                  <div className="flex flex-col gap-2">
                    {contact.status === "pending" && (
                      <Button size="sm" className="whitespace-nowrap">
                        <CheckCircle className="mr-2 h-4 w-4" />
                        Mark Resolved
                      </Button>
                    )}
                    <Button size="sm" variant="outline">
                      View Details
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  )
}
