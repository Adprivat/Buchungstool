import type { ReactNode } from "react"

interface AmenityCardProps {
  icon: ReactNode
  title: string
  description: string
}

export function AmenityCard({ icon, title, description }: AmenityCardProps) {
  return (
    <div className="rounded-xl border bg-card p-6 shadow-lg border-primary/20 transition-all hover:shadow-xl hover:border-primary/40">
      <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-primary/10">{icon}</div>
      <h3 className="font-cinzel text-xl font-bold uppercase">{title}</h3>
      <p className="mt-2 text-muted-foreground">{description}</p>
    </div>
  )
}

