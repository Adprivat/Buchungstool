from dataclasses import dataclass
from typing import List, Dict

class GladiatorType:
    def __init__(self, name, modifiers, strengths, weaknesses):
        self.name = name
        self.modifiers = modifiers
        self.strengths = strengths
        self.weaknesses = weaknesses

# Basislebenspunkte für alle Gladiatoren
BASE_LP = 10

# Definition der Gladiator‑Arten
gladiator_types = {
    "Murmillo": GladiatorType(
        "Murmillo",
        {"angriff": -1, "verteidigung": 2, "ausdauer": 1},
        "Sehr gute Verteidigung, solide Ausdauer",
        "Geringere Angriffseffektivität"
    ),
    "Secutor": GladiatorType(
        "Secutor",
        {"angriff": 0, "verteidigung": 1, "ausdauer": 0},
        "Gute Defensive, besonders gegen Netzkämpfer",
        "Keine herausragende Offensivkraft"
    ),
    "Thraex": GladiatorType(
        "Thraex",
        {"angriff": 1, "verteidigung": -1, "ausdauer": 1},
        "Schnelle und effektive Angriffe",
        "Weniger Schutz durch kleines Schild"
    ),
    "Hoplomachus": GladiatorType(
        "Hoplomachus",
        {"angriff": 2, "verteidigung": -2, "ausdauer": 1},
        "Hohe Angriffskraft durch Speer",
        "Schwache Defensive durch kleines Schild"
    ),
    "Dimachaerus": GladiatorType(
        "Dimachaerus",
        {"angriff": 2, "verteidigung": -2, "ausdauer": 1},
        "Sehr starker Angriff durch zwei Waffen",
        "Kaum Schutz gegen Angriffe"
    ),
    "Retiarius": GladiatorType(
        "Retiarius",
        {"angriff": 1, "verteidigung": -3, "ausdauer": 2},
        "Sehr beweglich, kann lange kämpfen",
        "Extrem verwundbar bei direkten Angriffen"
    ),
    "Provocator": GladiatorType(
        "Provocator",
        {"angriff": -1, "verteidigung": 2, "ausdauer": 0},
        "Hohe Verteidigung durch Panzerung",
        "Geringe Angriffsstärke"
    )
}

def get_all_gladiator_types():
    """Gibt das Dictionary aller definierten Gladiator‑Arten zurück."""
    return gladiator_types

if __name__ == "__main__":
    # Zum Testen: Ausgabe aller Gladiator-Typen und deren Attribute
    for key, gladiator in gladiator_types.items():
        print(f"{gladiator.name}:")
        print(f"  Vorteile: {gladiator.strengths}")
        print(f"  Nachteile: {gladiator.weaknesses}")
        print(f"  Attributmodifikatoren: {gladiator.modifiers}")
        print(f"  Basis LP: {BASE_LP}")
        print()
