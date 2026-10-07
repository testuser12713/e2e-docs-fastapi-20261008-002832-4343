# Notizen-REST-API

Eine kleine REST-API auf Basis von FastAPI und Pydantic v2 zum Anlegen,
Auflisten, Abrufen und Löschen von Notizen. Die Notizen liegen in einem
In-Memory-Speicher und gelten nur für die Laufzeit des Prozesses — es gibt keine
Datenbank und keinen Persistenzanspruch über den Prozesslauf hinaus. Die
Konfiguration läuft vollständig über `pydantic-settings`; alle Werte haben
sinnvolle Vorgaben und können per Umgebungsvariable überschrieben werden.

## Tech Stack

- **Sprache:** Python 3.13
- **Framework:** FastAPI
- **Validierung:** Pydantic v2 (`model_config`, `field_validator`)
- **Konfiguration:** pydantic-settings (`BaseSettings`)
- **Server:** uvicorn
- **Speicher:** In-Memory (prozessweit, keine Datenbank)
- **Tests:** pytest mit dem FastAPI `TestClient`
- **Lint:** ruff

## Installation

```bash
python -m pip install -r requirements.txt
```

## Starten (Entwicklung)

Aus dem Repository-Wurzelverzeichnis:

```bash
uvicorn app.main:app
```

Die API ist dann unter `http://127.0.0.1:8000` erreichbar. Während der
Entwicklung kann mit automatischem Neuladen gearbeitet werden:

```bash
uvicorn app.main:app --reload
```

## Produktion

Für Python gibt es keinen separaten Build-Schritt. Für den Produktivbetrieb wird
der Server ohne Reload gestartet und an alle Interfaces gebunden:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Konfiguration (Umgebungsvariablen)

Die Einstellungen werden über `pydantic-settings` gelesen. Ohne gesetzte
Umgebungsvariablen startet die Anwendung mit den Standardwerten.

| Variable           | Typ   | Standard    | Bedeutung                            |
| ------------------ | ----- | ----------- | ------------------------------------ |
| `APP_NAME`         | str   | `Notes API` | Name der Anwendung (OpenAPI-Titel)   |
| `MAX_TAGS`         | int   | `5`         | Maximale Anzahl Tags pro Notiz       |
| `MAX_TITLE_LENGTH` | int   | `100`       | Maximale Länge des Titels in Zeichen |

## Verwendung

Interaktive Dokumentation: `http://127.0.0.1:8000/docs`, das OpenAPI-Schema
unter `http://127.0.0.1:8000/openapi.json`.

### Datenmodelle

**NoteCreate** (Eingabe beim Anlegen):

```json
{
  "titel": "Einkaufsliste",
  "inhalt": "Milch und Brot",
  "tags": ["privat", "haushalt"]
}
```

`titel` ist Pflicht (1 bis `MAX_TITLE_LENGTH` Zeichen), `inhalt` und `tags` sind
optional (`inhalt` standardmäßig `""`, `tags` standardmäßig `[]`, höchstens
`MAX_TAGS` Einträge).

**Note** (Ausgabe):

```json
{
  "id": "3f1b2c4d-5e6f-4a7b-8c9d-0e1f2a3b4c5d",
  "titel": "Einkaufsliste",
  "inhalt": "Milch und Brot",
  "tags": ["privat", "haushalt"],
  "erstellt_am": "2026-10-07T12:00:00+00:00"
}
```

### Endpunkte

| Methode  | Pfad          | Anfrage                        | Antwort                          |
| -------- | ------------- | ------------------------------ | -------------------------------- |
| `POST`   | `/notes`      | `NoteCreate`                   | `201` mit `Note`                 |
| `GET`    | `/notes`      | optional `?tag=<tag>`          | `200` mit Liste von `Note`       |
| `GET`    | `/notes/{id}` | —                              | `200` mit `Note`, sonst `404`    |
| `DELETE` | `/notes/{id}` | —                              | `204` ohne Inhalt, sonst `404`   |
| `GET`    | `/health`     | —                              | `200` `{"status": "ok"}`         |

Fehlermeldungen liefern einen JSON-Body der Form `{"detail": "..."}`. Eine
ungültige Nutzlast beim Anlegen liefert `422` im Standardformat von Pydantic. Ein
unbekannter Tag im Filter ergibt eine leere Liste (`200 []`).

> Hinweis: Im aktuellen Skeleton antworten die vier Notiz-Routen noch mit `501
> Not Implemented`; sie werden von den jeweiligen Folge-Tickets implementiert.

## Tests

```bash
PYTHONPATH=. pytest
```

## Funktionen

- Anlegen einer Notiz mit Titel, optionalem Inhalt und bis zu `MAX_TAGS` Tags
- Auflisten aller Notizen, optional nach einem Tag gefiltert
- Abrufen einer einzelnen Notiz über ihre ID
- Löschen einer Notiz über ihre ID
- Validierung über Pydantic v2 (getrimmter Titel, Tag-Obergrenze)
- Konfiguration über Umgebungsvariablen mit Standardwerten
- Liveness-Endpunkt `/health`
