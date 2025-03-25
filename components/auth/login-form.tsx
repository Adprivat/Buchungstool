"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"
import { useToast } from "@/hooks/use-toast"

interface LoginFormProps {
  onSuccess: () => void
}

export function LoginForm({ onSuccess }: LoginFormProps) {
  const [isLoading, setIsLoading] = useState(false)
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const { toast } = useToast()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      // API-Anfrage an den Python-Backend-Server
      const response = await fetch("http://localhost:8000/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
        credentials: "include", // Wichtig für Cookies
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Anmeldung fehlgeschlagen")
      }

      // Erfolgreiche Anmeldung
      toast({
        title: "Erfolgreich angemeldet",
        description: "Willkommen zurück bei Harmony Heaven Hotels",
      })

      // Token im localStorage speichern (optional, je nach Sicherheitsanforderungen)
      if (data.access_token) {
        localStorage.setItem("token", data.access_token)
      }

      onSuccess()
    } catch (error) {
      console.error("Login error:", error)
      toast({
        title: "Fehler bei der Anmeldung",
        description: error instanceof Error ? error.message : "Bitte überprüfen Sie Ihre Anmeldedaten",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 py-2">
      <div className="space-y-2">
        <Label htmlFor="email">E-Mail</Label>
        <Input
          id="email"
          type="email"
          placeholder="ihre.email@beispiel.de"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <Label htmlFor="password">Passwort</Label>
          <Button variant="link" size="sm" className="px-0 font-normal h-auto">
            Passwort vergessen?
          </Button>
        </div>
        <Input
          id="password"
          type="password"
          placeholder="••••••••"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      <div className="flex items-center space-x-2">
        <Checkbox id="remember" />
        <Label htmlFor="remember" className="text-sm font-normal">
          Angemeldet bleiben
        </Label>
      </div>
      <Button
        type="submit"
        className="w-full font-cinzel bg-primary text-primary-foreground hover:bg-primary/90"
        disabled={isLoading}
      >
        {isLoading ? "Wird angemeldet..." : "Anmelden"}
      </Button>
    </form>
  )
}

