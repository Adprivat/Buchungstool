"use client"

import { useState } from "react"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { LoginForm } from "./login-form"
import { RegisterForm } from "./register-form"

interface AuthModalProps {
  isOpen: boolean
  onClose: () => void
  defaultTab?: "login" | "register"
}

export function AuthModal({ isOpen, onClose, defaultTab = "login" }: AuthModalProps) {
  const [activeTab, setActiveTab] = useState<string>(defaultTab)

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle className="font-cinzel text-center text-2xl uppercase">
            {activeTab === "login" ? "Anmelden" : "Registrieren"}
          </DialogTitle>
          <DialogDescription className="text-center">
            {activeTab === "login"
              ? "Melden Sie sich an, um Ihr Konto zu verwalten und Buchungen vorzunehmen."
              : "Erstellen Sie ein Konto, um von exklusiven Angeboten zu profitieren."}
          </DialogDescription>
        </DialogHeader>
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="login" className="font-cinzel">
              Anmelden
            </TabsTrigger>
            <TabsTrigger value="register" className="font-cinzel">
              Registrieren
            </TabsTrigger>
          </TabsList>
          <TabsContent value="login">
            <LoginForm onSuccess={onClose} />
          </TabsContent>
          <TabsContent value="register">
            <RegisterForm
              onSuccess={() => {
                setActiveTab("login")
              }}
            />
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  )
}

