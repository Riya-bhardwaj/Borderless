# Borderless

**Cross boundaries with confidence.** Borderless is a native Android application that proactively detects when users cross geographic boundaries (Indian state/city borders) and delivers importance-filtered legal, cultural, and behavioral context alerts with a multilingual dashboard and live AI-powered Q&A.

Built as a hackathon MVP focused on demo stability and architectural clarity.

## Features

### Geo-Intelligence Engine
- State-level geofencing using Android Location Services & Geofencing API
- Automatic boundary crossing detection with real-time alerts
- Supports 3-4 Indian states with curated datasets (Karnataka, Delhi, Maharashtra, Tamil Nadu)

### Proactive Alert Engine
- Categorized alerts: **Legal**, **Cultural**, **Behavioral**
- Severity-based scoring: Critical, Important, Informational
- Smart notification governance (max 2 alerts per boundary, 24-hour suppression)
- Push notifications via Firebase Cloud Messaging

### Context Dashboard
- Location card with quick facts about the current region
- Filterable alerts list with severity badges
- Region summary with alert counts
- Offline indicator for connectivity awareness

### Live Contextual Q&A (Gemini AI)
- Powered by **Gemini 2.5 Flash** via direct REST API
- Acts as a knowledgeable local expert for all of India
- Provides insights on culture, laws, geography, food, language, attractions, permits, safety, scams, and weather
- Risk-rated responses (Low / Medium / High / Critical)
- Source citations for grounded answers
- Multilingual response generation
- Works with or without alert data

### User Personalization
- Anonymous sign-in via Firebase Authentication
- Language preference (multilingual support)
- Region-based alert filtering
- Onboarding flow for initial setup

## Tech Stack

### Android App
| Component | Technology |
|-----------|-----------|
| Language | Kotlin |
| UI | Jetpack Compose + Material Design 3 |
| Architecture | MVVM + Clean Architecture |
| DI | Hilt |
| Navigation | Jetpack Navigation Compose |
| Local DB | Room |
| Networking | Retrofit + OkHttp |
| Auth | Firebase Authentication |
| Database | Cloud Firestore |
| Push Notifications | Firebase Cloud Messaging |
| Location | Google Play Services Location |
| AI | Gemini 2.5 Flash (REST API) |

### Backend
| Component | Technology |
|-----------|-----------|
| Runtime | Node.js 20+ |
| Framework | Express.js |
| Hosting | Firebase Cloud Functions |
| Database | Cloud Firestore |
| AI | Google Generative AI SDK |

### SDK Requirements
- Compile SDK: 35 (Android 15)
- Min SDK: 29 (Android 10)
- Target SDK: 35 (Android 15)
- Java/Kotlin: 17

## Project Structure

```
Borderless/
├── android/                    # Android application
│   └── app/src/main/java/com/borderless/app/
│       ├── data/
│       │   ├── local/          # Room database, entities, DAOs
│       │   ├── remote/         # Retrofit API interface & DTOs
│       │   └── repository/     # Repository implementations
│       ├── domain/
│       │   ├── model/          # Data classes (Region, Alert, QaInteraction, etc.)
│       │   ├── repository/     # Repository interfaces
│       │   └── usecase/        # Business logic (AskQuestionUseCase, etc.)
│       ├── di/                 # Hilt dependency injection modules
│       ├── service/            # GeminiService, GeofenceService, FCM, Notifications
│       └── ui/
│           ├── dashboard/      # Main dashboard screen
│           ├── alerts/         # Alert detail screen
│           ├── qa/             # Q&A screen with Gemini AI
│           ├── settings/       # User settings
│           ├── onboarding/     # First-time setup
│           ├── components/     # Reusable UI components
│           ├── navigation/     # Bottom nav & routing
│           └── theme/          # Material 3 theme, colors, typography
├── backend/                    # Node.js Firebase Cloud Functions
└── .specify/                   # Feature specifications & planning
```

## Getting Started

### Prerequisites
- Android Studio (latest stable)
- JDK 17+
- A Google Cloud project with:
  - Firebase project configured
  - Gemini API key

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Borderless
   ```

2. **Configure Firebase**
   - Create a Firebase project at [Firebase Console](https://console.firebase.google.com)
   - Enable Authentication (Anonymous sign-in)
   - Enable Cloud Firestore
   - Download `google-services.json` and place it in `android/app/`

3. **Configure Gemini API Key**
   - Get an API key from [Google AI Studio](https://aistudio.google.com/apikey)
   - Add to `android/local.properties`:
     ```properties
     gemini.api.key=YOUR_GEMINI_API_KEY
     ```

4. **Build and Run**
   ```bash
   cd android
   ./gradlew assembleDebug
   ```
   Or open the `android/` directory in Android Studio and run directly.

### Backend Setup (Optional)

The Android app can work independently with Gemini direct API calls and Firestore reads. The backend is optional for additional API endpoints.

```bash
cd backend
npm install
npm run build
npm run serve    # Local emulator
npm run deploy   # Deploy to Firebase
npm run seed     # Seed Firestore with demo data
```

## Architecture

The app follows **Clean Architecture** with three layers:

```
UI Layer (Compose Screens + ViewModels)
         ↓
Domain Layer (Use Cases + Repository Interfaces + Models)
         ↓
Data Layer (Repository Implementations + Remote API + Local DB)
```

- **UI Layer**: Jetpack Compose screens with Material 3, state managed via `StateFlow` in ViewModels
- **Domain Layer**: Pure Kotlin business logic, no Android dependencies
- **Data Layer**: Firestore for region/alert data, Room for crossing history, OkHttp for Gemini API

### Data Flow
```
Geofence Trigger → GeofenceService → Alert Fetch → Notification → Dashboard Update
                                                                        ↓
User Question → QaViewModel → AskQuestionUseCase → QaRepository → GeminiService → AI Response
```

## Permissions

| Permission | Purpose |
|-----------|---------|
| `ACCESS_FINE_LOCATION` | Precise geofencing |
| `ACCESS_COARSE_LOCATION` | Approximate location |
| `ACCESS_BACKGROUND_LOCATION` | Geofence monitoring when app is closed |
| `FOREGROUND_SERVICE_LOCATION` | Location tracking service |
| `POST_NOTIFICATIONS` | Alert notifications |
| `RECEIVE_BOOT_COMPLETED` | Re-register geofences after device restart |
| `INTERNET` | API calls & Firestore sync |

## Hackathon Trade-offs

- Hardcoded 3-4 Indian states with curated datasets
- Predefined geofences (state-level only)
- Simplified alert scoring (severity-based)
- Anonymous authentication (no full user accounts)
- Seeded demo data for reliability
- No full personalization engine
- Direct Gemini API calls instead of backend-proxied AI
