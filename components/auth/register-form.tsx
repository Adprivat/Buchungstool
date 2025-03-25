"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { useToast } from "@/hooks/use-toast"

interface RegisterFormProps {
  onSuccess: () => void
}

export function RegisterForm({ onSuccess }: RegisterFormProps) {
  const [isLoading, setIsLoading] = useState(false)
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    confirmPassword: "",
  })
  const [acceptTerms, setAcceptTerms] = useState(false)
  const [passwordError, setPasswordError] = useState("")
  const { toast } = useToast()

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))

    // Überprüfe Passwörter bei Änderung
    if ((name === "password" || name === "confirmPassword") && formData.confirmPassword && formData.password) {
      if (name === "password" && value !== formData.confirmPassword) {
        setPasswordError("Passwörter stimmen nicht überein")
      } else if (name === "confirmPassword" && value !== formData.password) {
        setPasswordError("Passwörter stimmen nicht überein")
      } else {
        setPasswordError("")
      }
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (formData.password !== formData.confirmPassword) {
      setPasswordError("Passwörter stimmen nicht überein")
      return
    }

    if (!acceptTerms) {
      return
    }

    setIsLoading(true)

    try {
      // API-Anfrage an den Python-Backend-Server
      const response = await fetch("http://localhost:8000/api/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          first_name: formData.firstName,
          last_name: formData.lastName,
          email: formData.email,
          password: formData.password,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Registrierung fehlgeschlagen")
      }

      // Erfolgreiche Registrierung
      toast({
        title: "Registrierung erfolgreich",
        description: "Ihr Konto wurde erfolgreich erstellt. Sie können sich jetzt anmelden.",
      })

      onSuccess()
    } catch (error) {
      console.error("Registration error:", error)
      toast({
        title: "Fehler bei der Registrierung",
        description: error instanceof Error ? error.message : "Bitte überprüfen Sie Ihre Eingaben",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 py-2">
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="firstName">Vorname</Label>
          <Input
            id="firstName"
            name="firstName"
            placeholder="Max"
            value={formData.firstName}
            onChange={handleChange}
            required
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="lastName">Nachname</Label>
          <Input
            id="lastName"
            name="lastName"
            placeholder="Mustermann"
            value={formData.lastName}
            onChange={handleChange}
            required
          />
        </div>
      </div>
      <div className="space-y-2">
        <Label htmlFor="email">E-Mail</Label>
        <Input
          id="email"
          name="email"
          type="email"
          placeholder="ihre.email@beispiel.de"
          value={formData.email}
          onChange={handleChange}
          required
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="password">Passwort</Label>
        <Input
          id="password"
          name="password"
          type="password"
          placeholder="••••••••"
          value={formData.password}
          onChange={handleChange}
          required
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="confirmPassword">Passwort bestätigen</Label>
        <Input
          id="confirmPassword"
          name="confirmPassword"
          type="password"
          placeholder="••••••••"
          value={formData.confirmPassword}
          onChange={handleChange}
          required
        />
        {passwordError && <p className="text-destructive text-sm">{passwordError}</p>}
      </div>
      <div className="flex items-center space-x-2">
        <Checkbox
          id="terms"
          checked={acceptTerms}
          onCheckedChange={(checked) => setAcceptTerms(checked as boolean)}
          required
        />
        <Label htmlFor="terms" className="text-sm font-normal">
          Ich akzeptiere die{" "}
          <Button variant="link" className="p-0 h-auto font-normal">
            AGB
          </Button>{" "}
          und{" "}
          <Button variant="link" className="p-0 h-auto font-normal">
            Datenschutzbestimmungen
          </Button>
        </Label>
      </div>
      <Button
        type="submit"
        className="w-full font-cinzel bg-primary text-primary-foreground hover:bg-primary/90"
        disabled={isLoading || !acceptTerms || !!passwordError}
      >
        {isLoading ? "Wird registriert..." : "Registrieren"}
      </Button>
    </form>
  )
}

