"use client"

import { useState, useEffect } from "react"
import { Link } from "react-router-dom"
import { Card, CardContent, CardFooter } from "../../components/ui/card"
import { Button } from "../../components/ui/button"
import { Input } from "../../components/ui/input"
import type { Item } from "../../services/itemService"
import { Search, MapPin } from "lucide-react"

// Dummy data for demonstration
const dummyItems: Item[] = [
  {
    id: "1",
    title: 'MacBook Pro 14" M1 Pro',
    description: "Excellent condition, barely used. Comes with original charger and box.",
    price: 1299,
    category: "electronics",
    condition: "like-new",
    images: ["/macbook-pro-laptop.png"],
    seller: {
      id: "1",
      name: "Sarah Johnson",
      university: "Stanford University",
    },
    createdAt: "2024-01-15T10:00:00Z",
  },
  {
    id: "2",
    title: "Data Structures and Algorithms Textbook",
    description: "CLRS 3rd Edition. Great condition with minimal highlighting.",
    price: 45,
    category: "books",
    condition: "good",
    images: ["/algorithms-textbook-book.jpg"],
    seller: {
      id: "2",
      name: "Mike Chen",
      university: "MIT",
    },
    createdAt: "2024-01-14T15:30:00Z",
  },
  {
    id: "3",
    title: "Mountain Bike - Trek Marlin 7",
    description: "Well-maintained bike, perfect for campus commuting and weekend trails.",
    price: 450,
    category: "cycles",
    condition: "good",
    images: ["/mountain-bike-bicycle.jpg"],
    seller: {
      id: "3",
      name: "Emily Davis",
      university: "UC Berkeley",
    },
    createdAt: "2024-01-13T09:15:00Z",
  },
  {
    id: "4",
    title: "Mini Fridge for Dorm",
    description: "Compact mini fridge, perfect for dorm rooms. Energy efficient.",
    price: 80,
    category: "hostel-items",
    condition: "good",
    images: ["/mini-fridge-refrigerator.jpg"],
    seller: {
      id: "4",
      name: "Alex Turner",
      university: "Stanford University",
    },
    createdAt: "2024-01-12T14:20:00Z",
  },
  {
    id: "5",
    title: "iPad Air 5th Gen with Apple Pencil",
    description: "64GB, Space Gray. Includes Apple Pencil 2nd gen and case.",
    price: 525,
    category: "electronics",
    condition: "like-new",
    images: ["/ipad-air-tablet.jpg"],
    seller: {
      id: "5",
      name: "Jessica Lee",
      university: "Harvard University",
    },
    createdAt: "2024-01-11T11:45:00Z",
  },
  {
    id: "6",
    title: "Organic Chemistry Study Set",
    description: "Bundle of 3 textbooks + study guide. Perfect for pre-med students.",
    price: 120,
    category: "books",
    condition: "good",
    images: ["/chemistry-textbooks-books.jpg"],
    seller: {
      id: "6",
      name: "David Kim",
      university: "Stanford University",
    },
    createdAt: "2024-01-10T16:00:00Z",
  },
]

export function ItemsListPage() {
  const [items, setItems] = useState<Item[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedCategory, setSelectedCategory] = useState<string>("all")

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setItems(dummyItems)
      setLoading(false)
    }, 500)
  }, [])

  const filteredItems = items.filter((item) => {
    const matchesSearch = item.title.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesCategory = selectedCategory === "all" || item.category === selectedCategory
    return matchesSearch && matchesCategory
  })

  const categories = [
    { value: "all", label: "All Items" },
    { value: "electronics", label: "Electronics" },
    { value: "books", label: "Books" },
    { value: "cycles", label: "Cycles" },
    { value: "hostel-items", label: "Hostel Items" },
  ]

  if (loading) {
    return (
      <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
      </div>
    )
  }

  return (
    <div className="bg-background">
      {/* Header */}
      <div className="border-b border-border bg-card">
        <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold">Browse Marketplace</h1>
          <p className="mt-2 text-muted-foreground">
            Discover electronics, books, cycles, and more from students in your university
          </p>
        </div>
      </div>

      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Search and Filters */}
        <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Search items..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>
          <div className="flex gap-2 overflow-x-auto">
            {categories.map((category) => (
              <Button
                key={category.value}
                variant={selectedCategory === category.value ? "default" : "outline"}
                size="sm"
                onClick={() => setSelectedCategory(category.value)}
                className="whitespace-nowrap"
              >
                {category.label}
              </Button>
            ))}
          </div>
        </div>

        {/* Items Grid */}
        {filteredItems.length === 0 ? (
          <div className="flex min-h-[400px] items-center justify-center">
            <div className="text-center">
              <p className="text-lg font-medium">No items found</p>
              <p className="mt-2 text-sm text-muted-foreground">Try adjusting your search or filters</p>
            </div>
          </div>
        ) : (
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {filteredItems.map((item) => (
              <Link key={item.id} to={`/items/${item.id}`}>
                <Card className="group h-full overflow-hidden transition-all hover:shadow-lg">
                  <div className="aspect-square overflow-hidden bg-muted">
                    <img
                      src={item.images[0] || "/placeholder.svg"}
                      alt={item.title}
                      className="h-full w-full object-cover transition-transform group-hover:scale-105"
                    />
                  </div>
                  <CardContent className="p-4">
                    <div className="mb-2 flex items-start justify-between gap-2">
                      <h3 className="font-semibold leading-snug line-clamp-2">{item.title}</h3>
                      <span className="text-lg font-bold text-primary whitespace-nowrap">${item.price}</span>
                    </div>
                    <p className="text-sm text-muted-foreground line-clamp-2">{item.description}</p>
                    <div className="mt-3 flex items-center gap-2">
                      <span className="rounded-full bg-primary/10 px-2 py-1 text-xs font-medium text-primary">
                        {item.condition}
                      </span>
                      <span className="rounded-full bg-secondary px-2 py-1 text-xs font-medium capitalize">
                        {item.category.replace("-", " ")}
                      </span>
                    </div>
                  </CardContent>
                  <CardFooter className="border-t border-border p-4">
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <MapPin className="h-4 w-4" />
                      <span className="truncate">{item.seller.university}</span>
                    </div>
                  </CardFooter>
                </Card>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
export default ItemsListPage;