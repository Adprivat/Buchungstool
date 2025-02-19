import os
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus .env Datei
load_dotenv()

# Überprüfe, ob alle erforderlichen Umgebungsvariablen vorhanden sind
required_env_vars = ["DB_HOST", "DB_PORT", "DB_USER", "DB_PASSWORD", "DB_NAME", "SERVER_HOST", "SERVER_PORT"]
for var in required_env_vars:
    if var not in os.environ:
        raise EnvironmentError(f"Erforderliche Umgebungsvariable {var} ist nicht gesetzt.")

# Datenbank-Konfiguration
db_config = {
    'host': os.environ['DB_HOST'],
    'port': int(os.environ['DB_PORT']),
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
    'database': os.environ['DB_NAME']
}

# Server-Konfiguration
server_config = {
    'host': os.environ['SERVER_HOST'],
    'port': int(os.environ['SERVER_PORT'])
} 