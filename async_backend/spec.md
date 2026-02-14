📄 Borderless – Hybrid Real-Time Context Intelligence Specification
1️⃣ System Philosophy
Borderless does not generate alerts purely based on current location.
It generates intelligence based on:

Context = f(previous_region, current_region, user_profile, validated_live_data)
The system detects context shifts, not just boundaries.

2️⃣ Architecture Overview
Layer 1 – Static Structured Metadata (Base Layer)
Stored in Firestore.

Contains:

Legal rules

Cultural norms

Behavioral notes

Language markers

Transport rules

Regional attributes (dry state, dominant language, etc.)

This layer:

Is manually curated

Does not depend on real-time fetch

Guarantees stability

Layer 2 – Scheduled Live Update Ingestion (Validation Layer)
Runs via backend cron (hourly or configurable).

Sources:

Government notifications

Police advisories

Verified news sources

Transport APIs

Festival APIs

Pipeline:

Fetch

Multi-source validation

Structured extraction (Gemini as parser)

Confidence scoring

TTL assignment

Store in live_updates collection

No user interaction required.

Layer 3 – Real-Time Transition Intelligence (Reasoning Layer)
Triggered only when:

User crosses region boundary

User enters special zone

User explicitly refreshes context

Backend receives:

{
  previous_region,
  current_region,
  user_profile,
  timestamp
}
3️⃣ Transition Classification Logic
System determines transition type:

A. State → State
Example: Delhi → Karnataka
Show:

Language shift

Legal differences

Cultural expectations

High-impact norms

Suppress:

Repeated universal info

B. City → City (Same State)
Example: Bangalore → Mysore
Show:

City-specific norms

Local advisories

Transport differences

Suppress:

State-level greeting

Already-known legal info

C. Region → Special Zone
Example: City → Temple
Show:

Dress code

Photography rules

Behavioral norms

Suppress:

State intro

General cultural notes

4️⃣ Data Storage Model
Collection: regions
{
  id,
  type: state | city | zone,
  parent_region,
  dominant_language,
  cultural_markers[],
  legal_rules[],
  behavioral_notes[]
}
Collection: live_updates
{
  id,
  region_id,
  category,
  severity,
  summary,
  source_links[],
  source_type,
  confidence_score,
  effective_from,
  expires_at,
  last_updated
}
Collection: user_sessions
{
  user_id,
  last_region,
  last_transition_type,
  last_alerts_shown[],
  last_update_timestamp
}
Used to prevent repetition.

5️⃣ Alert Generation Flow
Step 1 – Fetch Region Data
Static rules (current region)

Active live updates (not expired)

Previous region metadata

Step 2 – Compute Delta
Determine:

What is new?

What has changed?

What was already applicable?

Step 3 – Transition Reasoning (Gemini Prompt)
Gemini receives:

Previous region metadata

Current region metadata

Active live updates

User language preference

Recently shown alerts

Gemini must:

Identify meaningful differences

Suppress redundant info

Generate concise alert set

Assign severity category

Gemini is NOT allowed to invent new laws.

6️⃣ Real-Time Elements (Allowed at Trigger Time)
Allowed:

Weather API

Date-based festival API

Cached live updates

User profile preferences

Not allowed:

Raw news scraping

Long-running ingestion

Heavy validation processes

7️⃣ Alert Governance Rules
Max 2 proactive alerts per boundary.

No repetition within 24 hours.

Greeting shown only on state-level change.

If transition is within same cultural region → suppress intro.

High severity + high confidence → push notification.

Medium/low → dashboard only.

8️⃣ Confidence & Accuracy Model
Each live update must include:

Source weight

Multi-source validation

Expiry timestamp

Conflict detection result

Push threshold:

confidence_score ≥ 0.75
Below that:
→ Dashboard only.

9️⃣ Hackathon Constraints
For MVP:

3–4 states only.

Pre-curated dataset.

Limited ingestion sources.

Simplified confidence scoring.

Manual seeding allowed if APIs unreliable.

Deterministic demo flow preferred.

🔟 Performance Requirements
Boundary trigger → alert response under 2 seconds.

No ingestion at trigger time.

System must function even if ingestion layer fails.

Offline support via cached metadata.

1️⃣1️⃣ Key Differentiator
Borderless does not say:

“You are in Karnataka.”

It says:

“You have entered Karnataka from Delhi. Language norms, alcohol regulations, and temple etiquette differ. Here’s what’s new.”

That’s contextual intelligence.

If you want next, we can formalize this into:

A spec-kit compatible markdown version

Or convert it into engineering tickets

Or design the exact Gemini transition prompt template


Show less