# My Fitness Pal - Aplikacja do Śledzenia Progresji Ćwiczeń

Aplikacja webowa do śledzenia treningów z **systemem progresji ćwiczeń** - przechodzisz od łatwiejszych do trudniejszych wariantów ćwiczeń.

## Funkcje

- **Łańcuchy Progresji**: Przechodzenie od łatwiejszych do trudniejszych wariantów ćwiczeń
  - Przykład: Pompki od ściany → Pompki od blatu → Pompki na kolanach → Pełne pompki → Pompki diamentowe
- **Śledzenie Postępów**: Śledź swój aktualny poziom w każdej progresji
- **Automatyczne Sugestie**: Otrzymuj powiadomienia gdy jesteś gotowy na trudniejsze ćwiczenie
- **Historia Treningów**: Przeglądaj swoje poprzednie treningi

## Architektura

- **Backend**: FastAPI (Python) + SQLite
- **Frontend**: React + TypeScript

## Instalacja i Uruchomienie

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend uruchomi się na `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend uruchomi się na `http://localhost:3000`

## Struktura Projektu

```
my-fitness-pal/
├── backend/
│   └── app/
│       ├── api/           # Endpointy REST API
│       ├── db/            # Konfiguracja bazy danych
│       ├── models/        # Modele SQLAlchemy
│       ├── schemas/       # Schematy Pydantic
│       ├── services/      # Logika biznesowa
│       ├── seed_data.py   # Dane początkowe
│       └── main.py        # Główna aplikacja FastAPI
├── frontend/
│   └── src/
│       ├── api/           # Klient API
│       ├── components/    # Komponenty React
│       ├── pages/         # Strony aplikacji
│       └── types/         # Typy TypeScript
└── README.md
```

## System Progresji Ćwiczeń

Każde ćwiczenie należy do **łańcucha progresji**. Gdy opanujesz ćwiczenie (np. 3 serie × 12 powtórzeń), możesz przejść do kolejnego, trudniejszego wariantu:

### Dostępne Progresje

1. **Progresja Pompek** (7 poziomów)
   - Pompki od ściany → Pompki od blatu → Pompki na kolanach → Pełne pompki → Pompki diamentowe → Pompki łucznika → Pompki na jednej ręce

2. **Progresja Przysiadów** (7 poziomów)
   - Przysiady z asekuracją → Przysiady na skrzynię → Pełne przysiady → Przysiady wąskie → Bułgarskie przysiady → Przysiady krewetka → Przysiady pistoletowe

3. **Progresja Podciągnięć** (7 poziomów)
   - Martwy zwis → Podciągnięcia łopatkowe → Negatywy → Podciągnięcia z asystą → Podciągnięcia → Podciągnięcia z L-sit → Podciągnięcia łucznika

4. **Progresja Core** (7 poziomów)
   - Deska → Deska boczna → Unoszenie kolan → Unoszenie nóg → Palce do drążka → L-sit → Flaga smoka

5. **Progresja Dipów** (6 poziomów)
   - Dipy na ławce → Negatywy → Dipy z asystą → Dipy na poręczach → Dipy na kółkach → Dipy z obciążeniem

6. **Progresja Wiosłowania** (6 poziomów)
   - Wiosłowanie pod kątem → Wiosłowanie poziome → Wiosłowanie szerokie → Wiosłowanie z nogami na podwyższeniu → Wiosłowanie łucznika → Wiosłowanie na jednej ręce

## API Endpoints

- `GET /api/progressions` - Lista wszystkich progresji
- `GET /api/progressions/{chain_id}` - Szczegóły progresji z ćwiczeniami
- `GET /api/users/{username}/progressions` - Status wszystkich progresji użytkownika
- `POST /api/users/{username}/progressions/{chain_id}/record` - Zapisz trening
- `POST /api/users/{username}/progressions/{chain_id}/advance` - Przejdź do trudniejszego ćwiczenia
- `POST /api/users/{username}/progressions/{chain_id}/regress` - Wróć do łatwiejszego ćwiczenia

## Licencja

MIT
