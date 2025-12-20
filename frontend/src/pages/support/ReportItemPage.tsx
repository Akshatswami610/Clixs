"use client"

import type React from "react"
import { useState } from "react"
import { useSearchParams, useNavigate } from "react-router-dom"
import { Button } from "../../components/ui/button"
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "../../components/ui/card"
import { Label } from "../../components/ui/label"
import { Textarea } from "../../components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../../components/ui/select"
import { supportService } from "../../services/supportService"
import { AlertTriangle, Flag } from "lucide-react"

export function ReportItemPage() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [submitted, setSubmitted] = useState(false)
  const itemId = searchParams.get("itemId") || ""
  const [formData, setFormData] = useState({
    reason: "",
    description: "",
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!itemId) {
      alert("Item ID is required")
      return
    }
    setLoading(true)
    try {
      await supportService.reportItem({
        itemId,
        reason: formData.reason,
        description: formData.description,
      })
      setSubmitted(true)
    } catch (error) {
      console.error("[v0] Report submission error:", error)
      alert("Failed to submit report. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-background py-12">
      <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold">Report an Item</h1>
          <p className="mt-3 text-lg text-muted-foreground">
            Help us maintain a safe marketplace by reporting suspicious or inappropriate listings
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Flag className="h-5 w-5" />
              Submit a Report
            </CardTitle>
            <CardDescription>
              All reports are reviewed by our team. False reports may result in account suspension.
            </CardDescription>
          </CardHeader>
          <CardContent>
            {submitted ? (
              <div className="rounded-lg bg-primary/10 p-8 text-center">
                <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-primary/20">
                  <Flag className="h-8 w-8 text-primary" />
                </div>
                <h3 className="text-xl font-semibold">Report Submitted</h3>
                <p className="mt-2 text-muted-foreground">
                  Thank you for helping keep Clixs safe. Our team will review this report shortly.
                </p>
                <div className="mt-6 flex gap-3 justify-center">
                  <Button onClick={() => navigate("/items")}>Back to Marketplace</Button>
                  <Button variant="outline" onClick={() => setSubmitted(false)}>
                    Report Another Item
                  </Button>
                </div>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Item ID Display */}
                {itemId && (
                  <div className="rounded-lg bg-muted p-4">
                    <p className="text-sm text-muted-foreground">
                      Reporting Item ID: <span className="font-mono font-semibold text-foreground">{itemId}</span>
                    </p>
                  </div>
                )}

                {/* Reason */}
                <div className="space-y-2">
                  <Label htmlFor="reason">Reason for Report *</Label>
                  <Select
                    value={formData.reason}
                    onValueChange={(value) => setFormData({ ...formData, reason: value })}
                  >
                    <SelectTrigger id="reason">
                      <SelectValue placeholder="Select a reason" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="counterfeit">Counterfeit or Fake Product</SelectItem>
                      <SelectItem value="scam">Suspected Scam</SelectItem>
                      <SelectItem value="inappropriate">Inappropriate Content</SelectItem>
                      <SelectItem value="stolen">Stolen Item</SelectItem>
                      <SelectItem value="prohibited">Prohibited Item</SelectItem>
                      <SelectItem value="misleading">Misleading Description</SelectItem>
                      <SelectItem value="other">Other</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* Description */}
                <div className="space-y-2">
                  <Label htmlFor="description">Additional Details *</Label>
                  <Textarea
                    id="description"
                    placeholder="Please provide specific details about why you're reporting this item..."
                    rows={6}
                    required
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  />
                  <p className="text-sm text-muted-foreground">
                    The more details you provide, the faster we can investigate.
                  </p>
                </div>

                {/* Warning */}
                <Card className="border-destructive/50 bg-destructive/5">
                  <CardContent className="flex gap-3 p-4">
                    <AlertTriangle className="h-5 w-5 shrink-0 text-destructive" />
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      Please ensure your report is accurate. False or malicious reports may result in account suspension
                      or termination.
                    </p>
                  </CardContent>
                </Card>

                <div className="flex gap-3">
                  <Button type="submit" className="flex-1" disabled={loading}>
                    {loading ? "Submitting..." : "Submit Report"}
                  </Button>
                  <Button type="button" variant="outline" onClick={() => navigate(-1)} disabled={loading}>
                    Cancel
                  </Button>
                </div>
              </form>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
