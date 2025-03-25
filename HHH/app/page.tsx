import Image from "next/image"
import Link from "next/link"
import { BookingForm } from "@/components/booking-form"
import { RoomCard } from "@/components/room-card"
import { AmenityCard } from "@/components/amenity-card"
import { TestimonialCard } from "@/components/testimonial-card"
import { Button } from "@/components/ui/button"
import { Header } from "@/components/header"
import {
  Bed,
  UtensilsCrossed,
  Waves,
  Dumbbell,
  Car,
  Wifi,
  MapPin,
  Phone,
  Mail,
  Instagram,
  Facebook,
  Twitter,
} from "lucide-react"

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      <main className="flex-1">
        <section className="relative hero-section">
          <div className="absolute inset-0 bg-gradient-to-r from-background/90 via-background/70 to-background/40 z-10" />
          <div className="relative h-[80vh]">
            <Image
              src="/hero-luxury.jpg"
              alt="Luxuriöses Harmony Heaven Hotel"
              fill
              className="object-cover hero-image"
              priority
            />
            <div className="container relative z-20 flex h-full flex-col items-start justify-center gap-4">
              <div className="max-w-xl space-y-4">
                <h1 className="font-cinzel text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl uppercase">
                  Luxus neu definiert
                </h1>
                <p className="text-lg text-muted-foreground md:text-xl">
                  Erleben Sie unvergleichlichen Komfort und Eleganz in unseren exklusiven Hotels.
                </p>
                <div className="flex flex-col sm:flex-row gap-3">
                  <Button size="lg" className="bg-primary text-primary-foreground hover:bg-primary/90 font-cinzel">
                    Jetzt buchen
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section id="booking" className="bg-muted py-12">
          <div className="container">
            <BookingForm />
          </div>
        </section>

        <section id="about" className="py-20">
          <div className="container">
            <div className="grid gap-12 lg:grid-cols-2 lg:gap-8 items-center">
              <div className="space-y-6">
                <div className="inline-block rounded-lg bg-muted px-3 py-1 text-sm font-cinzel uppercase">Über uns</div>
                <h2 className="font-cinzel text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl uppercase">
                  Willkommen bei Harmony Heaven Hotels
                </h2>
                <p className="text-muted-foreground text-lg">
                  Seit über zwei Jahrzehnten definieren wir Luxushotellerie neu. Unsere Hotels verbinden zeitlose
                  Eleganz mit modernem Komfort und bieten Ihnen ein unvergleichliches Erlebnis.
                </p>
                <p className="text-muted-foreground text-lg">
                  Jedes unserer Hotels ist einzigartig gestaltet, um die lokale Kultur zu reflektieren und gleichzeitig
                  den höchsten Standards an Luxus und Service gerecht zu werden.
                </p>
                <div className="flex flex-col sm:flex-row gap-3">
                  <Button className="bg-primary text-primary-foreground hover:bg-primary/90 font-cinzel">
                    Mehr erfahren
                  </Button>
                </div>
              </div>
              <div className="relative aspect-video overflow-hidden rounded-xl shadow-2xl border border-primary/20">
                <Image src="/about-luxury.jpg" alt="Elegante Hotellobby" fill className="object-cover" />
              </div>
            </div>
          </div>
        </section>

        <section id="locations" className="py-20 bg-muted">
          <div className="container">
            <div className="text-center space-y-4 mb-12">
              <div className="inline-block rounded-lg bg-background px-3 py-1 text-sm font-cinzel uppercase">
                Unterkünfte
              </div>
              <h2 className="font-cinzel text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl uppercase">
                Unsere Hotels
              </h2>
              <p className="mx-auto max-w-[700px] text-muted-foreground text-lg">
                Entdecken Sie unsere exklusiven Hotels in den schönsten Städten Deutschlands und genießen Sie
                erstklassigen Service und Komfort.
              </p>
            </div>
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
              <RoomCard
                title="Harmony Heaven Berlin"
                description="Im Herzen der Hauptstadt, nahe dem Brandenburger Tor"
                price={199}
                image="/berlin.jpeg"
              />
              <RoomCard
                title="Harmony Heaven Hamburg"
                description="Direkt an der Alster mit Blick auf den Hafen"
                price={219}
                image="/hamburg.jpeg"
              />
              <RoomCard
                title="Harmony Heaven München"
                description="Luxuriöse Unterkunft im Zentrum der bayerischen Metropole"
                price={229}
                image="/muenchen.jpeg"
              />
              <RoomCard
                title="Harmony Heaven Frankfurt"
                description="Modernes Design im Bankenviertel mit Skyline-Blick"
                price={209}
                image="/frankfurt.jpeg"
              />
            </div>
          </div>
        </section>

        <section id="amenities" className="py-20">
          <div className="container">
            <div className="text-center space-y-4 mb-12">
              <div className="inline-block rounded-lg bg-muted px-3 py-1 text-sm font-cinzel uppercase">
                Annehmlichkeiten
              </div>
              <h2 className="font-cinzel text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl uppercase">
                Erstklassiger Service
              </h2>
              <p className="mx-auto max-w-[700px] text-muted-foreground text-lg">
                Genießen Sie unsere erstklassigen Annehmlichkeiten, die Ihren Aufenthalt unvergesslich machen.
              </p>
            </div>
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              <AmenityCard
                icon={<UtensilsCrossed className="h-8 w-8 text-primary" />}
                title="Gourmet Restaurant"
                description="Genießen Sie exquisite Speisen von preisgekrönten Köchen"
              />
              <AmenityCard
                icon={<Waves className="h-8 w-8 text-primary" />}
                title="Infinity Pool"
                description="Entspannen Sie in unserem beheizten Pool mit atemberaubendem Ausblick"
              />
              <AmenityCard
                icon={<Dumbbell className="h-8 w-8 text-primary" />}
                title="Fitnesscenter"
                description="Modernste Geräte und persönliche Trainer rund um die Uhr"
              />
              <AmenityCard
                icon={<Car className="h-8 w-8 text-primary" />}
                title="Valet Parking"
                description="Kostenloser Parkservice für alle Hotelgäste"
              />
              <AmenityCard
                icon={<Wifi className="h-8 w-8 text-primary" />}
                title="Highspeed WLAN"
                description="Kostenloses Highspeed-Internet im gesamten Hotel"
              />
              <AmenityCard
                icon={<Bed className="h-8 w-8 text-primary" />}
                title="Luxuriöse Bettwäsche"
                description="Handgefertigte Bettwäsche für erholsamen Schlaf"
              />
            </div>
          </div>
        </section>

        <section className="py-20 bg-muted">
          <div className="container">
            <div className="text-center space-y-4 mb-12">
              <div className="inline-block rounded-lg bg-background px-3 py-1 text-sm font-cinzel uppercase">
                Erfahrungen
              </div>
              <h2 className="font-cinzel text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl uppercase">
                Was unsere Gäste sagen
              </h2>
              <p className="mx-auto max-w-[700px] text-muted-foreground text-lg">
                Entdecken Sie, warum unsere Gäste immer wieder zu uns zurückkehren.
              </p>
            </div>
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              <TestimonialCard
                quote="Ein unvergleichliches Erlebnis. Der Service war erstklassig und das Zimmer atemberaubend."
                author="Maria Schmidt"
                role="Geschäftsreisende"
              />
              <TestimonialCard
                quote="Die Aufmerksamkeit zum Detail ist bemerkenswert. Definitiv das beste Hotel, in dem ich je übernachtet habe."
                author="Thomas Müller"
                role="Urlauber"
              />
              <TestimonialCard
                quote="Von der Ankunft bis zur Abreise war alles perfekt. Wir kommen auf jeden Fall wieder!"
                author="Lisa und Mark Weber"
                role="Hochzeitsreisende"
              />
            </div>
          </div>
        </section>

        <section className="relative py-20">
          <div className="absolute inset-0 bg-gradient-to-r from-background/90 to-background/70" />
          <div className="relative h-[60vh]">
            <Image src="/hhh.jpeg" alt="Luxuriöse Hotelansicht" fill className="object-cover" />
            <div className="container relative flex h-full flex-col items-center justify-center gap-4 text-center">
              <div className="max-w-2xl space-y-4">
                <h2 className="font-cinzel text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl uppercase">
                  Buchen Sie Ihren Traumurlaub
                </h2>
                <p className="text-lg text-muted-foreground md:text-xl">
                  Sichern Sie sich jetzt Ihren Aufenthalt in einem unserer exklusiven Hotels und erleben Sie Luxus auf
                  höchstem Niveau.
                </p>
                <div className="flex flex-col sm:flex-row gap-3 justify-center">
                  <Button size="lg" className="bg-primary text-primary-foreground hover:bg-primary/90 font-cinzel">
                    Jetzt buchen
                  </Button>
                  <Button
                    size="lg"
                    variant="outline"
                    className="border-primary text-primary hover:bg-primary hover:text-primary-foreground font-cinzel"
                  >
                    Kontaktieren Sie uns
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section id="contact" className="py-20">
          <div className="container">
            <div className="grid gap-12 lg:grid-cols-2 lg:gap-8 items-start">
              <div className="space-y-6">
                <div className="inline-block rounded-lg bg-muted px-3 py-1 text-sm font-cinzel uppercase">Kontakt</div>
                <h2 className="font-cinzel text-3xl font-bold tracking-tighter sm:text-4xl uppercase">
                  Kontaktieren Sie uns
                </h2>
                <p className="text-muted-foreground text-lg">
                  Haben Sie Fragen oder möchten Sie eine Reservierung vornehmen? Unser Team steht Ihnen jederzeit zur
                  Verfügung.
                </p>
                <div className="space-y-4">
                  <div className="flex items-center gap-3">
                    <MapPin className="h-5 w-5 text-primary" />
                    <span>Luxusstraße 123, 10115 Berlin, Deutschland</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <Phone className="h-5 w-5 text-primary" />
                    <span>+49 30 1234567</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <Mail className="h-5 w-5 text-primary" />
                    <span>info@harmonyheaven.com</span>
                  </div>
                </div>
                <div className="flex gap-4">
                  <Button variant="outline" size="icon" className="rounded-full">
                    <Instagram className="h-5 w-5" />
                  </Button>
                  <Button variant="outline" size="icon" className="rounded-full">
                    <Facebook className="h-5 w-5" />
                  </Button>
                  <Button variant="outline" size="icon" className="rounded-full">
                    <Twitter className="h-5 w-5" />
                  </Button>
                </div>
              </div>
              <div className="space-y-6">
                <form className="space-y-4">
                  <div className="grid gap-4 sm:grid-cols-2">
                    <div className="space-y-2">
                      <label htmlFor="name" className="text-sm font-medium">
                        Name
                      </label>
                      <input
                        id="name"
                        className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                        placeholder="Ihr Name"
                      />
                    </div>
                    <div className="space-y-2">
                      <label htmlFor="email" className="text-sm font-medium">
                        E-Mail
                      </label>
                      <input
                        id="email"
                        type="email"
                        className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                        placeholder="Ihre E-Mail"
                      />
                    </div>
                  </div>
                  <div className="space-y-2">
                    <label htmlFor="subject" className="text-sm font-medium">
                      Betreff
                    </label>
                    <input
                      id="subject"
                      className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                      placeholder="Betreff Ihrer Nachricht"
                    />
                  </div>
                  <div className="space-y-2">
                    <label htmlFor="message" className="text-sm font-medium">
                      Nachricht
                    </label>
                    <textarea
                      id="message"
                      className="flex min-h-[120px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                      placeholder="Ihre Nachricht"
                    />
                  </div>
                  <Button className="w-full bg-primary text-primary-foreground hover:bg-primary/90 font-cinzel">
                    Nachricht senden
                  </Button>
                </form>
              </div>
            </div>
          </div>
        </section>
      </main>
      <footer className="bg-muted py-12 border-t border-primary/20">
        <div className="container">
          <div className="grid gap-8 sm:grid-cols-2 md:grid-cols-4">
            <div className="space-y-4">
              <div className="flex items-center gap-2">
                <Image
                  src="/logo-transparent.png"
                  alt="Harmony Heaven Hotels Logo"
                  width={40}
                  height={40}
                  className="h-8 w-auto"
                />
                <span className="font-cinzel text-lg font-semibold tracking-wider text-primary uppercase">
                  Harmony Heaven
                </span>
              </div>
              <p className="text-sm text-muted-foreground">
                Luxus neu definiert. Erleben Sie unvergleichlichen Komfort und Eleganz in unseren exklusiven Hotels.
              </p>
              <div className="flex gap-4">
                <Button variant="ghost" size="icon" className="h-8 w-8 rounded-full">
                  <Instagram className="h-4 w-4" />
                </Button>
                <Button variant="ghost" size="icon" className="h-8 w-8 rounded-full">
                  <Facebook className="h-4 w-4" />
                </Button>
                <Button variant="ghost" size="icon" className="h-8 w-8 rounded-full">
                  <Twitter className="h-4 w-4" />
                </Button>
              </div>
            </div>
            <div className="space-y-4">
              <h3 className="font-cinzel text-sm font-medium uppercase">Schnelllinks</h3>
              <ul className="space-y-2 text-sm">
                <li>
                  <Link href="#" className="text-muted-foreground hover:text-foreground transition-colors">
                    Home
                  </Link>
                </li>
                <li>
                  <Link href="#about" className="text-muted-foreground hover:text-foreground transition-colors">
                    Über uns
                  </Link>
                </li>
                <li>
                  <Link href="#locations" className="text-muted-foreground hover:text-foreground transition-colors">
                    Standorte
                  </Link>
                </li>
                <li>
                  <Link href="#amenities" className="text-muted-foreground hover:text-foreground transition-colors">
                    Annehmlichkeiten
                  </Link>
                </li>
                <li>
                  <Link href="#contact" className="text-muted-foreground hover:text-foreground transition-colors">
                    Kontakt
                  </Link>
                </li>
              </ul>
            </div>
            <div className="space-y-4">
              <h3 className="font-cinzel text-sm font-medium uppercase">Rechtliches</h3>
              <ul className="space-y-2 text-sm">
                <li>
                  <Link href="#" className="text-muted-foreground hover:text-foreground transition-colors">
                    AGB
                  </Link>
                </li>
                <li>
                  <Link href="#" className="text-muted-foreground hover:text-foreground transition-colors">
                    Datenschutz
                  </Link>
                </li>
                <li>
                  <Link href="#" className="text-muted-foreground hover:text-foreground transition-colors">
                    Impressum
                  </Link>
                </li>
                <li>
                  <Link href="#" className="text-muted-foreground hover:text-foreground transition-colors">
                    Cookie-Richtlinie
                  </Link>
                </li>
              </ul>
            </div>
            <div className="space-y-4">
              <h3 className="font-cinzel text-sm font-medium uppercase">Newsletter</h3>
              <p className="text-sm text-muted-foreground">Abonnieren Sie unseren Newsletter für exklusive Angebote.</p>
              <form className="flex gap-2">
                <input
                  type="email"
                  className="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder="Ihre E-Mail"
                />
                <Button type="submit" size="sm" className="h-9 font-cinzel">
                  Abonnieren
                </Button>
              </form>
            </div>
          </div>
          <div className="mt-12 border-t pt-6 text-center text-sm text-muted-foreground">
            <p>&copy; {new Date().getFullYear()} Harmony Heaven Hotels. Alle Rechte vorbehalten.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

