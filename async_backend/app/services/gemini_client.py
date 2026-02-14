import json
import logging
import uuid
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

_SYSTEM_INSTRUCTION = (
    "You are a cultural travel companion for India. When someone crosses a "
    "regional boundary, provide 3-4 short, warm, actionable tips about the "
    "new place. Focus on:\n"
    "- Local greetings and useful phrases (transliterated, not just in script)\n"
    "- Cultural and regional practices unique to the destination\n"
    "- Food, customs, and daily-life differences compared to where they came from\n"
    "- Seasonal or time-of-day relevant tips\n\n"
    "Be specific, practical, and friendly — not generic. "
    "Return ONLY a JSON array, no markdown fences, no extra text.\n"
    'Each element: {"category": "<language|cultural|festival>", '
    '"severity": "<low|medium>", "summary": "<1-2 sentence tip>", '
    '"confidence": <0.80-0.95>}'
)


def _season_from_month(month):
    if month in (11, 12, 1, 2):
        return "winter/dry season"
    if month in (3, 4, 5):
        return "summer/hot season"
    return "monsoon/rainy season"


def _time_of_day(hour):
    if 5 <= hour < 12:
        return "morning"
    if 12 <= hour < 17:
        return "afternoon"
    if 17 <= hour < 21:
        return "evening"
    return "night"


class GeminiClient:
    """
    Generates transition alerts using two layers:
    1. Stub logic — deterministic set-diff on seed data (legal, live updates)
    2. Gemini API — cultural enrichment (greetings, practices, food, differences)

    If no GEMINI_API_KEY is configured, only the stub layer runs.
    If the Gemini call fails at runtime, the stub layer is returned as fallback.

    Alerts from Gemini are tagged with source="gemini" so governance can
    guarantee at least one enrichment alert is included.
    """

    def __init__(self, config):
        self._model_name = config.GEMINI_MODEL_NAME
        self._api_key = config.GEMINI_API_KEY
        self._use_stub = True
        self._client = None

        if self._api_key:
            try:
                from google import genai
                self._client = genai.Client(api_key=self._api_key)
                self._use_stub = False
                logger.info("Gemini API initialized (model=%s)", self._model_name)
            except Exception:
                logger.exception("Failed to initialize Gemini SDK — falling back to stub")

    def generate_transition_alerts(self, prev_region, curr_region,
                                   live_updates, transition_type):
        if not prev_region or not curr_region:
            return []

        # Layer 1: deterministic stub alerts (legal diffs, live updates)
        alerts = self._stub_alerts(prev_region, curr_region,
                                   live_updates, transition_type)

        # Layer 2: Gemini cultural enrichment (if available)
        if not self._use_stub:
            enrichment = self._gemini_alerts(prev_region, curr_region,
                                            transition_type)
            alerts.extend(enrichment)

        return alerts

    # ------------------------------------------------------------------
    # Layer 1: deterministic stub (always runs)
    # ------------------------------------------------------------------

    def _stub_alerts(self, prev_region, curr_region,
                     live_updates, transition_type):
        alerts = []

        # Language shift
        prev_lang = prev_region.get("dominant_language", "")
        curr_lang = curr_region.get("dominant_language", "")
        if prev_lang and curr_lang and prev_lang != curr_lang:
            greeting = ""
            if transition_type == "state_to_state":
                curr_name = curr_region.get("id", "").replace("_", " ").title()
                greeting = f"Welcome to {curr_name}! "

            alerts.append(self._make_alert(
                category="language",
                severity="medium",
                summary=(
                    f"{greeting}Primary language shifts from "
                    f"{prev_lang} to {curr_lang}."
                ),
                confidence=0.95,
                source="stub",
            ))

        # Legal differences
        prev_legal = set(prev_region.get("legal_rules", []))
        curr_legal = set(curr_region.get("legal_rules", []))
        new_legal = curr_legal - prev_legal
        for rule in sorted(new_legal)[:2]:
            alerts.append(self._make_alert(
                category="legal",
                severity="high",
                summary=rule,
                confidence=0.90,
                source="stub",
            ))

        # Cultural differences
        prev_cultural = set(prev_region.get("cultural_markers", []))
        curr_cultural = set(curr_region.get("cultural_markers", []))
        new_cultural = curr_cultural - prev_cultural
        for marker in sorted(new_cultural)[:1]:
            alerts.append(self._make_alert(
                category="cultural",
                severity="low",
                summary=marker,
                confidence=0.85,
                source="stub",
            ))

        # Behavioral differences
        prev_behavioral = set(prev_region.get("behavioral_notes", []))
        curr_behavioral = set(curr_region.get("behavioral_notes", []))
        new_behavioral = curr_behavioral - prev_behavioral
        for note in sorted(new_behavioral)[:1]:
            alerts.append(self._make_alert(
                category="cultural",
                severity="low",
                summary=note,
                confidence=0.80,
                source="stub",
            ))

        # Live updates as alerts
        for update in live_updates:
            alerts.append(self._make_alert(
                category=update.get("category", "safety"),
                severity=update.get("severity", "medium"),
                summary=update.get("summary", ""),
                confidence=update.get("confidence_score", 0.5),
                source="stub",
            ))

        return alerts

    # ------------------------------------------------------------------
    # Layer 2: Gemini cultural enrichment
    # ------------------------------------------------------------------

    def _gemini_alerts(self, prev_region, curr_region, transition_type):
        try:
            now = datetime.now(timezone.utc)
            prompt = self._build_prompt(prev_region, curr_region,
                                        transition_type, now)

            response = self._client.models.generate_content(
                model=self._model_name,
                contents=prompt,
                config={
                    "system_instruction": _SYSTEM_INSTRUCTION,
                    "temperature": 0.7,
                    "max_output_tokens": 2048,
                },
            )
            text = response.text.strip()

            # Strip markdown fences if Gemini wraps the response
            if text.startswith("```"):
                text = text.split("\n", 1)[1] if "\n" in text else text[3:]
                if text.endswith("```"):
                    text = text[:-3].strip()

            items = json.loads(text)
            if not isinstance(items, list):
                logger.warning("Gemini returned non-list: %s", type(items))
                return []

            alerts = []
            for item in items:
                category = item.get("category", "cultural")
                severity = item.get("severity", "low")
                summary = item.get("summary", "")
                confidence = item.get("confidence", 0.85)

                if not summary:
                    continue

                # Clamp to valid values
                if category not in ("language", "cultural", "festival",
                                    "safety", "weather"):
                    category = "cultural"
                if severity not in ("low", "medium", "high", "critical"):
                    severity = "low"
                confidence = max(0.0, min(1.0, float(confidence)))

                alerts.append(self._make_alert(
                    category=category,
                    severity=severity,
                    summary=summary,
                    confidence=confidence,
                    source="gemini",
                ))

            logger.info("Gemini returned %d cultural enrichment alerts", len(alerts))
            return alerts

        except Exception:
            logger.exception("Gemini API call failed — returning no enrichment")
            return []

    @staticmethod
    def _build_prompt(prev_region, curr_region, transition_type, now):
        prev_name = prev_region.get("id", "unknown").replace("_", " ").title()
        curr_name = curr_region.get("id", "unknown").replace("_", " ").title()
        prev_lang = prev_region.get("dominant_language", "unknown")
        curr_lang = curr_region.get("dominant_language", "unknown")
        prev_type = prev_region.get("type", "state")
        curr_type = curr_region.get("type", "state")
        curr_parent = curr_region.get("parent_region", "")

        day_name = now.strftime("%A")
        tod = _time_of_day(now.hour)
        month_name = now.strftime("%B")
        season = _season_from_month(now.month)

        parent_str = f" in {curr_parent.replace('_', ' ').title()}" if curr_parent else ""

        return (
            f"Traveling from: {prev_name} ({prev_type}, {prev_lang}-speaking)\n"
            f"Arriving in: {curr_name} ({curr_type}{parent_str}, "
            f"{curr_lang}-speaking)\n"
            f"Transition: {transition_type}\n"
            f"Time: {day_name} {tod}, {month_name} ({season})\n\n"
            f"Generate 3-4 cultural tips as a JSON array."
        )

    @staticmethod
    def _make_alert(category, severity, summary, confidence, source="stub"):
        return {
            "id": str(uuid.uuid4()),
            "category": category,
            "severity": severity,
            "summary": summary,
            "confidence": confidence,
            "source": source,
        }
