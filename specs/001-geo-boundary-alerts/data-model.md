# Data Model: Geo-Boundary Context Alerts

**Branch**: `001-geo-boundary-alerts`
**Date**: 2026-02-14

## Overview

Two storage systems:
1. **Firestore** (cloud) — regions, alert entries, Q&A logs, user profiles
2. **Room** (local Android) — crossing history, cached preferences, notification state

## Firestore Collections

### `regions`

Top-level collection. One document per geographic region.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Auto-generated document ID |
| `name` | string | Region display name (English) |
| `type` | string | Enum: `country`, `state`, `city` |
| `parentId` | string | null | Reference to parent region (e.g., state → country) |
| `geofences` | array<map> | List of geofence definitions for this region |
| `geofences[].lat` | number | Center latitude |
| `geofences[].lng` | number | Center longitude |
| `geofences[].radiusMeters` | number | Geofence radius in meters |
| `geofences[].label` | string | Human-readable label (e.g., "NH48 Karnataka Entry") |
| `quickFacts` | array<string> | 3-5 short facts for dashboard display |
| `active` | boolean | Whether this region is active for alerts |
| `updatedAt` | timestamp | Last modification timestamp |

**Example document**:
```json
{
  "id": "karnataka",
  "name": "Karnataka",
  "type": "state",
  "parentId": "india",
  "geofences": [
    {"lat": 14.9506, "lng": 74.2179, "radiusMeters": 5000, "label": "Goa-Karnataka Border NH66"},
    {"lat": 12.2586, "lng": 77.0046, "radiusMeters": 5000, "label": "TN-Karnataka Border NH44"}
  ],
  "quickFacts": [
    "Kannada is the official language",
    "Alcohol sale restricted on dry days",
    "Helmet mandatory for two-wheelers"
  ],
  "active": true,
  "updatedAt": "2026-02-14T10:00:00Z"
}
```

### `regions/{regionId}/alerts` (subcollection)

Alert entries tied to a specific region.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Auto-generated document ID |
| `category` | string | Enum: `legal`, `cultural`, `behavioral` |
| `severity` | string | Enum: `critical`, `important`, `informational` |
| `title` | string | Short alert title (English, source language) |
| `description` | string | Detailed alert description (English) |
| `source` | string | Citation / data source |
| `effectiveDate` | timestamp | When alert becomes active |
| `expiryDate` | timestamp | null | When alert expires (null = no expiry) |
| `tags` | array<string> | Searchable tags for Q&A matching |
| `active` | boolean | Computed from effectiveDate/expiryDate |
| `updatedAt` | timestamp | Last modification timestamp |

**Severity sort order**: `critical` = 0, `important` = 1, `informational` = 2

**Example document**:
```json
{
  "id": "ka-legal-001",
  "category": "legal",
  "severity": "critical",
  "title": "Plastic ban enforced",
  "description": "Karnataka has a strict ban on single-use plastics. Carrying plastic bags can result in fines up to ₹500 for first offense.",
  "source": "Karnataka State Pollution Control Board, 2024",
  "effectiveDate": "2024-01-01T00:00:00Z",
  "expiryDate": null,
  "tags": ["plastic", "ban", "fine", "environment"],
  "active": true,
  "updatedAt": "2026-02-14T10:00:00Z"
}
```

### `users`

User profile documents.

| Field | Type | Description |
|-------|------|-------------|
| `uid` | string | Firebase Auth UID (document ID) |
| `displayName` | string | User's display name |
| `language` | string | Preferred language code (e.g., `en`, `hi`, `ta`) |
| `alertFilters` | map | Severity filter preferences |
| `alertFilters.critical` | boolean | Show critical alerts (default: true) |
| `alertFilters.important` | boolean | Show important alerts (default: true) |
| `alertFilters.informational` | boolean | Show informational (default: true) |
| `currentRegionId` | string | null | Last detected region |
| `createdAt` | timestamp | Account creation time |
| `updatedAt` | timestamp | Last profile update |

### `qaLogs`

Q&A interaction records (for analytics, not shown to other users).

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Auto-generated |
| `userId` | string | Firebase Auth UID |
| `regionId` | string | Region context for the question |
| `question` | string | User's question text |
| `answer` | string | Gemini-generated response |
| `riskRating` | string | Enum: `low`, `medium`, `high`, `critical` |
| `sources` | array<string> | Alert IDs used as grounding |
| `language` | string | Response language |
| `responseTimeMs` | number | Response latency in milliseconds |
| `feedback` | string | null | Enum: `helpful`, `not_helpful`, null |
| `createdAt` | timestamp | Interaction timestamp |

## Room Database (Local Android)

### `crossing_history` table

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PK | Auto-increment |
| `from_region_id` | TEXT | Origin region ID |
| `from_region_name` | TEXT | Origin region name (denormalized) |
| `to_region_id` | TEXT | Destination region ID |
| `to_region_name` | TEXT | Destination region name (denormalized) |
| `latitude` | REAL | GPS latitude at crossing |
| `longitude` | REAL | GPS longitude at crossing |
| `alert_count` | INTEGER | Number of alerts delivered |
| `timestamp` | INTEGER | Unix epoch milliseconds |

### `notification_state` table

| Column | Type | Description |
|--------|------|-------------|
| `region_id` | TEXT PK | Region ID |
| `last_notified_at` | INTEGER | Unix epoch ms of last notification |
| `notification_count` | INTEGER | Count within suppression window |

**Suppression logic**: If `notification_count >= 2` AND
`now - last_notified_at < 24 hours`, suppress notification.

## Entity Relationships

```text
india (region, type=country)
├── karnataka (region, type=state, parentId=india)
│   ├── bangalore (region, type=city, parentId=karnataka)
│   ├── alerts/ (subcollection)
│   │   ├── ka-legal-001 (plastic ban)
│   │   ├── ka-cultural-001 (festival customs)
│   │   └── ka-behavioral-001 (tipping norms)
│   └── geofences: [{border points}]
├── delhi (region, type=state, parentId=india)
│   ├── new-delhi (region, type=city, parentId=delhi)
│   └── alerts/ ...
├── maharashtra (region, type=state, parentId=india)
│   ├── mumbai (region, type=city, parentId=maharashtra)
│   └── alerts/ ...
└── tamil-nadu (region, type=state, parentId=india)
    ├── chennai (region, type=city, parentId=tamil-nadu)
    └── alerts/ ...

users/{uid}
├── displayName, language, alertFilters
└── currentRegionId → references regions/{id}

qaLogs/{id}
├── userId → references users/{uid}
├── regionId → references regions/{id}
└── sources[] → references regions/{regionId}/alerts/{alertId}

crossing_history (Room, local)
├── from_region_id → regions/{id}
└── to_region_id → references regions/{id}
```

## Indexes Required (Firestore)

1. `regions` — composite index on `(type, active)` for filtered queries
2. `regions/{id}/alerts` — composite index on `(active, severity)` for
   sorted alert retrieval
3. `qaLogs` — composite index on `(userId, createdAt)` for user history

## Hackathon Seed Data Summary

| State | Cities | Alert Count | Categories |
|-------|--------|-------------|------------|
| Karnataka | Bangalore | 20 | 7 legal, 8 cultural, 5 behavioral |
| Delhi | New Delhi | 22 | 9 legal, 7 cultural, 6 behavioral |
| Maharashtra | Mumbai | 18 | 6 legal, 7 cultural, 5 behavioral |
| Tamil Nadu | Chennai | 20 | 7 legal, 8 cultural, 5 behavioral |
| **Total** | **4 cities** | **80** | **29 legal, 30 cultural, 21 behavioral** |
