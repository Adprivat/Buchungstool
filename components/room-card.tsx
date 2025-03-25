import Image from "next/image"
import { Button } from "@/components/ui/button"
import { Bed, Users, Maximize2, Coffee } from "lucide-react"

interface RoomCardProps {
  title: string
  description: string
  price: number
  image: string
}

export function RoomCard({ title, description, price, image }: RoomCardProps) {
  return (
    <div className="group overflow-hidden rounded-xl border bg-card text-card-foreground shadow-lg border-primary/20 transition-all hover:shadow-xl hover:border-primary/40">
      <div className="relative h-64 overflow-hidden">
        <Image
          src={image || "/placeholder.svg"}
          alt={title}
          fill
          className="object-cover transition-transform duration-300 group-hover:scale-105"
        />
      </div>
      <div className="p-6">
        <h3 className="font-cinzel text-xl font-bold uppercase">{title}</h3>
        <p className="mt-2 text-muted-foreground">{description}</p>
        <div className="mt-4 flex flex-wrap gap-4">
          <div className="flex items-center gap-1 text-sm">
            <Bed className="h-4 w-4 text-primary" />
            <span>Kingsize-Bett</span>
          </div>
          <div className="flex items-center gap-1 text-sm">
            <Users className="h-4 w-4 text-primary" />
            <span>2 Personen</span>
          </div>
          <div className="flex items-center gap-1 text-sm">
            <Maximize2 className="h-4 w-4 text-primary" />
            <span>42 m²</span>
          </div>
          <div className="flex items-center gap-1 text-sm">
            <Coffee className="h-4 w-4 text-primary" />
            <span>Frühstück</span>
          </div>
        </div>
        <div className="mt-6 flex items-center justify-between">
          <div>
            <span className="text-2xl font-bold">{price} €</span>
            <span className="text-sm text-muted-foreground"> / Nacht</span>
          </div>
          <Button className="bg-primary text-primary-foreground hover:bg-primary/90 font-cinzel">Buchen</Button>
        </div>
      </div>
    </div>
  )
}

