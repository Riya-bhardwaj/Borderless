# Research: Geo-Boundary Context Alerts

**Branch**: `001-geo-boundary-alerts`
**Date**: 2026-02-14

## R1: Android Geofencing for State-Level Boundaries

**Decision**: Use Android Geofencing API with predefined circular
geofences at state boundary entry points, combined with reverse geocoding
for precise state detection.

**Rationale**: Android's Geofencing API supports up to 100 geofences per
app and handles background monitoring with minimal battery impact. For
hackathon scope (3-4 Indian states), we only need ~10-15 geofences.
Circular geofences at border crossing corridors (highways, rail routes)
are sufficient. Reverse geocoding via Android's Geocoder class confirms
exact state after geofence trigger.

**Alternatives considered**:
- Polygon-based geofencing (too complex for hackathon; requires custom
  point-in-polygon math)
- Continuous GPS polling (battery drain, unnecessary for state-level)
- Third-party geofencing SDKs (additional dependency, overkill for MVP)

## R2: Firebase Stack for Backend

**Decision**: Firebase Authentication (anonymous + email sign-up),
Cloud Firestore for metadata storage, Cloud Functions for Node.js API
endpoints.

**Rationale**: Firebase provides a complete serverless backend that
eliminates infrastructure setup. Firestore's real-time listeners enable
instant metadata sync. Cloud Functions run Node.js natively, matching the
backend requirement. Anonymous auth allows instant onboarding; users can
optionally link email later. Free tier covers hackathon demo load.

**Alternatives considered**:
- Express.js on a VPS (requires server setup, deployment pipeline)
- Supabase (PostgreSQL-based, less natural for document-oriented metadata)
- AWS Amplify (more complex setup, steeper learning curve)

## R3: Gemini API Integration Strategy

**Decision**: Use Gemini 2.0 Flash via Google AI SDK for Node.js.
Three distinct prompt templates: alert summarization, Q&A grounding,
and translation. Hybrid scoring: rule-based severity from metadata +
Gemini for contextual importance.

**Rationale**: Gemini 2.0 Flash offers the best latency/cost ratio for
hackathon. Structured prompts with system instructions ensure grounded
responses. Rule-based severity (Critical/Important/Informational from
metadata) avoids Gemini latency for basic classification. Gemini handles
nuanced tasks: Q&A, translation, and contextual summarization.

**Alternatives considered**:
- Gemini Pro (higher latency, unnecessary quality for MVP)
- Full Gemini scoring for all alerts (too slow, too expensive)
- OpenAI GPT (not aligned with Google/Firebase ecosystem)

## R4: Regional Metadata Structure (Indian States)

**Decision**: Curate metadata for 4 Indian states: Karnataka (Bangalore),
Delhi (NCR), Maharashtra (Mumbai), and Tamil Nadu (Chennai). Each state
gets 15-25 alert entries across Legal, Cultural, and Behavioral
categories. Store as Firestore documents with flat structure for fast
queries.

**Rationale**: These states offer high contrast in laws, culture, and
language — ideal for demo impact. Example contrasts: Delhi's pollution
laws vs Karnataka's tech hub norms, Tamil Nadu's language politics vs
Maharashtra's food regulations. 15-25 entries per state provide enough
variety without requiring days of curation.

**Alternatives considered**:
- International countries (harder to verify accuracy for hackathon)
- Fewer states (less impressive demo)
- Auto-generated metadata via Gemini (risk of hallucination in legal data)

## R5: Android UI Architecture

**Decision**: Jetpack Compose with Material Design 3, single-activity
architecture with Compose Navigation. MVVM with Hilt dependency
injection. StateFlow for reactive UI state.

**Rationale**: Jetpack Compose is the modern Android UI toolkit, aligns
with Constitution Principle I (Modern Practices) and VII (Beautiful UX).
Material Design 3 provides dynamic color theming out of the box. MVVM
with Hilt is the standard Android architecture pattern. Single-activity
with Compose Navigation simplifies the navigation graph.

**Alternatives considered**:
- XML layouts with Fragments (outdated, more boilerplate)
- Compose without Hilt (manual DI is error-prone)
- MVI pattern (overkill for hackathon scope)

## R6: Notification Strategy

**Decision**: Use Android NotificationManager with a dedicated
notification channel for boundary alerts. Foreground service for
geofence monitoring. Max 2 notifications per boundary crossing, 24-hour
suppression for repeated crossings of the same boundary.

**Rationale**: Android requires notification channels (API 26+). A
foreground service ensures geofence monitoring survives background
restrictions (Doze mode). Notification governance (max 2, 24h
suppression) prevents alert fatigue during demo. FCM is unnecessary
for hackathon — local notifications from geofence triggers are
sufficient and avoid backend round-trips.

**Alternatives considered**:
- FCM push notifications (requires server round-trip, adds latency)
- WorkManager for geofences (less reliable than foreground service)
- No notification limits (alert fatigue during demo)

## R7: Offline Caching Strategy

**Decision**: Firestore offline persistence (built-in) for metadata
cache. Room database for crossing history and user preferences. Cache
metadata on first sync per region; TTL of 3 hours for high-risk, 24
hours for cultural/behavioral.

**Rationale**: Firestore's built-in offline mode caches all read
documents automatically — zero additional code. Room handles structured
local data (crossing logs, preferences) with compile-time SQL
verification. Dual-cache approach means alerts work offline while
Q&A gracefully degrades with a "requires internet" message.

**Alternatives considered**:
- Room for everything (requires manual sync logic)
- SharedPreferences (not suitable for structured data)
- DataStore (good for preferences, not for complex queries)

## R8: Demo Data Flow

**Decision**: Seed Firestore with curated metadata at deploy time via
a Node.js seed script. Demo flow: Mock location change → Geofence
trigger → Local notification → Tap to open alert detail → Dashboard
shows region card → Q&A sends query to Cloud Function → Gemini
generates grounded response.

**Rationale**: Seeded data ensures demo reliability regardless of
external API availability. Mock location (Android developer options)
allows reproducible boundary crossings during demo without physically
traveling. End-to-end flow touches all 4 user stories in under 60
seconds.

**Alternatives considered**:
- Live API fetch during demo (risky if APIs fail)
- Emulator-only demo (less impressive than real device)
- Pre-recorded video fallback (not interactive)
