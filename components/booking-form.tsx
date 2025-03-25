"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { CalendarIcon, Users, MapPin, Check, AlertCircle } from "lucide-react"
import { useToast } from "@/hooks/use-toast"
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"

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

interface Hotel {
  id: string
  name: string
  location: string
}

interface Room {
  id: number
  name: string
  description: string
  price_per_night: number
  capacity: number
  room_type: string
  image_url: string
}

interface AvailabilityResponse {
  available_rooms: number
  price_per_night: number
}

export function BookingForm() {
  const [hotels, setHotels] = useState<Hotel[]>([])
  const [selectedHotel, setSelectedHotel] = useState<string>("")
  const [checkIn, setCheckIn] = useState<Date>()
  const [checkOut, setCheckOut] = useState<Date>()
  const [adults, setAdults] = useState(2)
  const [children, setChildren] = useState(0)
  const [rooms, setRooms] = useState(1)
  const [isLoading, setIsLoading] = useState(false)
  const [availability, setAvailability] = useState<AvailabilityResponse | null>(null)
  const [showAvailabilityModal, setShowAvailabilityModal] = useState(false)
  const [showErrorModal, setShowErrorModal] = useState(false)
  const [errorMessage, setErrorMessage] = useState("")
  const { toast } = useToast()

  // Hotels aus der API laden
  useEffect(() => {
    async function fetchHotels() {
      try {
        // API-Urls definieren, die wir versuchen
        const apiUrls = [
          "http://localhost:8000/api/hotels",
          "http://127.0.0.1:8000/api/hotels"
        ];
        
        let response = null;
        let error = null;
        
        // Jeden API-Endpunkt versuchen
        for (const url of apiUrls) {
          try {
            console.log(`Trying to fetch hotels from: ${url}`);
            response = await fetch(url);
            
            if (response.ok) {
              console.log(`Successfully connected to: ${url}`);
              const data = await response.json();
              setHotels(data);
              return; // Bei erfolgreicher Verbindung abbrechen
            }
          } catch (e) {
            console.error(`Error connecting to ${url}:`, e);
            error = e;
          }
        }
        
        // Wenn keine Verbindung hergestellt werden konnte
        throw error || new Error("Verbindung zum Server nicht möglich");
      } catch (error) {
        console.error("Fehler beim Laden der Hotels:", error)
        toast({
          title: "Fehler",
          description: "Die Hotels konnten nicht geladen werden. Bitte stellen Sie sicher, dass der Server läuft.",
          variant: "destructive",
        })
      }
    }

    fetchHotels()
  }, [toast])

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
      // API-Urls definieren, die wir versuchen
      const apiUrls = [
        "http://localhost:8000/api/bookings/check",
        "http://127.0.0.1:8000/api/bookings/check"
      ];
      
      let response = null;
      let error = null;
      let data = null;
      
      // Jeden API-Endpunkt versuchen
      for (const url of apiUrls) {
        try {
          console.log(`Trying to connect to: ${url}`);
          response = await fetch(url, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              hotel_id: selectedHotel,
              check_in: checkIn.toISOString().split("T")[0],
              check_out: checkOut.toISOString().split("T")[0],
              adults,
              children,
              rooms,
            }),
          });
          
          if (response.ok) {
            console.log(`Successfully connected to: ${url}`);
            data = await response.json();
            break; // Bei erfolgreicher Verbindung abbrechen
          }
        } catch (e) {
          console.error(`Error connecting to ${url}:`, e);
          error = e;
        }
      }
      
      if (!response || !response.ok || !data) {
        throw error || new Error("Verbindung zum Server nicht möglich");
      }

      // Verfügbarkeitsinformationen speichern und Modal anzeigen
      setAvailability(data)
      setShowAvailabilityModal(true)
    } catch (error) {
      console.error("Booking check error:", error)
      setErrorMessage(
        error instanceof Error 
          ? error.message 
          : "Verbindung zum Server fehlgeschlagen. Bitte stellen Sie sicher, dass der Server läuft."
      )
      setShowErrorModal(true)
    } finally {
      setIsLoading(false)
    }
  }

  const handleBooking = async () => {
    if (!availability || !selectedHotel || !checkIn || !checkOut) return

    try {
      setIsLoading(true)

      // API-Urls definieren, die wir versuchen
      const apiUrls = [
        "http://localhost:8000/api/bookings",
        "http://127.0.0.1:8000/api/bookings"
      ];
      
      let response = null;
      let error = null;
      
      // Jeden API-Endpunkt versuchen
      for (const url of apiUrls) {
        try {
          console.log(`Trying to connect to: ${url}`);
          response = await fetch(url, {
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
              // In einer vollständigen Implementierung würde hier eine room_id übergeben werden
            }),
          });
          
          if (response.ok) {
            console.log(`Successfully connected to: ${url}`);
            break; // Bei erfolgreicher Verbindung abbrechen
          }
        } catch (e) {
          console.error(`Error connecting to ${url}:`, e);
          error = e;
        }
      }

      if (!response || !response.ok) {
        const errorData = response ? await response.json() : null;
        throw new Error(errorData?.detail || "Verbindung zum Server nicht möglich");
      }

      toast({
        title: "Buchung erfolgreich",
        description: "Ihre Buchung wurde erfolgreich abgeschlossen.",
      })
      
      // Formular zurücksetzen
      setSelectedHotel("")
      setCheckIn(undefined)
      setCheckOut(undefined)
      setAdults(2)
      setChildren(0)
      setRooms(1)
    } catch (error) {
      console.error("Booking error:", error)
      toast({
        title: "Buchung fehlgeschlagen",
        description: error instanceof Error 
          ? error.message 
          : "Verbindung zum Server fehlgeschlagen. Bitte stellen Sie sicher, dass der Server läuft.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
      setShowAvailabilityModal(false)
    }
  }

  // Berechnen der Anzahl der Übernachtungen
  const calculateNights = () => {
    if (!checkIn || !checkOut) return 0
    return Math.round((checkOut.getTime() - checkIn.getTime()) / (1000 * 60 * 60 * 24))
  }

  // Berechnen des Gesamtpreises
  const calculateTotalPrice = () => {
    if (!availability) return 0
    return availability.price_per_night * calculateNights() * rooms
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
                <Calendar 
                  mode="single" 
                  selected={checkIn} 
                  onSelect={setCheckIn} 
                  initialFocus 
                  disabled={(date) => date < new Date(new Date().setHours(0, 0, 0, 0))} 
                />
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
                  disabled={(date) => (checkIn ? date <= checkIn : false) || date < new Date(new Date().setHours(0, 0, 0, 0))}
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

      {/* Verfügbarkeits-Modal */}
      <Dialog open={showAvailabilityModal} onOpenChange={setShowAvailabilityModal}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>Verfügbarkeit bestätigt</DialogTitle>
            <DialogDescription>
              Wir haben {availability?.available_rooms} verfügbare Zimmer für Ihren Aufenthalt gefunden.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <Alert>
              <Check className="h-4 w-4" />
              <AlertTitle>Verfügbare Zimmer</AlertTitle>
              <AlertDescription>
                <div className="mt-2 space-y-2">
                  <div className="flex justify-between">
                    <span>Hotel:</span>
                    <span className="font-semibold">{hotels.find((h) => h.id === selectedHotel)?.name}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Check-in:</span>
                    <span className="font-semibold">{formatDate(checkIn)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Check-out:</span>
                    <span className="font-semibold">{formatDate(checkOut)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Anzahl der Nächte:</span>
                    <span className="font-semibold">{calculateNights()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Preis pro Nacht:</span>
                    <span className="font-semibold">{availability?.price_per_night.toFixed(2)} €</span>
                  </div>
                  <div className="flex justify-between border-t pt-2 mt-2">
                    <span>Gesamtpreis:</span>
                    <span className="font-semibold">{calculateTotalPrice().toFixed(2)} €</span>
                  </div>
                </div>
              </AlertDescription>
            </Alert>
          </div>
          <DialogFooter className="sm:justify-between">
            <Button variant="outline" onClick={() => setShowAvailabilityModal(false)}>
              Abbrechen
            </Button>
            <Button type="button" onClick={handleBooking} disabled={isLoading}>
              {isLoading ? "Wird gebucht..." : "Jetzt buchen"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Fehler-Modal */}
      <Dialog open={showErrorModal} onOpenChange={setShowErrorModal}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>Fehler bei der Verfügbarkeitsprüfung</DialogTitle>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertTitle>Fehler</AlertTitle>
              <AlertDescription>
                {errorMessage}
              </AlertDescription>
            </Alert>
          </div>
          <DialogFooter>
            <Button type="button" onClick={() => setShowErrorModal(false)}>
              Schließen
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}

