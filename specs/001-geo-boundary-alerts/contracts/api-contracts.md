# API Contracts: Geo-Boundary Context Alerts

**Branch**: `001-geo-boundary-alerts`
**Date**: 2026-02-14
**Base URL**: Cloud Functions — `https://<region>-<project>.cloudfunctions.net/api`

## Authentication

All endpoints require Firebase Auth ID token in the Authorization header:
```
Authorization: Bearer <firebase-id-token>
```

---

## 1. GET /regions

Retrieve all active regions with geofence definitions.

**Purpose**: App loads geofences on startup and after sync.

**Request**: No parameters.

**Response** `200 OK`:
```json
{
  "regions": [
    {
      "id": "karnataka",
      "name": "Karnataka",
      "type": "state",
      "parentId": "india",
      "geofences": [
        {
          "lat": 14.9506,
          "lng": 74.2179,
          "radiusMeters": 5000,
          "label": "Goa-Karnataka Border NH66"
        }
      ],
      "quickFacts": [
        "Kannada is the official language",
        "Helmet mandatory for two-wheelers"
      ],
      "alertCount": 20
    }
  ],
  "lastUpdated": "2026-02-14T10:00:00Z"
}
```

**Error responses**:
- `401 Unauthorized` — missing or invalid auth token
- `500 Internal Server Error` — Firestore read failure

---

## 2. GET /regions/:regionId/alerts

Retrieve alerts for a specific region, sorted by severity.

**Purpose**: Called when a boundary crossing is detected.

**Path parameters**:
- `regionId` (string, required) — the region ID

**Query parameters**:
- `language` (string, optional) — target language code (default: `en`).
  If non-English, alerts are translated via Gemini before response.
- `severity` (string, optional) — filter: `critical`, `important`,
  `informational`, or `all` (default: `all`)

**Response** `200 OK`:
```json
{
  "regionId": "karnataka",
  "regionName": "Karnataka",
  "alerts": [
    {
      "id": "ka-legal-001",
      "category": "legal",
      "severity": "critical",
      "title": "Plastic ban enforced",
      "description": "Karnataka has a strict ban on single-use plastics...",
      "source": "Karnataka State Pollution Control Board, 2024",
      "tags": ["plastic", "ban", "fine"]
    },
    {
      "id": "ka-cultural-001",
      "category": "cultural",
      "severity": "important",
      "title": "Temple dress code",
      "description": "Most temples require modest clothing...",
      "source": "Karnataka Tourism Board",
      "tags": ["temple", "dress", "culture"]
    }
  ],
  "totalCount": 20,
  "language": "en"
}
```

**Error responses**:
- `401 Unauthorized`
- `404 Not Found` — region ID does not exist
- `500 Internal Server Error`

---

## 3. POST /qa

Submit a Q&A question grounded in regional metadata.

**Purpose**: User asks a free-text question about the current region.

**Request body**:
```json
{
  "regionId": "karnataka",
  "question": "Can I drink tap water in Bangalore?",
  "language": "en"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `regionId` | string | yes | Current region context |
| `question` | string | yes | User's question (max 500 chars) |
| `language` | string | no | Response language (default: `en`) |

**Response** `200 OK`:
```json
{
  "answer": "Tap water in Bangalore is generally not recommended for drinking without filtering or boiling. Most locals and visitors use filtered or bottled water.",
  "riskRating": "high",
  "sources": [
    {
      "alertId": "ka-behavioral-003",
      "title": "Drinking water safety",
      "source": "WHO India Water Quality Report, 2025"
    }
  ],
  "language": "en",
  "responseTimeMs": 2340
}
```

**Risk rating logic**:
- `critical` — legal violation risk (fines, arrest)
- `high` — health or safety risk
- `medium` — social discomfort or cultural misstep
- `low` — general information, no risk

**Error responses**:
- `400 Bad Request` — missing required fields or question too long
- `401 Unauthorized`
- `404 Not Found` — region ID does not exist
- `503 Service Unavailable` — Gemini API timeout or failure

---

## 4. POST /users/profile

Create or update user profile and preferences.

**Purpose**: Simple sign-up and preference management.

**Request body**:
```json
{
  "displayName": "Riya",
  "language": "en",
  "alertFilters": {
    "critical": true,
    "important": true,
    "informational": false
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `displayName` | string | yes | User's name |
| `language` | string | no | Preferred language code (default: `en`) |
| `alertFilters` | object | no | Severity filter preferences |

**Response** `200 OK`:
```json
{
  "uid": "firebase-uid-123",
  "displayName": "Riya",
  "language": "en",
  "alertFilters": {
    "critical": true,
    "important": true,
    "informational": false
  },
  "createdAt": "2026-02-14T10:00:00Z",
  "updatedAt": "2026-02-14T10:00:00Z"
}
```

**Error responses**:
- `400 Bad Request` — missing displayName
- `401 Unauthorized`

---

## 5. POST /crossings

Log a boundary crossing event.

**Purpose**: Record crossing for user history and analytics.

**Request body**:
```json
{
  "fromRegionId": "maharashtra",
  "toRegionId": "karnataka",
  "latitude": 14.9506,
  "longitude": 74.2179,
  "alertsDelivered": 5
}
```

**Response** `201 Created`:
```json
{
  "id": "crossing-uuid-456",
  "fromRegionId": "maharashtra",
  "toRegionId": "karnataka",
  "alertsDelivered": 5,
  "timestamp": "2026-02-14T15:30:00Z"
}
```

**Error responses**:
- `400 Bad Request` — missing required fields
- `401 Unauthorized`

---

## 6. GET /crossings

Retrieve crossing history for the authenticated user.

**Purpose**: Dashboard crossing history display.

**Query parameters**:
- `limit` (integer, optional) — max results (default: 20, max: 100)

**Response** `200 OK`:
```json
{
  "crossings": [
    {
      "id": "crossing-uuid-456",
      "fromRegion": {"id": "maharashtra", "name": "Maharashtra"},
      "toRegion": {"id": "karnataka", "name": "Karnataka"},
      "alertsDelivered": 5,
      "timestamp": "2026-02-14T15:30:00Z"
    }
  ],
  "total": 1
}
```

---

## Endpoint Summary

| Method | Path | Purpose | Gemini? |
|--------|------|---------|---------|
| GET | `/regions` | Load geofences + region list | No |
| GET | `/regions/:id/alerts` | Get alerts for region | Yes (translation) |
| POST | `/qa` | Ask grounded question | Yes (Q&A + translation) |
| POST | `/users/profile` | Create/update profile | No |
| POST | `/crossings` | Log crossing event | No |
| GET | `/crossings` | Get crossing history | No |

**Total**: 6 endpoints — minimal surface area for hackathon.
