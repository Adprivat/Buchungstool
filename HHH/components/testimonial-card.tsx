interface TestimonialCardProps {
  quote: string
  author: string
  role: string
}

export function TestimonialCard({ quote, author, role }: TestimonialCardProps) {
  return (
    <div className="rounded-xl border bg-card p-6 shadow-lg border-primary/20">
      <div className="mb-4 text-4xl text-primary">"</div>
      <p className="text-muted-foreground">{quote}</p>
      <div className="mt-6">
        <p className="font-cinzel font-semibold">{author}</p>
        <p className="text-sm text-muted-foreground">{role}</p>
      </div>
    </div>
  )
}

