import { Link } from "react-router-dom"
import { Button } from "../components/ui/button"
import { Card } from "../components/ui/card"
import { Laptop, BookOpen, Bike, Home, ArrowRight, Shield, Users, Zap } from "lucide-react"

export function HomePage() {
  const categories = [
    { name: "Electronics", icon: Laptop, color: "text-blue-600" },
    { name: "Books", icon: BookOpen, color: "text-green-600" },
    { name: "Cycles", icon: Bike, color: "text-orange-600" },
    { name: "Hostel Items", icon: Home, color: "text-purple-600" },
  ]

  const features = [
    {
      icon: Shield,
      title: "University Verified",
      description: "Only verified university students can buy and sell",
    },
    {
      icon: Users,
      title: "Student Community",
      description: "Connect with fellow students in your university",
    },
    {
      icon: Zap,
      title: "Quick & Easy",
      description: "List items in minutes, sell faster than ever",
    },
  ]

  return (
    <div className="bg-background">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-primary/5 to-background">
        <div className="mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-5xl font-bold tracking-tight text-foreground sm:text-6xl lg:text-7xl text-balance">
              Your University <span className="text-primary">Marketplace</span>
            </h1>
            <p className="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground leading-relaxed">
              Buy and sell electronics, books, cycles, and hostel items within your university community. Safe, simple,
              and trusted by students.
            </p>
            <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
              <Link to="/items">
                <Button size="lg" className="gap-2">
                  Browse Items
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
              <Link to="/register">
                <Button size="lg" variant="outline">
                  Start Selling
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section className="py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-center text-3xl font-bold">Shop by Category</h2>
          <div className="mt-12 grid grid-cols-2 gap-6 md:grid-cols-4">
            {categories.map((category) => (
              <Link key={category.name} to="/items">
                <Card className="group cursor-pointer border-2 p-8 transition-all hover:border-primary hover:shadow-lg">
                  <div className="flex flex-col items-center gap-4">
                    <category.icon
                      className={`h-12 w-12 ${category.color} transition-transform group-hover:scale-110`}
                    />
                    <h3 className="text-center font-semibold">{category.name}</h3>
                  </div>
                </Card>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="bg-muted/50 py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-center text-3xl font-bold">Why Choose Clixs?</h2>
          <div className="mt-12 grid gap-8 md:grid-cols-3">
            {features.map((feature) => (
              <Card key={feature.title} className="p-8">
                <div className="flex flex-col items-center text-center">
                  <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
                    <feature.icon className="h-8 w-8 text-primary" />
                  </div>
                  <h3 className="mt-6 text-xl font-semibold">{feature.title}</h3>
                  <p className="mt-3 text-sm text-muted-foreground leading-relaxed">{feature.description}</p>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="mx-auto max-w-4xl px-4 text-center sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-balance">Ready to start trading?</h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Join thousands of students already using Clixs to buy and sell within their university community.
          </p>
          <Link to="/register">
            <Button size="lg" className="mt-8">
              Create Your Account
            </Button>
          </Link>
        </div>
      </section>
    </div>
  )
}
export default HomePage;