"use client"

import type React from "react"

import { useState, useEffect } from "react"
import Image from "next/image"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { AuthModal } from "@/components/auth/auth-modal"
import { Menu, X } from "lucide-react"

export function Header() {
  const [isScrolled, setIsScrolled] = useState(false)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false)
  const [authModalTab, setAuthModalTab] = useState<"login" | "register">("login")

  // Überwache das Scrollen, um den Header anzupassen
  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 10) {
        setIsScrolled(true)
      } else {
        setIsScrolled(false)
      }
    }

    window.addEventListener("scroll", handleScroll)
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  const openAuthModal = (tab: "login" | "register") => {
    setAuthModalTab(tab)
    setIsAuthModalOpen(true)
    setIsMobileMenuOpen(false)
  }

  // Funktion für sanftes Scrollen zu Ankerpunkten
  const scrollToSection = (e: React.MouseEvent<HTMLAnchorElement>, sectionId: string) => {
    e.preventDefault()
    const section = document.getElementById(sectionId)
    if (section) {
      window.scrollTo({
        top: section.offsetTop,
        behavior: "smooth",
      })
      setIsMobileMenuOpen(false)
    }
  }

  return (
    <>
      <header
        className={`sticky top-0 z-50 w-full border-b border-primary/20 transition-all duration-300 ${
          isScrolled ? "h-16 bg-background/95 backdrop-blur-md" : "h-20 bg-transparent"
        }`}
      >
        <div className="container h-full flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Image
              src="/logo-transparent.png"
              alt="Harmony Heaven Hotels Logo"
              width={50}
              height={50}
              className={`transition-all duration-300 ${isScrolled ? "h-10 w-auto" : "h-12 w-auto"}`}
            />
            <span
              className={`font-cinzel font-semibold tracking-wider text-primary uppercase transition-all duration-300 ${
                isScrolled ? "text-lg" : "text-xl"
              }`}
            >
              Harmony Heaven Hotels
            </span>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex gap-6">
            <Link
              href="#"
              className="font-cinzel text-sm font-medium hover:text-primary transition-colors uppercase"
              onClick={(e) => scrollToSection(e, "")}
            >
              Home
            </Link>
            <Link
              href="#about"
              className="font-cinzel text-sm font-medium hover:text-primary transition-colors uppercase"
              onClick={(e) => scrollToSection(e, "about")}
            >
              Über uns
            </Link>
            <Link
              href="#locations"
              className="font-cinzel text-sm font-medium hover:text-primary transition-colors uppercase"
              onClick={(e) => scrollToSection(e, "locations")}
            >
              Standorte
            </Link>
            <Link
              href="#amenities"
              className="font-cinzel text-sm font-medium hover:text-primary transition-colors uppercase"
              onClick={(e) => scrollToSection(e, "amenities")}
            >
              Annehmlichkeiten
            </Link>
            <Link
              href="#contact"
              className="font-cinzel text-sm font-medium hover:text-primary transition-colors uppercase"
              onClick={(e) => scrollToSection(e, "contact")}
            >
              Kontakt
            </Link>
          </nav>

          {/* Desktop Auth Buttons */}
          <div className="hidden md:flex items-center gap-4">
            <Button
              variant="outline"
              className="border-primary text-primary hover:bg-primary hover:text-primary-foreground font-cinzel"
              onClick={() => openAuthModal("login")}
            >
              Anmelden
            </Button>
            <Button className="font-cinzel" onClick={() => openAuthModal("register")}>
              Registrieren
            </Button>
          </div>

          {/* Mobile Menu Button */}
          <Button
            variant="ghost"
            className="md:hidden"
            size="icon"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            {isMobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </Button>
        </div>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden absolute top-full left-0 right-0 bg-background border-b border-primary/20 py-4 shadow-lg">
            <nav className="container flex flex-col gap-4">
              <Link
                href="#"
                className="font-cinzel text-sm font-medium hover:text-primary transition-colors uppercase py-2"
                onClick={(e) => scrollToSection(e, "")}
              >
                Home
              </Link>
              <Link
                href="#about"
                className="font-cinzel text-sm font-medium hover:text-primary transition-colors uppercase py-2"
                onClick={(e) => scrollToSection(e, "about")}
              >
                Über uns
              </Link>
              <Link
                href="#locations"
                className="font-cinzel text-sm font-medium hover:text-primary transition-colors uppercase py-2"
                onClick={(e) => scrollToSection(e, "locations")}
              >
                Standorte
              </Link>
              <Link
                href="#amenities"
                className="font-cinzel text-sm font-medium hover:text-primary transition-colors uppercase py-2"
                onClick={(e) => scrollToSection(e, "amenities")}
              >
                Annehmlichkeiten
              </Link>
              <Link
                href="#contact"
                className="font-cinzel text-sm font-medium hover:text-primary transition-colors uppercase py-2"
                onClick={(e) => scrollToSection(e, "contact")}
              >
                Kontakt
              </Link>
              <div className="flex flex-col gap-3 pt-2">
                <Button
                  variant="outline"
                  className="w-full border-primary text-primary hover:bg-primary hover:text-primary-foreground font-cinzel"
                  onClick={() => openAuthModal("login")}
                >
                  Anmelden
                </Button>
                <Button className="w-full font-cinzel" onClick={() => openAuthModal("register")}>
                  Registrieren
                </Button>
              </div>
            </nav>
          </div>
        )}
      </header>

      {/* Auth Modal */}
      <AuthModal isOpen={isAuthModalOpen} onClose={() => setIsAuthModalOpen(false)} defaultTab={authModalTab} />
    </>
  )
}

