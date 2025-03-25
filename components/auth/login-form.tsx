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
      // Formular-Daten für die OAuth2-Anforderung vorbereiten
      const formData = new FormData();
      formData.append("username", email); // Backend erwartet 'username' statt 'email'
      formData.append("password", password);

      // Verschiedene API-Endpunkt-URLs ausprobieren
      const apiUrls = [
        "http://localhost:8000/api/auth/login",
        "http://127.0.0.1:8000/api/auth/login"
      ];
      
      let response = null;
      let error = null;
      
      // Versuchen Sie jeden API-Endpunkt
      for (const url of apiUrls) {
        try {
          console.log(`Trying to connect to: ${url}`);
          response = await fetch(url, {
            method: "POST",
            body: formData,
            credentials: "include", // Wichtig für Cookies
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
        throw error || new Error("Verbindung zum Server nicht möglich");
      }

      const data = await response.json();

      // Erfolgreiche Anmeldung
      toast({
        title: "Erfolgreich angemeldet",
        description: "Willkommen zurück bei Harmony Heaven Hotels",
      });

      // Token im localStorage speichern
      if (data.access_token) {
        localStorage.setItem("token", data.access_token);
      }

      // Callback für erfolgreiche Anmeldung aufrufen
      onSuccess();
    } catch (error) {
      console.error("Login error:", error);
      toast({
        title: "Fehler bei der Anmeldung",
        description: error instanceof Error 
          ? error.message 
          : "Verbindung zum Server fehlgeschlagen. Bitte stellen Sie sicher, dass der Server läuft.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

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

