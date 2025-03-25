import Image from "next/image"
import { Button } from "@/components/ui/button"
import { MapPin, Star, Coffee, Wifi } from "lucide-react"

interface HotelCardProps {
  title: string
  description: string
  price: number
  image: string
}

export function HotelCard({ title, description, price, image }: HotelCardProps) {
  return (
    <div className="group overflow-hidden rounded-xl border bg-card text-card-foreground shadow-lg border-primary/20 transition-all hover:shadow-xl hover:border-primary/40">
      <div className="relative h-48 overflow-hidden">
        <Image
          src={image || "/placeholder.svg"}
          alt={title}
          fill
          className="object-cover transition-transform duration-300 group-hover:scale-105"
        />
        <div className="absolute top-2 right-2 bg-primary/90 text-primary-foreground px-2 py-1 rounded-md text-sm font-medium flex items-center">
          <Star className="h-3 w-3 mr-1 fill-current" /> 5.0
        </div>
      </div>
      <div className="p-5">
        <h3 className="font-cinzel text-xl font-bold">{title}</h3>
        <div className="flex items-center mt-1 text-sm text-muted-foreground">
          <MapPin className="h-3.5 w-3.5 mr-1 text-primary" />
          <span>{description}</span>
        </div>
        <div className="mt-3 flex flex-wrap gap-3">
          <div className="flex items-center gap-1 text-xs bg-secondary/30 px-2 py-1 rounded-full">
            <Coffee className="h-3 w-3 text-primary" />
            <span>Frühstück</span>
          </div>
          <div className="flex items-center gap-1 text-xs bg-secondary/30 px-2 py-1 rounded-full">
            <Wifi className="h-3 w-3 text-primary" />
            <span>Gratis WLAN</span>
          </div>
        </div>
        <div className="mt-4 flex items-center justify-between">
          <div>
            <span className="text-lg font-bold">ab {price} €</span>
            <span className="text-xs text-muted-foreground"> / Nacht</span>
          </div>
          <Button className="bg-primary text-primary-foreground hover:bg-primary/90 font-cinzel text-sm">
            Details
          </Button>
        </div>
      </div>
    </div>
  )
}

