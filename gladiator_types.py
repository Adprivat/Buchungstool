from dataclasses import dataclass
from typing import List, Dict

@dataclass
class GladiatorType:
    name: str
    description: str
    advantages: List[str]
    disadvantages: List[str]
    modifiers: Dict[str, int]
    special_ability: str

# Basislebenspunkte für alle Gladiatoren
BASE_LP = 100

# Definition der Gladiator‑Arten
gladiator_types = {
    "Retiarius": GladiatorType(
        name="Retiarius",
        description=(
            "Netzkämpfer – Leicht bewaffnet mit Netz, Dreizack und Dolch. "
            "Kein Helm, nur Schulter- und Armschutz."
        ),
        advantages=["Schnell", "Wendig", "Kann Gegner mit dem Netz fangen und aus der Distanz angreifen"],
        disadvantages=["Wenig Schutz", "Anfällig gegen schwerere Gegner"],
        modifiers={"Agilität": 3, "Präzision": 2, "Konstitution": -1, "Grundrüstung": -2},
        special_ability=(
            "Netzwurf – Wirft das Netz, um den Gegner für eine Runde bewegungsunfähig zu machen "
            "(Wurf auf Präzision gegen die Agilität des Gegners)."
        )
    ),
    "Secutor": GladiatorType(
        name="Secutor",
        description=(
            "Verfolger – Schwer gepanzert mit großem Schild, Gladius (Kurzschwert) und Helm mit Sehschlitzen."
        ),
        advantages=["Stark gepanzert", "Guter Nahkämpfer"],
        disadvantages=["Langsam", "Eingeschränkte Sicht durch Helm"],
        modifiers={"Konstitution": 3, "Grundrüstung": 4, "Agilität": -1, "Präzision": -1},
        special_ability=(
            "Schildwall – Erhöht seine Grundrüstung für eine Runde, um sich vor einem starken Angriff zu schützen."
        )
    ),
    "Murmillo": GladiatorType(
        name="Murmillo",
        description=(
            "Fischhelm – Ähnlich dem Secutor, aber mit anderem Helmtyp und kleinerem Schild."
        ),
        advantages=["Gut gepanzert", "Vielseitig im Kampf"],
        disadvantages=["Weniger Schutz als der Secutor, aber auch etwas wendiger"],
        modifiers={"Stärke": 1, "Konstitution": 2, "Agilität": -1},
        special_ability=(
            "Hieb und Stoß – Führt eine Kombination aus einem kräftigen Hieb mit dem Gladius und einem schnellen Stoß aus, um den Gegner zu überraschen."
        )
    ),
    "Thraex": GladiatorType(
        name="Thraex",
        description=(
            "Thraker – Leicht bewaffnet mit Sica (gebogenes Schwert), kleinem Schild und Helm mit hohem Kamm."
        ),
        advantages=["Schnell", "Wendig", "Guter Angreifer"],
        disadvantages=["Wenig Schutz", "Anfällig gegen schwerere Gegner"],
        modifiers={"Agilität": 2, "Stärke": 1, "Konstitution": -1, "Grundrüstung": -1},
        special_ability=(
            "Sichelhieb – Führt einen schnellen, seitlichen Hieb mit der Sica aus, der den Gegner bluten lässt "
            "(zusätzlicher Blutungsschaden über Zeit)."
        )
    ),
    "Hoplomachus": GladiatorType(
        name="Hoplomachus",
        description=(
            "Schwerbewaffneter – Schwer bewaffnet mit Speer, Gladius und kleinem rundem Schild."
        ),
        advantages=["Gute Reichweite mit dem Speer", "Stark im Nahkampf"],
        disadvantages=["Weniger wendig als leichtere Klassen"],
        modifiers={"Stärke": 2, "Ausdauer": 1, "Agilität": -1},
        special_ability=(
            "Speerstich – Führt einen kraftvollen Stich mit dem Speer aus, der den Gegner zurückstoßen kann."
        )
    ),
    "Dimachaerus": GladiatorType(
        name="Dimachaerus",
        description=(
            "Doppelkämpfer – Kämpfer, der zwei Schwerter oder Dolche gleichzeitig führt. Selten."
        ),
        advantages=["Sehr gefährlich im Nahkampf", "Unberechenbar"],
        disadvantages=["Benötigt viel Übung", "Hoher Energieverbrauch"],
        modifiers={"Stärke": 2, "Agilität": 1, "Konstitution": -1},
        special_ability=(
            "Doppelhieb – Führt zwei schnelle Hiebe mit den Schwertern gleichzeitig aus, die den Gegner überraschen und verwunden können."
        )
    ),
    "Provocator": GladiatorType(
        name="Provocator",
        description=(
            "Herausforderer – Mittelschwer bewaffnet mit Brustpanzer, Schild, Gladius und Helm."
        ),
        advantages=["Guter Kompromiss zwischen Schutz und Beweglichkeit"],
        disadvantages=["Nicht so stark gepanzert wie schwere Klassen"],
        modifiers={"Konstitution": 1, "Grundrüstung": 2, "Agilität": -1},
        special_ability=(
            "Provozieren – Versucht, den Gegner durch Spott oder Drohungen aus der Fassung zu bringen, was dessen "
            "Agilität oder Angriffskraft für eine Runde verringern kann."
        )
    ),
}

def get_all_gladiator_types():
    """Gibt das Dictionary aller definierten Gladiator‑Arten zurück."""
    return gladiator_types

if __name__ == "__main__":
    # Zum Testen: Ausgabe aller Gladiator-Typen und deren Attribute
    for key, gladiator in gladiator_types.items():
        print(f"{gladiator.name}:")
        print(f"  Beschreibung: {gladiator.description}")
        print(f"  Vorteile: {', '.join(gladiator.advantages)}")
        print(f"  Nachteile: {', '.join(gladiator.disadvantages)}")
        print(f"  Attributmodifikatoren: {gladiator.modifiers}")
        print(f"  Spezialfähigkeit: {gladiator.special_ability}")
        print(f"  Basis LP: {BASE_LP}")
        print()
