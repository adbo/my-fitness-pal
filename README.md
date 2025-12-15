# My Fitness Pal - Aplikacja do Śledzenia Progresji Ćwiczeń

Aplikacja webowa do śledzenia treningów z **systemem progresji ćwiczeń** - przechodzisz od łatwiejszych do trudniejszych wariantów ćwiczeń.

## Funkcje

- **Łańcuchy Progresji**: Przechodzenie od łatwiejszych do trudniejszych wariantów ćwiczeń
  - Przykład: Pompki od ściany → Pompki od blatu → Pompki na kolanach → Pełne pompki → Pompki diamentowe
- **Śledzenie Postępów**: Śledź swój aktualny poziom w każdej progresji
- **Automatyczne Sugestie**: Otrzymuj powiadomienia gdy jesteś gotowy na trudniejsze ćwiczenie

## Architektura

- **Frontend**: React + TypeScript + Vite
- **Backend**: Firebase Firestore (bez serwera!)

## Instalacja i Uruchomienie

### 1. Konfiguracja Firebase

1. Utwórz projekt na [Firebase Console](https://console.firebase.google.com/)
2. Włącz Firestore Database
3. Skopiuj dane konfiguracyjne

### 2. Konfiguracja aplikacji

```bash
# Skopiuj plik z przykładową konfiguracją
cp .env.example .env

# Uzupełnij dane Firebase w pliku .env
```

### 3. Uruchomienie

```bash
npm install
npm run dev
```

Aplikacja uruchomi się na `http://localhost:3000`

## Struktura Projektu

```
my-fitness-pal/
├── src/
│   ├── components/     # Komponenty React
│   ├── pages/          # Strony aplikacji
│   ├── firebase/       # Konfiguracja i serwisy Firebase
│   ├── data/           # Dane ćwiczeń (statyczne)
│   └── types/          # Typy TypeScript
├── .env.example        # Przykładowa konfiguracja
└── package.json
```

## System Progresji Ćwiczeń

Każde ćwiczenie należy do **łańcucha progresji**. Gdy opanujesz ćwiczenie (3 serie × 12 powtórzeń), możesz przejść do kolejnego, trudniejszego wariantu.

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

## Deploy

Aplikacja jest statyczna - możesz ją hostować za darmo na:
- Firebase Hosting
- Vercel
- Netlify
- GitHub Pages

```bash
npm run build
# Folder dist/ zawiera gotową aplikację
```

## Licencja

MIT
