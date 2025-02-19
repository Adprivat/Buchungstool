import os
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus .env Datei
load_dotenv()

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