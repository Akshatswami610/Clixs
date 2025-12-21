"use client"

import { useState, useEffect } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { Button } from "../../components/ui/button"
import { Card, CardContent } from "../../components/ui/card"
import type { Item } from "../../services/itemService"
import { ArrowLeft, MapPin, Calendar, Shield, MessageCircle, Flag } from "lucide-react"

// Dummy data
const dummyItems: Item[] = [
  {
    id: "1",
    title: 'MacBook Pro 14" M1 Pro',
    description:
      "Excellent condition MacBook Pro with M1 Pro chip. This laptop has been barely used and comes with the original charger, USB-C cable, and original box. Perfect for students who need a powerful machine for coding, video editing, or general use.\n\nSpecifications:\n- 14-inch Liquid Retina XDR display\n- Apple M1 Pro chip with 8-core CPU\n- 16GB unified memory\n- 512GB SSD storage\n- Three Thunderbolt 4 ports\n- MagSafe 3 charging\n\nNo scratches or dents. Battery health at 98%. Still under AppleCare warranty until December 2024.",
    price: 1299,
    category: "electronics",
    condition: "like-new",
    images: ["/macbook-pro-laptop-front.jpg", "/macbook-pro-laptop-keyboard.jpg", "/macbook-pro-laptop-ports.jpg"],
    seller: {
      id: "1",
      name: "Sarah Johnson",
      university: "Stanford University",
    },
    createdAt: "2024-01-15T10:00:00Z",
  },
]

export function ItemDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [item, setItem] = useState<Item | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedImage, setSelectedImage] = useState(0)

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      const foundItem = dummyItems.find((i) => i.id === id)
      setItem(foundItem || null)
      setLoading(false)
    }, 500)
  }, [id])

  if (loading) {
    return (
      <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
      </div>
    )
  }

  if (!item) {
    return (
      <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center px-4">
        <Card className="w-full max-w-md">
          <CardContent className="pt-6 text-center">
            <p className="text-muted-foreground">Item not found</p>
            <Button className="mt-4" onClick={() => navigate("/items")}>
              Back to Marketplace
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  const formattedDate = new Date(item.createdAt).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  })

  return (
    <div className="bg-background">
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <Button variant="ghost" className="mb-6 -ml-4" onClick={() => navigate("/items")}>
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Marketplace
        </Button>

        <div className="grid gap-8 lg:grid-cols-2">
          {/* Images */}
          <div className="space-y-4">
            <Card className="overflow-hidden">
              <div className="aspect-square bg-muted">
                <img
                  src={item.images[selectedImage] || "/placeholder.svg"}
                  alt={item.title}
                  className="h-full w-full object-cover"
                />
              </div>
            </Card>
            {item.images.length > 1 && (
              <div className="grid grid-cols-3 gap-4">
                {item.images.map((image, index) => (
                  <button
                    key={index}
                    onClick={() => setSelectedImage(index)}
                    className={`aspect-square overflow-hidden rounded-lg border-2 transition-all ${
                      selectedImage === index ? "border-primary" : "border-border hover:border-muted-foreground"
                    }`}
                  >
                    <img
                      src={image || "/placeholder.svg"}
                      alt={`${item.title} ${index + 1}`}
                      className="h-full w-full object-cover"
                    />
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Details */}
          <div className="space-y-6">
            <div>
              <div className="mb-2 flex items-start justify-between gap-4">
                <h1 className="text-3xl font-bold text-balance">{item.title}</h1>
                <span className="text-3xl font-bold text-primary whitespace-nowrap">${item.price}</span>
              </div>
              <div className="flex flex-wrap gap-2">
                <span className="rounded-full bg-primary/10 px-3 py-1 text-sm font-medium text-primary capitalize">
                  {item.condition.replace("-", " ")}
                </span>
                <span className="rounded-full bg-secondary px-3 py-1 text-sm font-medium capitalize">
                  {item.category.replace("-", " ")}
                </span>
              </div>
            </div>

            <Card>
              <CardContent className="p-6">
                <h2 className="mb-3 text-lg font-semibold">Description</h2>
                <p className="whitespace-pre-line text-sm leading-relaxed text-muted-foreground">{item.description}</p>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-6">
                <h2 className="mb-4 text-lg font-semibold">Seller Information</h2>
                <div className="space-y-3">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
                      <Shield className="h-5 w-5 text-primary" />
                    </div>
                    <div>
                      <p className="font-medium">{item.seller.name}</p>
                      <p className="text-sm text-muted-foreground">Verified Student</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <MapPin className="h-5 w-5 text-muted-foreground" />
                    <span className="text-sm">{item.seller.university}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <Calendar className="h-5 w-5 text-muted-foreground" />
                    <span className="text-sm">Listed on {formattedDate}</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <div className="flex flex-col gap-3 sm:flex-row">
              <Button size="lg" className="flex-1">
                <MessageCircle className="mr-2 h-4 w-4" />
                Contact Seller
              </Button>
              <Button size="lg" variant="outline" onClick={() => navigate("/report")}>
                <Flag className="mr-2 h-4 w-4" />
                Report
              </Button>
            </div>

            <Card className="bg-primary/5 border-primary/20">
              <CardContent className="p-4">
                <p className="text-sm text-muted-foreground leading-relaxed">
                  <strong className="text-foreground">Safety Tip:</strong> Meet in a public place on campus and inspect
                  the item before making payment. Never share sensitive information.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
export default ItemDetailPage;
