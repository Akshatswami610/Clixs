"use client"

import { useState, useEffect } from "react"
import { Card, CardContent } from "../../components/ui/card"
import { Button } from "../../components/ui/button"
import { Badge } from "../../components/ui/badge"
import type { AdminReport } from "../../services/adminService"
import { Flag, Calendar, User, AlertTriangle, CheckCircle } from "lucide-react"

// Dummy data
const dummyReports: AdminReport[] = [
  {
    id: "1",
    itemId: "item-123",
    reason: "Suspected Scam",
    description:
      "The seller is asking for payment outside the platform via Venmo. This seems very suspicious and against platform policies.",
    createdAt: "2024-01-15T11:00:00Z",
    reporterName: "Alex Turner",
    status: "pending",
  },
  {
    id: "2",
    itemId: "item-456",
    reason: "Counterfeit Product",
    description:
      "The AirPods being sold look fake. The charging case has incorrect branding and the serial number doesn't check out on Apple's website.",
    createdAt: "2024-01-14T16:45:00Z",
    reporterName: "Jessica Lee",
    status: "investigating",
  },
  {
    id: "3",
    itemId: "item-789",
    reason: "Inappropriate Content",
    description: "The item photos contain inappropriate content that violates community guidelines.",
    createdAt: "2024-01-13T13:20:00Z",
    reporterName: "David Kim",
    status: "resolved",
  },
]

export function AdminReportsPage() {
  const [reports, setReports] = useState<AdminReport[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<"all" | "pending" | "investigating" | "resolved">("all")

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setReports(dummyReports)
      setLoading(false)
    }, 500)
  }, [])

  const filteredReports = reports.filter((report) => {
    if (filter === "all") return true
    return report.status === filter
  })

  const pendingCount = reports.filter((r) => r.status === "pending").length
  const investigatingCount = reports.filter((r) => r.status === "investigating").length

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
          <h1 className="text-3xl font-bold">Item Reports</h1>
          <p className="mt-2 text-muted-foreground">
            Review and take action on reported items ({pendingCount} pending, {investigatingCount} investigating)
          </p>
        </div>
      </div>

      {/* Filters */}
      <div className="mb-6 flex gap-2">
        <Button variant={filter === "all" ? "default" : "outline"} size="sm" onClick={() => setFilter("all")}>
          All ({reports.length})
        </Button>
        <Button variant={filter === "pending" ? "default" : "outline"} size="sm" onClick={() => setFilter("pending")}>
          Pending ({pendingCount})
        </Button>
        <Button
          variant={filter === "investigating" ? "default" : "outline"}
          size="sm"
          onClick={() => setFilter("investigating")}
        >
          Investigating ({investigatingCount})
        </Button>
        <Button variant={filter === "resolved" ? "default" : "outline"} size="sm" onClick={() => setFilter("resolved")}>
          Resolved
        </Button>
      </div>

      {/* Reports List */}
      <div className="space-y-4">
        {filteredReports.length === 0 ? (
          <Card>
            <CardContent className="p-12 text-center">
              <Flag className="mx-auto h-12 w-12 text-muted-foreground" />
              <p className="mt-4 text-muted-foreground">No reports found</p>
            </CardContent>
          </Card>
        ) : (
          filteredReports.map((report) => (
            <Card
              key={report.id}
              className={`overflow-hidden ${report.status === "pending" ? "border-destructive/50" : ""}`}
            >
              <CardContent className="p-6">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="mb-3 flex items-center gap-3">
                      <AlertTriangle className="h-5 w-5 text-destructive" />
                      <h3 className="text-lg font-semibold">{report.reason}</h3>
                      <Badge
                        variant={
                          report.status === "pending"
                            ? "destructive"
                            : report.status === "investigating"
                              ? "default"
                              : "secondary"
                        }
                      >
                        {report.status}
                      </Badge>
                    </div>
                    <p className="mb-4 text-sm leading-relaxed text-muted-foreground">{report.description}</p>
                    <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
                      <div className="flex items-center gap-2">
                        <User className="h-4 w-4" />
                        Reported by: {report.reporterName}
                      </div>
                      <div className="flex items-center gap-2">
                        <Flag className="h-4 w-4" />
                        Item ID: <span className="font-mono">{report.itemId}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Calendar className="h-4 w-4" />
                        {new Date(report.createdAt).toLocaleDateString()}
                      </div>
                    </div>
                  </div>
                  <div className="flex flex-col gap-2">
                    {report.status === "pending" && (
                      <Button size="sm" className="whitespace-nowrap">
                        Start Investigation
                      </Button>
                    )}
                    {report.status === "investigating" && (
                      <Button size="sm" variant="outline" className="whitespace-nowrap bg-transparent">
                        <CheckCircle className="mr-2 h-4 w-4" />
                        Mark Resolved
                      </Button>
                    )}
                    <Button size="sm" variant="outline">
                      View Item
                    </Button>
                    <Button size="sm" variant="destructive">
                      Remove Item
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
