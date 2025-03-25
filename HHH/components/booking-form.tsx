"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { CalendarIcon, Users, MapPin } from "lucide-react"
import { useToast } from "@/hooks/use-toast"

// Einfache Datumsformatierungsfunktion ohne externe Bibliothek
function formatDate(date: Date | undefined): string {
  if (!date) return ""

  // Deutsche Monatsnamen
  const monthNames = [
    "Januar",
    "Februar",
    "März",
    "April",
    "Mai",
    "Juni",
    "Juli",
    "August",
    "September",
    "Oktober",
    "November",
    "Dezember",
  ]

  const day = date.getDate()
  const month = monthNames[date.getMonth()]
  const year = date.getFullYear()

  return `${day}. ${month} ${year}`
}

// Beispiel-Hotels
const hotels = [
  { id: "berlin", name: "Harmony Heaven Berlin", location: "Berlin" },
  { id: "munich", name: "Harmony Heaven München", location: "München" },
  { id: "hamburg", name: "Harmony Heaven Hamburg", location: "Hamburg" },
  { id: "frankfurt", name: "Harmony Heaven Frankfurt", location: "Frankfurt" },
]

export function BookingForm() {
  const [selectedHotel, setSelectedHotel] = useState<string>("")
  const [checkIn, setCheckIn] = useState<Date>()
  const [checkOut, setCheckOut] = useState<Date>()
  const [adults, setAdults] = useState(2)
  const [children, setChildren] = useState(0)
  const [rooms, setRooms] = useState(1)
  const [isLoading, setIsLoading] = useState(false)
  const { toast } = useToast()

  const handleSubmit = async () => {
    if (!selectedHotel) {
      toast({
        title: "Fehlende Daten",
        description: "Bitte wählen Sie ein Hotel aus",
        variant: "destructive",
      })
      return
    }

    if (!checkIn || !checkOut) {
      toast({
        title: "Fehlende Daten",
        description: "Bitte wählen Sie Check-in und Check-out Daten",
        variant: "destructive",
      })
      return
    }

    setIsLoading(true)

    try {
      // API-Anfrage an den Python-Backend-Server
      const response = await fetch("http://localhost:8000/api/bookings/check", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`, // Falls der Nutzer angemeldet ist
        },
        body: JSON.stringify({
          hotel_id: selectedHotel,
          check_in: checkIn.toISOString().split("T")[0],
          check_out: checkOut.toISOString().split("T")[0],
          adults,
          children,
          rooms,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Verfügbarkeitsprüfung fehlgeschlagen")
      }

      // Erfolgreiche Verfügbarkeitsprüfung
      toast({
        title: "Verfügbarkeit bestätigt",
        description: `Wir haben ${data.available_rooms} verfügbare Zimmer für Ihren Aufenthalt gefunden.`,
      })

      // Hier könnten Sie zur Buchungsseite weiterleiten
      // router.push('/booking/details')
    } catch (error) {
      console.error("Booking check error:", error)
      toast({
        title: "Fehler bei der Verfügbarkeitsprüfung",
        description: error instanceof Error ? error.message : "Bitte versuchen Sie es später erneut",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="rounded-xl border bg-card text-card-foreground shadow-lg border-primary/20">
      <div className="p-6">
        <h3 className="text-2xl font-semibold leading-none tracking-tight">Verfügbarkeit prüfen</h3>
        <p className="text-sm text-muted-foreground mt-2">Finden Sie die perfekte Unterkunft für Ihren Aufenthalt</p>
      </div>
      <div className="p-6 pt-0">
        <div className="grid gap-4 md:grid-cols-5">
          <div className="space-y-2">
            <label htmlFor="hotel" className="text-sm font-medium">
              Hotel & Ort
            </label>
            <Select value={selectedHotel} onValueChange={setSelectedHotel}>
              <SelectTrigger id="hotel" className="w-full">
                <SelectValue placeholder="Hotel wählen">
                  {selectedHotel ? (
                    <div className="flex items-center">
                      <MapPin className="mr-2 h-4 w-4 text-primary" />
                      <span>{hotels.find((h) => h.id === selectedHotel)?.location || "Hotel wählen"}</span>
                    </div>
                  ) : (
                    <span>Hotel wählen</span>
                  )}
                </SelectValue>
              </SelectTrigger>
              <SelectContent>
                {hotels.map((hotel) => (
                  <SelectItem key={hotel.id} value={hotel.id}>
                    <div className="flex flex-col">
                      <span>{hotel.name}</span>
                      <span className="text-xs text-muted-foreground">{hotel.location}</span>
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-2">
            <label htmlFor="check-in" className="text-sm font-medium">
              Check-in
            </label>
            <Popover>
              <PopoverTrigger asChild>
                <Button variant="outline" className="w-full justify-start text-left font-normal" id="check-in">
                  <CalendarIcon className="mr-2 h-4 w-4" />
                  {checkIn ? formatDate(checkIn) : <span>Datum wählen</span>}
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-auto p-0" align="start">
                <Calendar mode="single" selected={checkIn} onSelect={setCheckIn} initialFocus />
              </PopoverContent>
            </Popover>
          </div>
          <div className="space-y-2">
            <label htmlFor="check-out" className="text-sm font-medium">
              Check-out
            </label>
            <Popover>
              <PopoverTrigger asChild>
                <Button variant="outline" className="w-full justify-start text-left font-normal" id="check-out">
                  <CalendarIcon className="mr-2 h-4 w-4" />
                  {checkOut ? formatDate(checkOut) : <span>Datum wählen</span>}
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-auto p-0" align="start">
                <Calendar
                  mode="single"
                  selected={checkOut}
                  onSelect={setCheckOut}
                  initialFocus
                  disabled={(date) => (checkIn ? date < checkIn : false) || date < new Date()}
                />
              </PopoverContent>
            </Popover>
          </div>
          <div className="space-y-2">
            <label htmlFor="guests" className="text-sm font-medium">
              Gäste
            </label>
            <Popover>
              <PopoverTrigger asChild>
                <Button variant="outline" className="w-full justify-start text-left font-normal" id="guests">
                  <Users className="mr-2 h-4 w-4" />
                  <span>
                    {adults + children} Gäste, {rooms} Zimmer
                  </span>
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-80" align="start">
                <div className="grid gap-4">
                  <div className="flex items-center justify-between">
                    <div className="text-sm">Erwachsene</div>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="outline"
                        size="icon"
                        className="h-8 w-8 rounded-full"
                        onClick={() => setAdults(Math.max(1, adults - 1))}
                        disabled={adults <= 1}
                      >
                        <span>-</span>
                      </Button>
                      <span className="w-8 text-center">{adults}</span>
                      <Button
                        variant="outline"
                        size="icon"
                        className="h-8 w-8 rounded-full"
                        onClick={() => setAdults(adults + 1)}
                      >
                        <span>+</span>
                      </Button>
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="text-sm">Kinder</div>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="outline"
                        size="icon"
                        className="h-8 w-8 rounded-full"
                        onClick={() => setChildren(Math.max(0, children - 1))}
                        disabled={children <= 0}
                      >
                        <span>-</span>
                      </Button>
                      <span className="w-8 text-center">{children}</span>
                      <Button
                        variant="outline"
                        size="icon"
                        className="h-8 w-8 rounded-full"
                        onClick={() => setChildren(children + 1)}
                      >
                        <span>+</span>
                      </Button>
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="text-sm">Zimmer</div>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="outline"
                        size="icon"
                        className="h-8 w-8 rounded-full"
                        onClick={() => setRooms(Math.max(1, rooms - 1))}
                        disabled={rooms <= 1}
                      >
                        <span>-</span>
                      </Button>
                      <span className="w-8 text-center">{rooms}</span>
                      <Button
                        variant="outline"
                        size="icon"
                        className="h-8 w-8 rounded-full"
                        onClick={() => setRooms(rooms + 1)}
                      >
                        <span>+</span>
                      </Button>
                    </div>
                  </div>
                </div>
              </PopoverContent>
            </Popover>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">&nbsp;</label>
            <Button
              className="w-full bg-primary text-primary-foreground hover:bg-primary/90"
              onClick={handleSubmit}
              disabled={isLoading}
            >
              {isLoading ? "Wird geprüft..." : "Verfügbarkeit prüfen"}
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}

