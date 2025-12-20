"use client"

import type React from "react"
import { useState } from "react"
import { Button } from "../../components/ui/button"
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "../../components/ui/card"
import { Label } from "../../components/ui/label"
import { Textarea } from "../../components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../../components/ui/select"
import { supportService } from "../../services/supportService"
import { Star, MessageSquare } from "lucide-react"

export function FeedbackPage() {
  const [loading, setLoading] = useState(false)
  const [submitted, setSubmitted] = useState(false)
  const [rating, setRating] = useState(0)
  const [hoveredRating, setHoveredRating] = useState(0)
  const [formData, setFormData] = useState({
    category: "",
    message: "",
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (rating === 0) {
      alert("Please select a rating")
      return
    }
    setLoading(true)
    try {
      await supportService.submitFeedback({
        rating,
        message: formData.message,
        category: formData.category as "bug" | "feature" | "general",
      })
      setSubmitted(true)
      setRating(0)
      setFormData({ category: "", message: "" })
    } catch (error) {
      console.error("[v0] Feedback submission error:", error)
      alert("Failed to submit feedback. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-background py-12">
      <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold">Share Your Feedback</h1>
          <p className="mt-3 text-lg text-muted-foreground">
            Help us improve Clixs by sharing your thoughts and suggestions
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <MessageSquare className="h-5 w-5" />
              Your Feedback Matters
            </CardTitle>
            <CardDescription>Tell us about your experience, report bugs, or suggest new features</CardDescription>
          </CardHeader>
          <CardContent>
            {submitted ? (
              <div className="rounded-lg bg-primary/10 p-8 text-center">
                <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-primary/20">
                  <Star className="h-8 w-8 text-primary" />
                </div>
                <h3 className="text-xl font-semibold">Thank You!</h3>
                <p className="mt-2 text-muted-foreground">
                  Your feedback helps us build a better marketplace for everyone.
                </p>
                <Button className="mt-6" onClick={() => setSubmitted(false)}>
                  Submit More Feedback
                </Button>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Rating */}
                <div className="space-y-2">
                  <Label>How would you rate your experience? *</Label>
                  <div className="flex items-center gap-2">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <button
                        key={star}
                        type="button"
                        onClick={() => setRating(star)}
                        onMouseEnter={() => setHoveredRating(star)}
                        onMouseLeave={() => setHoveredRating(0)}
                        className="transition-transform hover:scale-110"
                      >
                        <Star
                          className={`h-10 w-10 ${
                            star <= (hoveredRating || rating)
                              ? "fill-primary text-primary"
                              : "fill-none text-muted-foreground"
                          }`}
                        />
                      </button>
                    ))}
                    {rating > 0 && <span className="ml-2 text-sm text-muted-foreground">({rating}/5)</span>}
                  </div>
                </div>

                {/* Category */}
                <div className="space-y-2">
                  <Label htmlFor="category">Feedback Category *</Label>
                  <Select
                    value={formData.category}
                    onValueChange={(value) => setFormData({ ...formData, category: value })}
                  >
                    <SelectTrigger id="category">
                      <SelectValue placeholder="Select category" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="general">General Feedback</SelectItem>
                      <SelectItem value="bug">Bug Report</SelectItem>
                      <SelectItem value="feature">Feature Request</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* Message */}
                <div className="space-y-2">
                  <Label htmlFor="message">Your Feedback *</Label>
                  <Textarea
                    id="message"
                    placeholder="Tell us what you think, describe a bug, or suggest a new feature..."
                    rows={6}
                    required
                    value={formData.message}
                    onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                  />
                </div>

                <Button type="submit" className="w-full" disabled={loading}>
                  {loading ? "Submitting..." : "Submit Feedback"}
                </Button>
              </form>
            )}
          </CardContent>
        </Card>

        {/* Info Cards */}
        <div className="mt-8 grid gap-4 sm:grid-cols-2">
          <Card className="bg-muted/50 border-muted">
            <CardContent className="p-6">
              <h3 className="mb-2 font-semibold">Report Bugs</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Found something not working as expected? Let us know so we can fix it quickly.
              </p>
            </CardContent>
          </Card>
          <Card className="bg-muted/50 border-muted">
            <CardContent className="p-6">
              <h3 className="mb-2 font-semibold">Request Features</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Have an idea to make Clixs better? We'd love to hear your suggestions!
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
