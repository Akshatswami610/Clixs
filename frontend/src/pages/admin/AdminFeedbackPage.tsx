"use client"

import { useState, useEffect } from "react"
import { Card, CardContent } from "../../components/ui/card"
import { Button } from "../../components/ui/button"
import { Badge } from "../../components/ui/badge"
import type { AdminFeedback } from "../../services/adminService"
import { MessageSquare, Calendar, User, Star, CheckCircle } from "lucide-react"

// Dummy data
const dummyFeedback: AdminFeedback[] = [
  {
    id: "1",
    rating: 5,
    message:
      "Love the platform! It's so much easier to buy and sell items within my university community. The interface is clean and intuitive.",
    category: "general",
    createdAt: "2024-01-15T12:00:00Z",
    userName: "Sarah Johnson",
    status: "pending",
  },
  {
    id: "2",
    rating: 4,
    message:
      "Great app overall, but would love to see a built-in messaging system so I don't have to share my personal contact info.",
    category: "feature",
    createdAt: "2024-01-14T15:30:00Z",
    userName: "Mike Chen",
    status: "reviewed",
  },
  {
    id: "3",
    rating: 3,
    message:
      "The image upload keeps failing when I try to upload more than 3 photos. Getting an error message that isn't very helpful.",
    category: "bug",
    createdAt: "2024-01-13T10:45:00Z",
    userName: "Emily Davis",
    status: "pending",
  },
]

export function AdminFeedbackPage() {
  const [feedback, setFeedback] = useState<AdminFeedback[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<"all" | "pending" | "reviewed">("all")
  const [categoryFilter, setCategoryFilter] = useState<"all" | "general" | "bug" | "feature">("all")

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setFeedback(dummyFeedback)
      setLoading(false)
    }, 500)
  }, [])

  const filteredFeedback = feedback.filter((item) => {
    if (filter !== "all" && item.status !== filter) return false
    if (categoryFilter !== "all" && item.category !== categoryFilter) return false
    return true
  })

  const pendingCount = feedback.filter((f) => f.status === "pending").length
  const averageRating = (feedback.reduce((sum, f) => sum + f.rating, 0) / feedback.length).toFixed(1)

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
          <h1 className="text-3xl font-bold">User Feedback</h1>
          <p className="mt-2 text-muted-foreground">
            Review user feedback and suggestions (Average: {averageRating}/5, {pendingCount} pending review)
          </p>
        </div>
      </div>

      {/* Filters */}
      <div className="mb-6 space-y-3">
        <div className="flex gap-2">
          <Button variant={filter === "all" ? "default" : "outline"} size="sm" onClick={() => setFilter("all")}>
            All ({feedback.length})
          </Button>
          <Button variant={filter === "pending" ? "default" : "outline"} size="sm" onClick={() => setFilter("pending")}>
            Pending ({pendingCount})
          </Button>
          <Button
            variant={filter === "reviewed" ? "default" : "outline"}
            size="sm"
            onClick={() => setFilter("reviewed")}
          >
            Reviewed
          </Button>
        </div>
        <div className="flex gap-2">
          <Button
            variant={categoryFilter === "all" ? "secondary" : "outline"}
            size="sm"
            onClick={() => setCategoryFilter("all")}
          >
            All Categories
          </Button>
          <Button
            variant={categoryFilter === "general" ? "secondary" : "outline"}
            size="sm"
            onClick={() => setCategoryFilter("general")}
          >
            General
          </Button>
          <Button
            variant={categoryFilter === "bug" ? "secondary" : "outline"}
            size="sm"
            onClick={() => setCategoryFilter("bug")}
          >
            Bugs
          </Button>
          <Button
            variant={categoryFilter === "feature" ? "secondary" : "outline"}
            size="sm"
            onClick={() => setCategoryFilter("feature")}
          >
            Features
          </Button>
        </div>
      </div>

      {/* Feedback List */}
      <div className="space-y-4">
        {filteredFeedback.length === 0 ? (
          <Card>
            <CardContent className="p-12 text-center">
              <MessageSquare className="mx-auto h-12 w-12 text-muted-foreground" />
              <p className="mt-4 text-muted-foreground">No feedback found</p>
            </CardContent>
          </Card>
        ) : (
          filteredFeedback.map((item) => (
            <Card key={item.id} className="overflow-hidden">
              <CardContent className="p-6">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="mb-3 flex items-center gap-3">
                      <div className="flex items-center gap-1">
                        {Array.from({ length: 5 }).map((_, i) => (
                          <Star
                            key={i}
                            className={`h-4 w-4 ${i < item.rating ? "fill-primary text-primary" : "fill-none text-muted-foreground"}`}
                          />
                        ))}
                      </div>
                      <Badge variant="outline" className="capitalize">
                        {item.category}
                      </Badge>
                      <Badge variant={item.status === "pending" ? "default" : "secondary"}>
                        {item.status === "pending" ? "Pending" : "Reviewed"}
                      </Badge>
                    </div>
                    <p className="mb-4 text-sm leading-relaxed text-muted-foreground">{item.message}</p>
                    <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                      <div className="flex items-center gap-2">
                        <User className="h-4 w-4" />
                        {item.userName}
                      </div>
                      <div className="flex items-center gap-2">
                        <Calendar className="h-4 w-4" />
                        {new Date(item.createdAt).toLocaleDateString()}
                      </div>
                    </div>
                  </div>
                  <div className="flex flex-col gap-2">
                    {item.status === "pending" && (
                      <Button size="sm" className="whitespace-nowrap">
                        <CheckCircle className="mr-2 h-4 w-4" />
                        Mark Reviewed
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
