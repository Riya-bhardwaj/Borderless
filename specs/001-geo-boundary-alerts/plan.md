# Implementation Plan: Geo-Boundary Context Alerts

**Branch**: `001-geo-boundary-alerts` | **Date**: 2026-02-14 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-geo-boundary-alerts/spec.md`

## Summary

Build Borderless as a native Android hackathon MVP that detects when users
cross Indian state boundaries and delivers importance-filtered legal,
cultural, and behavioral context alerts. The app features a Material
Design 3 multilingual dashboard and a live risk-rated Q&A powered by
Gemini API, all backed by a Node.js/Firebase serverless backend with
curated regional metadata for 4 Indian states (Karnataka, Delhi,
Maharashtra, Tamil Nadu).

## Technical Context

**Language/Version**: Kotlin 2.0+ (Android), Node.js 20+ (Backend)
**Primary Dependencies**:
- Android: Jetpack Compose, Material Design 3, Hilt, Compose Navigation,
  Google Play Services (Location, Geofencing), Firebase Android SDK
  (Auth, Firestore), Retrofit/OkHttp
- Backend: Firebase Cloud Functions, Firebase Admin SDK, Google AI SDK
  (Gemini 2.0 Flash), Express.js (within Cloud Functions)
**Storage**: Cloud Firestore (primary), Room (local Android cache)
**Testing**: JUnit 5 + Compose UI tests (Android), Jest (Node.js)
**Target Platform**: Android 10+ (API 29+) with Google Play Services
**Project Type**: Mobile + API (Android app + Firebase Cloud Functions)
**Performance Goals**: <10s boundary detection, <5s Q&A response, 60fps UI
**Constraints**: Hackathon timeline, offline-capable alerts, Gemini API
latency budget, 100 geofence limit per app
**Scale/Scope**: 4 Indian states, ~80 alert entries, single user demo,
6 API endpoints

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Modern Practices | PASS | Kotlin 2.0, Jetpack Compose, Material 3, Node.js 20, latest Firebase SDKs |
| II. Configuration-Driven | PASS | Geofences in Firestore (config), alert rules in JSON, API keys in .env, feature flags in config/ |
| III. Extensibility & Modularity | PASS | Feature-module Android architecture, Cloud Functions per-endpoint, region data addable via Firestore |
| IV. Quality-First Testing | PASS | JUnit for services, Compose UI tests for screens, Jest for Cloud Functions, contract tests for API |
| V. Non-Breaking Changes | PASS | First build — no existing functionality to break. Additive Firestore schema. Versioned API. |
| VI. Simplicity & Accessibility | PASS | MVVM architecture, single-activity, feature-folder structure, README per module |
| VII. Beautiful & Intuitive UX | PASS | Material Design 3, dynamic color, edge-to-edge, 48dp touch targets, dark mode, motion system |

**Gate result**: ALL PASS — proceed to implementation.

## Project Structure

### Documentation (this feature)

```text
specs/001-geo-boundary-alerts/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── api-contracts.md # REST API specifications
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
android/
├── app/
│   ├── src/main/
│   │   ├── java/com/borderless/app/
│   │   │   ├── di/                    # Hilt dependency injection modules
│   │   │   ├── data/
│   │   │   │   ├── local/             # Room database, DAOs
│   │   │   │   ├── remote/            # Retrofit API service, DTOs
│   │   │   │   └── repository/        # Repository implementations
│   │   │   ├── domain/
│   │   │   │   ├── model/             # Domain entities
│   │   │   │   ├── repository/        # Repository interfaces
│   │   │   │   └── usecase/           # Business logic use cases
│   │   │   ├── service/
│   │   │   │   ├── GeofenceService.kt # Foreground service for geofencing
│   │   │   │   └── NotificationHelper.kt
│   │   │   ├── ui/
│   │   │   │   ├── theme/             # Material 3 theme, colors, typography
│   │   │   │   ├── navigation/        # Compose Navigation graph
│   │   │   │   ├── onboarding/        # Sign-up screen
│   │   │   │   ├── dashboard/         # Dashboard screen + ViewModel
│   │   │   │   ├── alerts/            # Alert detail screen + ViewModel
│   │   │   │   ├── qa/                # Q&A screen + ViewModel
│   │   │   │   ├── history/           # Crossing history screen
│   │   │   │   ├── settings/          # Settings / language picker
│   │   │   │   └── components/        # Shared composables
│   │   │   └── BorderlessApp.kt       # Application class
│   │   └── res/
│   │       ├── values/                # Strings, themes, colors
│   │       └── values-hi/             # Hindi strings (demo)
│   └── src/test/                      # Unit tests
│   └── src/androidTest/               # UI / instrumented tests
├── build.gradle.kts
└── gradle/

backend/
├── functions/
│   ├── src/
│   │   ├── index.ts                   # Cloud Functions entry point
│   │   ├── routes/
│   │   │   ├── regions.ts             # GET /regions, GET /regions/:id/alerts
│   │   │   ├── qa.ts                  # POST /qa
│   │   │   ├── users.ts              # POST /users/profile
│   │   │   └── crossings.ts          # POST /crossings, GET /crossings
│   │   ├── services/
│   │   │   ├── gemini.ts             # Gemini API wrapper (Q&A, translate)
│   │   │   ├── firestore.ts          # Firestore data access
│   │   │   └── scoring.ts            # Alert importance scoring
│   │   ├── middleware/
│   │   │   └── auth.ts               # Firebase Auth token verification
│   │   ├── config/
│   │   │   └── regions.json          # Region geofence definitions
│   │   └── prompts/
│   │       ├── qa-system.txt         # Gemini system prompt for Q&A
│   │       └── translate-system.txt  # Gemini system prompt for translation
│   ├── seed/
│   │   ├── seed.ts                   # Database seeding script
│   │   └── data/
│   │       ├── karnataka.json        # Karnataka alert entries
│   │       ├── delhi.json            # Delhi alert entries
│   │       ├── maharashtra.json      # Maharashtra alert entries
│   │       └── tamil-nadu.json       # Tamil Nadu alert entries
│   ├── tests/
│   │   ├── routes/                   # API route tests
│   │   └── services/                 # Service unit tests
│   ├── package.json
│   ├── tsconfig.json
│   └── .env                          # Environment variables (gitignored)
├── firestore.rules
├── firestore.indexes.json
└── firebase.json

config/
├── features/
│   └── geofences.json                # Geofence definitions (copied to backend)
├── schemas/
│   ├── region.schema.json            # Region document schema
│   └── alert.schema.json             # Alert document schema
└── env/
    └── .env.example                  # Template for environment variables
```

**Structure Decision**: Mobile + API structure selected. Android app in
`android/` with clean architecture (data/domain/ui layers). Firebase Cloud
Functions backend in `backend/functions/` with TypeScript. Shared config
in `config/` at project root per constitution requirements.

## Architecture Overview

```text
┌─────────────────────────────────────────────────────┐
│                    ANDROID APP                       │
│                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │Onboarding│  │Dashboard │  │   Alert Detail    │  │
│  │  Screen  │  │  Screen  │  │     Screen        │  │
│  └────┬─────┘  └────┬─────┘  └────────┬─────────┘  │
│       │              │                 │             │
│  ┌────┴──────────────┴─────────────────┴──────────┐ │
│  │              ViewModels (MVVM)                  │ │
│  └────────────────────┬───────────────────────────┘ │
│                       │                             │
│  ┌────────────────────┴───────────────────────────┐ │
│  │              Use Cases (Domain)                 │ │
│  └──────┬─────────────┬──────────────┬────────────┘ │
│         │             │              │              │
│  ┌──────┴──────┐ ┌────┴────┐ ┌──────┴──────────┐   │
│  │ Geofence    │ │  Room   │ │ Retrofit API    │   │
│  │ Service     │ │  (local)│ │ (remote)        │   │
│  └──────┬──────┘ └─────────┘ └──────┬──────────┘   │
│         │                           │              │
└─────────┼───────────────────────────┼──────────────┘
          │                           │
  ┌───────┴────────┐    ┌─────────────┴──────────────┐
  │  Android GPS   │    │   Firebase Cloud Functions  │
  │  + Geofencing  │    │                            │
  │     API        │    │  ┌─────────┐ ┌──────────┐  │
  └────────────────┘    │  │ Routes  │ │ Gemini   │  │
                        │  │ (REST)  │ │ Service  │  │
                        │  └────┬────┘ └────┬─────┘  │
                        │       │           │        │
                        │  ┌────┴───────────┴─────┐  │
                        │  │     Firestore        │  │
                        │  │  (regions, alerts,   │  │
                        │  │   users, qaLogs)     │  │
                        │  └──────────────────────┘  │
                        └────────────────────────────┘
```

## Demo Data Flow

```text
1. USER crosses state boundary
   │
2. Android Geofencing API triggers BroadcastReceiver
   │
3. GeofenceService identifies target region from geofence ID
   │
4. GET /regions/:regionId/alerts → Cloud Function
   │  ├── Reads alerts from Firestore
   │  ├── Sorts by severity (critical first)
   │  └── Translates via Gemini if language ≠ en
   │
5. NotificationHelper posts Android system notification
   │  ├── Max 2 per boundary (check notification_state)
   │  └── Shows region name + critical alert count
   │
6. User TAPS notification → Alert Detail Screen
   │  └── Shows categorized alert cards (Legal/Cultural/Behavioral)
   │
7. User navigates to DASHBOARD
   │  ├── Region summary card (name, quick facts)
   │  ├── Alert count by category
   │  └── Recent crossing history (from Room)
   │
8. User opens Q&A, types question
   │
9. POST /qa → Cloud Function
   │  ├── Loads region alerts as context
   │  ├── Sends to Gemini with grounding prompt
   │  ├── Gemini returns answer + risk assessment
   │  └── Logs to qaLogs collection
   │
10. Q&A screen shows answer with risk badge + source citation
```

## Hackathon Trade-offs & Assumptions

| Decision | Trade-off | Rationale |
|----------|-----------|-----------|
| State-level geofencing only | No city-level granularity | Reduces geofence count; state crossings are more impactful |
| Circular geofences at borders | Not polygon-based | Android API supports circles natively; sufficient for highway corridors |
| Curated seed data | No live API integration | Demo reliability > real-time freshness for hackathon |
| Gemini Flash (not Pro) | Lower quality responses | 3x faster, 10x cheaper; quality sufficient for demo |
| Firebase anonymous → email link | No password management | Minimal friction; Firebase handles token refresh |
| Local notifications only | No FCM push | Eliminates server→device latency; geofence triggers are local |
| 4 Indian states | Not international | High contrast data available; avoids geopolitical complexity |
| Pre-generated translations cached | Not real-time translation for all | Reduces Gemini calls during demo; translate on first request then cache |
| Room for crossing history | Not synced to Firestore | Keeps history local and fast; server sync is post-hackathon |
| Simplified alert scoring | Rule-based severity, not ML | metadata.severity field is sufficient; Gemini adds context in Q&A only |

## Complexity Tracking

No constitution violations detected. All principles are satisfied with
the chosen architecture. No complexity justifications needed.

| Principle | Implementation | Compliant |
|-----------|---------------|-----------|
| Config-driven | Geofences in JSON, alerts in Firestore, keys in .env | Yes |
| Modular | Feature-module Android, per-route Cloud Functions | Yes |
| Testable | Use cases isolated from framework, API routes unit-testable | Yes |
| Non-breaking | First build, additive schema, versioned API | Yes |
| Beautiful UX | Material 3, dynamic color, edge-to-edge, animations | Yes |
