# DepotCheck 2026 📈

Ein automatisiertes System zur Überwachung von ETFs, das auf einer **QNAP NAS** in einer isolierten **Docker-Umgebung** läuft. Das Tool ruft stündliche Marktdaten ab, berechnet Profit/Loss und speichert die Historie in einer MariaDB.

## 🛠 Architektur & Tech-Stack

* **Sprache:** Python 3.11+
* **Containerisierung:** Docker & Docker Compose (Debian-Basis)
* **Datenbank:** MariaDB (extern oder als Container)
* **API:** Yahoo Finance (`yfinance`)
* **Logging:** Custom Python Logging mit `RotatingFileHandler` (5MB Limit)



## 📁 Projektstruktur

* `depotcheck.py`: Das Hauptskript für den Abgleich.
* `log_modul.py`: Zentrales Logging-Management (vermeidet Log-Spam von Bibliotheken).
* `orders_model.py` / `marketdata_model.py`: Datenbankschicht (Models).
* `docker-compose.yml`: Definition der Container-Umgebung.
* `.gitignore`: Verhindert das Einchecken von Passwörtern und Cache-Müll.

## 🚀 Installation & Deployment (QNAP)

### 1. Vorbereitung
Die Dateien in ein Verzeichnis auf der QNAP kopieren (z.B. `/share/Software/DepChk`).

### 2. Container starten
```bash
docker-compose up -d
