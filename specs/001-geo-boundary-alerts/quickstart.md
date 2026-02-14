# Quickstart: Borderless Hackathon MVP

**Branch**: `001-geo-boundary-alerts`
**Date**: 2026-02-14

## Prerequisites

- Android Studio Ladybug (2024.2+) with Kotlin 2.0+
- Node.js 20+ and npm
- Firebase CLI (`npm install -g firebase-tools`)
- Google Cloud project with:
  - Firebase enabled (Auth, Firestore, Cloud Functions)
  - Gemini API enabled (Google AI Studio API key)
- Android device or emulator (API 29+) with Google Play Services

## 1. Clone and Setup

```bash
git clone <repo-url>
cd Borderless
git checkout 001-geo-boundary-alerts
```

## 2. Firebase Setup

```bash
# Login to Firebase
firebase login

# Initialize Firebase in the backend directory
cd backend
firebase init
# Select: Firestore, Functions, Emulators
# Use existing project or create new one
```

Create `backend/.env`:
```env
GEMINI_API_KEY=your-gemini-api-key-here
FIREBASE_PROJECT_ID=your-project-id
```

## 3. Seed Database

```bash
cd backend
npm install
npm run seed
# Seeds 4 Indian states with ~80 alert entries
```

## 4. Deploy Cloud Functions

```bash
cd backend
npm run deploy
# Or for local development:
npm run serve
# Functions available at http://localhost:5001/<project>/us-central1/api
```

## 5. Android App Setup

1. Download `google-services.json` from Firebase Console
2. Place it in `android/app/google-services.json`
3. Create `android/local.properties` (if not exists):
   ```properties
   sdk.dir=/path/to/Android/Sdk
   ```
4. Create `android/app/src/main/res/values/secrets.xml`:
   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <resources>
       <string name="api_base_url">https://YOUR_REGION-YOUR_PROJECT.cloudfunctions.net/api</string>
   </resources>
   ```

## 6. Build and Run

```bash
cd android
./gradlew assembleDebug
# Or open in Android Studio and run on device/emulator
```

## 7. Demo Walkthrough

### Setup Mock Location (for demo)
1. Enable Developer Options on device
2. Set "Select mock location app" to Borderless (or a GPS spoofing app)
3. Set initial location to Mumbai (19.0760, 72.8777)

### Demo Flow
1. **Sign up** — enter name, select language, set alert filters
2. **Dashboard** — see Mumbai region card with quick facts
3. **Simulate crossing** — change mock location to Bangalore (12.9716, 77.5946)
4. **Notification** — system notification appears: "You've entered Karnataka"
5. **Tap notification** — opens alert detail with Legal/Cultural/Behavioral cards
6. **Dashboard update** — region card now shows Karnataka, crossing in history
7. **Q&A** — ask "Is alcohol easily available in Karnataka?"
8. **Response** — grounded answer with risk rating and source citation
9. **Language switch** — change to Hindi, see all content translate

### Expected Timing
- Sign-up to dashboard: < 30 seconds
- Boundary crossing to notification: < 10 seconds
- Q&A question to answer: < 5 seconds
- Language switch: < 2 seconds (UI) + < 3 seconds (content translation)

## Troubleshooting

- **Geofence not triggering**: Ensure location permissions are "Allow all the
  time" (background location). Check that Google Play Services is up to date.
- **Gemini API errors**: Verify API key in `.env`. Check quota in Google AI
  Studio dashboard. Fallback: seed data includes pre-generated responses.
- **Firestore permission denied**: Ensure Firebase Auth is configured and
  security rules allow authenticated reads.
- **Functions not deploying**: Run `firebase deploy --only functions` with
  `--debug` flag for detailed errors.
