# Verwende das offizielle Python-Image als Basis
FROM python:3.8-slim

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die Anforderungsdatei in das Arbeitsverzeichnis
COPY requirements.txt ./

# Installiere alle in der Anforderungsdatei aufgeführten Pakete
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest des Anwendungsverzeichnisses in das Arbeitsverzeichnis
COPY . .

# Mache den Port, auf dem die Anwendung läuft, nach außen hin zugänglich
EXPOSE 5000

# Definiere den Befehl zum Starten der Anwendung
CMD ["python", "app.py"]

