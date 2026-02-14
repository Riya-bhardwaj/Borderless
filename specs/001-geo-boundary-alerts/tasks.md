# Tasks: Geo-Boundary Context Alerts

**Input**: Design documents from `/specs/001-geo-boundary-alerts/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Tests are included as the constitution mandates Quality-First Testing (Principle IV).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Android app**: `android/app/src/main/java/com/borderless/app/`
- **Backend**: `backend/functions/src/`
- **Config**: `config/`
- **Seed data**: `backend/functions/seed/data/`

---

## Phase 1: Setup

**Purpose**: Project initialization, tooling, and shared configuration

- [x] T001 Create Android project with Kotlin 2.0+, Jetpack Compose, Material 3, and Hilt in android/
- [x] T002 [P] Create Firebase Cloud Functions Node.js project with TypeScript in backend/functions/
- [x] T003 [P] Create config/ directory structure with config/features/geofences.json, config/schemas/region.schema.json, config/schemas/alert.schema.json, and config/env/.env.example
- [x] T004 [P] Configure Firebase project: enable Auth, Firestore, Cloud Functions; download google-services.json to android/app/
- [x] T005 [P] Configure Android build.gradle.kts with dependencies: Compose, Hilt, Retrofit, Room, Firebase SDK, Play Services Location
- [x] T006 [P] Configure backend package.json with dependencies: firebase-admin, firebase-functions, @google/generative-ai, express, cors
- [x] T007 Create Firestore security rules in backend/firestore.rules allowing authenticated read access to regions/alerts, user-scoped writes to users/qaLogs
- [x] T008 [P] Create Firestore composite indexes in backend/firestore.indexes.json for (regions: type+active), (alerts: active+severity), (qaLogs: userId+createdAt)
- [x] T009 Set up Android linting (ktlint) and backend linting (eslint + prettier) configuration files
- [x] T010 [P] Create .gitignore with entries for .env, google-services.json, local.properties, build/, node_modules/

**Checkpoint**: Both projects build and deploy successfully. Firebase connected.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T011 Create domain models: Region, AlertEntry, GeofenceDefinition, UserProfile, CrossingEvent, QaInteraction in android/app/src/main/java/com/borderless/app/domain/model/
- [x] T012 [P] Create Room database with BorderlessDatabase, CrossingHistoryEntity, NotificationStateEntity, and DAOs in android/app/src/main/java/com/borderless/app/data/local/
- [x] T013 [P] Create Retrofit API service interface (BorderlessApi) with all 6 endpoints and DTO classes in android/app/src/main/java/com/borderless/app/data/remote/
- [x] T014 [P] Create repository interfaces (RegionRepository, AlertRepository, UserRepository, CrossingRepository, QaRepository) in android/app/src/main/java/com/borderless/app/domain/repository/
- [x] T015 Create repository implementations in android/app/src/main/java/com/borderless/app/data/repository/ wiring Retrofit + Room + Firestore
- [x] T016 [P] Create Hilt modules (NetworkModule, DatabaseModule, RepositoryModule, FirebaseModule) in android/app/src/main/java/com/borderless/app/di/
- [x] T017 [P] Create Firebase Auth middleware for token verification in backend/functions/src/middleware/auth.ts
- [x] T018 [P] Create Firestore data access service in backend/functions/src/services/firestore.ts with methods: getRegions, getAlertsByRegion, getUser, createUser, updateUser, logCrossing, getCrossings, logQa
- [x] T019 Create Express.js app setup with CORS, JSON parsing, and auth middleware in backend/functions/src/index.ts
- [x] T020 [P] Create Material 3 theme (colors, typography, shapes) with dynamic color support and dark mode in android/app/src/main/java/com/borderless/app/ui/theme/
- [x] T021 [P] Create shared UI components (AlertCard, SeverityBadge, RiskRatingChip, RegionSummaryCard, LoadingState, EmptyState, ErrorState) in android/app/src/main/java/com/borderless/app/ui/components/
- [x] T022 Create Compose Navigation graph with routes: Onboarding, Dashboard, AlertDetail, QA, History, Settings in android/app/src/main/java/com/borderless/app/ui/navigation/
- [x] T023 Create Application class (BorderlessApp) with Hilt setup in android/app/src/main/java/com/borderless/app/BorderlessApp.kt
- [x] T024 [P] Create seed data JSON files for 4 states: backend/functions/seed/data/karnataka.json (20 alerts), delhi.json (22 alerts), maharashtra.json (18 alerts), tamil-nadu.json (20 alerts)
- [x] T025 Create database seeding script in backend/functions/seed/seed.ts that populates Firestore regions collection and alerts subcollections from JSON files
- [x] T026 Run seed script to populate Firestore with 4 states, 4 cities, and ~80 alert entries

**Checkpoint**: Foundation ready — Android builds with navigation shell, backend deploys with seeded data, all repositories wired.

---

## Phase 3: User Story 1 — Boundary Crossing Detection & Alerts (Priority: P1) MVP

**Goal**: Detect state boundary crossings and deliver severity-sorted context alerts via notification + in-app detail view

**Independent Test**: Simulate GPS location change from Mumbai to Bangalore → verify notification appears within 10s → tap to see categorized alerts sorted by severity

### Tests for User Story 1

- [x] T027 [P] [US1] Write unit tests for GeofenceService boundary detection logic in android/app/src/test/java/com/borderless/app/service/GeofenceServiceTest.kt
- [x] T028 [P] [US1] Write unit tests for alert scoring/sorting service in backend/functions/tests/services/scoring.test.ts
- [x] T029 [P] [US1] Write API route tests for GET /regions and GET /regions/:id/alerts in backend/functions/tests/routes/regions.test.ts

### Implementation for User Story 1

- [x] T030 [US1] Create alert importance scoring service with rule-based severity sorting (critical>important>informational) in backend/functions/src/services/scoring.ts
- [x] T031 [P] [US1] Create GET /regions route returning all active regions with geofence definitions in backend/functions/src/routes/regions.ts
- [x] T032 [US1] Create GET /regions/:regionId/alerts route returning severity-sorted alerts with optional language translation in backend/functions/src/routes/regions.ts
- [x] T033 [US1] Create GeofenceBroadcastReceiver to handle geofence transition events in android/app/src/main/java/com/borderless/app/service/GeofenceBroadcastReceiver.kt
- [x] T034 [US1] Create GeofenceService foreground service that registers geofences from API response and monitors transitions in android/app/src/main/java/com/borderless/app/service/GeofenceService.kt
- [x] T035 [US1] Create NotificationHelper with notification channel setup, alert notification builder (shows region name + critical count), and suppression logic (max 2 per boundary, 24h window) in android/app/src/main/java/com/borderless/app/service/NotificationHelper.kt
- [x] T036 [US1] Create GetAlertsForRegionUseCase that fetches alerts from API, applies user severity filters, and caches to Room in android/app/src/main/java/com/borderless/app/domain/usecase/GetAlertsForRegionUseCase.kt
- [x] T037 [US1] Create RegisterGeofencesUseCase that loads regions from API and registers circular geofences with Play Services in android/app/src/main/java/com/borderless/app/domain/usecase/RegisterGeofencesUseCase.kt
- [x] T038 [US1] Create AlertDetailViewModel managing alert list state, severity filtering, and "View All" toggle in android/app/src/main/java/com/borderless/app/ui/alerts/AlertDetailViewModel.kt
- [x] T039 [US1] Create AlertDetailScreen with categorized alert cards (Legal/Cultural/Behavioral sections), severity badges, and expand/collapse animation in android/app/src/main/java/com/borderless/app/ui/alerts/AlertDetailScreen.kt
- [x] T040 [US1] Wire notification tap deep link to AlertDetailScreen via Compose Navigation in android/app/src/main/java/com/borderless/app/ui/navigation/
- [x] T041 [US1] Add location permission request flow with rationale dialog and manual region selection fallback in android/app/src/main/java/com/borderless/app/ui/onboarding/
- [x] T042 [US1] Add AndroidManifest.xml entries: foreground service declaration, location permissions (fine + background), RECEIVE_BOOT_COMPLETED, geofence receiver

**Checkpoint**: User Story 1 fully functional — boundary crossing triggers notification, tap opens alert detail with sorted alerts.

---

## Phase 4: User Story 2 — Multilingual Dashboard (Priority: P2)

**Goal**: Display region summary, active alerts count, crossing history, and support dynamic language switching via Gemini translation

**Independent Test**: Open dashboard → see current region card with quick facts and alert counts → switch language to Hindi → verify all content translates without restart

### Tests for User Story 2

- [x] T043 [P] [US2] Write unit tests for Gemini translation service in backend/functions/tests/services/gemini.test.ts
- [x] T044 [P] [US2] Write unit tests for DashboardViewModel state management in android/app/src/test/java/com/borderless/app/ui/dashboard/DashboardViewModelTest.kt

### Implementation for User Story 2

- [x] T045 [US2] Create Gemini API wrapper service with translation prompt template in backend/functions/src/services/gemini.ts
- [x] T046 [US2] Create Gemini system prompt for translation in backend/functions/src/prompts/translate-system.txt
- [x] T047 [US2] Add translation support to GET /regions/:id/alerts route — when language param ≠ en, batch-translate alert titles and descriptions via Gemini in backend/functions/src/routes/regions.ts
- [x] T048 [US2] Create DashboardViewModel managing current region state, alert counts by category, crossing history, and language preference in android/app/src/main/java/com/borderless/app/ui/dashboard/DashboardViewModel.kt
- [x] T049 [US2] Create DashboardScreen with region summary card (name, quick facts), alert count chips by category (Legal/Cultural/Behavioral), and recent crossings list in android/app/src/main/java/com/borderless/app/ui/dashboard/DashboardScreen.kt
- [x] T050 [US2] Create SettingsScreen with language picker dropdown and alert filter toggles in android/app/src/main/java/com/borderless/app/ui/settings/SettingsScreen.kt
- [x] T051 [US2] Create SettingsViewModel managing language selection and persisting to UserProfile via POST /users/profile in android/app/src/main/java/com/borderless/app/ui/settings/SettingsViewModel.kt
- [x] T052 [US2] Create Android string resources for English (values/strings.xml) and Hindi demo (values-hi/strings.xml) covering all UI chrome labels
- [x] T053 [US2] Implement live language switching — observe language preference changes in DashboardViewModel, re-fetch translated content from API without activity restart
- [x] T054 [US2] Create CrossingHistoryScreen showing chronological list of boundary crossings with from/to region names and timestamps in android/app/src/main/java/com/borderless/app/ui/history/CrossingHistoryScreen.kt
- [x] T055 [US2] Wire bottom navigation bar with Dashboard, Q&A, History, and Settings tabs following Material 3 NavigationBar pattern

**Checkpoint**: Dashboard shows region info and alerts, language switching works end-to-end, crossing history displays.

---

## Phase 5: User Story 3 — Live Risk-Rated Q&A (Priority: P3)

**Goal**: Users ask free-text questions about the current region and receive Gemini-grounded answers with risk ratings and source citations

**Independent Test**: Open Q&A in Karnataka → type "Can I drink tap water in Bangalore?" → verify answer appears within 5s with risk rating badge and source citation

### Tests for User Story 3

- [x] T056 [P] [US3] Write unit tests for Q&A Gemini grounding service in backend/functions/tests/services/gemini.test.ts
- [x] T057 [P] [US3] Write API route tests for POST /qa in backend/functions/tests/routes/qa.test.ts

### Implementation for User Story 3

- [x] T058 [US3] Create Gemini Q&A system prompt with grounding instructions, risk rating rubric, and citation format in backend/functions/src/prompts/qa-system.txt
- [x] T059 [US3] Add Q&A method to Gemini service: accept question + region alerts context, return structured answer with riskRating and sources in backend/functions/src/services/gemini.ts
- [x] T060 [US3] Create POST /qa route that loads region alerts as grounding context, calls Gemini Q&A, logs interaction to qaLogs collection in backend/functions/src/routes/qa.ts
- [x] T061 [US3] Create AskQuestionUseCase that sends question to POST /qa API with current region and language in android/app/src/main/java/com/borderless/app/domain/usecase/AskQuestionUseCase.kt
- [x] T062 [US3] Create QaViewModel managing question input, loading state, answer display, and thumbs-up/down feedback in android/app/src/main/java/com/borderless/app/ui/qa/QaViewModel.kt
- [x] T063 [US3] Create QaScreen with text input field, send button, answer card (with risk rating badge, source citation list), and feedback thumbs in android/app/src/main/java/com/borderless/app/ui/qa/QaScreen.kt
- [x] T064 [US3] Add Q&A offline handling — show "Requires internet connection" message with retry button when network unavailable
- [x] T065 [US3] Add Q&A answer translation — pass user's language preference to POST /qa so Gemini responds in the correct language

**Checkpoint**: Q&A returns grounded answers with risk ratings, sources cited, feedback collected.

---

## Phase 6: User Story 4 — Regional Metadata Management (Priority: P4)

**Goal**: Seed script and Firestore-based metadata management for curated alert entries (admin via Firebase Console for hackathon)

**Independent Test**: Add a new alert entry to Firestore via seed script → trigger sync on device → verify new alert appears in the region's alert list

### Implementation for User Story 4

- [x] T066 [US4] Create POST /users/profile route for user sign-up and preference updates in backend/functions/src/routes/users.ts
- [x] T067 [US4] Create POST /crossings and GET /crossings routes for crossing event logging and history retrieval in backend/functions/src/routes/crossings.ts
- [x] T068 [US4] Create OnboardingViewModel managing sign-up form state (name, language, filters) and profile creation via POST /users/profile in android/app/src/main/java/com/borderless/app/ui/onboarding/OnboardingViewModel.kt
- [x] T069 [US4] Create OnboardingScreen with name input, language selector, alert filter toggles, and "Get Started" button with smooth transition animation in android/app/src/main/java/com/borderless/app/ui/onboarding/OnboardingScreen.kt
- [x] T070 [US4] Add metadata refresh logic — on app open, fetch regions and check for updated alerts via GET /regions, update local cache if newer data available
- [x] T071 [US4] Add seed script enhancement: accept --update flag to add new entries without overwriting existing data in backend/functions/seed/seed.ts

**Checkpoint**: Sign-up flow works, metadata refreshes on app open, seed script supports incremental updates.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: UI polish, edge cases, animations, and demo preparation

- [x] T072 [P] Add Material 3 motion system: shared element transitions between alert list and detail, fade-through for navigation, container transforms for cards in android/app/src/main/java/com/borderless/app/ui/theme/
- [x] T073 [P] Add edge-to-edge content display with proper inset handling for all screens
- [x] T074 [P] Add loading shimmer effects for dashboard region card and alert list loading states
- [x] T075 Add notification batching for rapid boundary crossings — debounce geofence events within 30-second window, deliver most recent region alerts only
- [x] T076 Add offline fallback — detect network state, show cached alerts when offline, display "Last updated X ago" indicator on dashboard
- [x] T077 [P] Add manual region selection picker as fallback when location permissions denied — dropdown of available states on dashboard
- [x] T078 Run full demo walkthrough per quickstart.md: sign-up → mock location → boundary crossing → notification → alert detail → dashboard → Q&A → language switch
- [x] T079 [P] Add README.md files at project root, android/, and backend/ with setup instructions and architecture overview
- [x] T080 Final validation: verify all acceptance scenarios from spec.md pass, all constitution principles satisfied

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - US1 (P1): Can start after Foundational — no dependencies on other stories
  - US2 (P2): Can start after Foundational — uses alert APIs from US1 backend routes
  - US3 (P3): Depends on Gemini service from US2 (T045) — can start backend in parallel
  - US4 (P4): Can start after Foundational — independent user/crossing routes
- **Polish (Phase 7)**: Depends on all user stories being complete

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Backend routes before Android use cases
- Use cases before ViewModels
- ViewModels before Screens
- Core implementation before integration

### Parallel Opportunities

Setup phase:
```
T001 (Android project) | T002 (Backend project) | T003 (Config)
T004 (Firebase) | T005 (Android deps) | T006 (Backend deps) | T010 (.gitignore)
```

Foundational phase:
```
T011 (Domain models) → T012 (Room) | T013 (Retrofit) | T014 (Repos)
T017 (Auth middleware) | T018 (Firestore service) | T020 (Theme) | T021 (Components)
T024 (Seed data) → T025 (Seed script) → T026 (Run seed)
```

User stories (after foundational):
```
US1 backend: T030 → T031 | T032
US1 android: T033 → T034 → T035 → T036 | T037 → T038 → T039 → T040
US2 can start backend (T045-T047) while US1 android is in progress
US4 backend routes (T066-T067) can run in parallel with US1/US2
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Mock location crossing → notification → alert detail
5. Demo-ready with core value proposition

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. User Story 1 → Boundary crossing + alerts working (MVP!)
3. User Story 2 → Dashboard + multilingual support
4. User Story 3 → Q&A with Gemini grounding
5. User Story 4 → Sign-up flow + metadata management
6. Polish → Animations, edge cases, demo prep

### Hackathon Sprint Plan

With 1-2 developers over a hackathon weekend:

**Day 1 Morning**: Phase 1 (Setup) + Phase 2 (Foundational) + Seed data
**Day 1 Afternoon**: Phase 3 (US1 — Boundary Crossing) — core demo flow
**Day 1 Evening**: Phase 4 (US2 — Dashboard + Language) — visual polish
**Day 2 Morning**: Phase 5 (US3 — Q&A) + Phase 6 (US4 — Onboarding)
**Day 2 Afternoon**: Phase 7 (Polish) + Demo rehearsal

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Tests MUST fail before implementing corresponding feature
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Total seed data: ~80 alert entries across 4 Indian states
- Gemini API key required for US2 (translation) and US3 (Q&A)
