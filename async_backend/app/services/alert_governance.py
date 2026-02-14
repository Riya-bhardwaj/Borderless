from datetime import datetime, timedelta, timezone


class AlertGovernance:
    def __init__(self, config):
        self._max_alerts = config.MAX_ALERTS_PER_TRANSITION
        self._dedup_hours = config.DEDUP_WINDOW_HOURS
        self._confidence_threshold = config.CONFIDENCE_THRESHOLD_PUSH
        self._severity_priority = config.SEVERITY_PRIORITY
        self._category_priority = config.ALERT_CATEGORY_PRIORITY

    def apply(self, alerts, session, now=None):
        if now is None:
            now = datetime.now(timezone.utc)

        # 1. Dedup: remove alerts with categories shown within dedup window
        alerts = self._dedup(alerts, session, now)

        # 2. Rank by severity priority → category priority → confidence desc
        alerts = self._rank(alerts)

        # 3. Cap at max alerts, guaranteeing at least 1 Gemini enrichment
        alerts = self._cap_with_gemini_guarantee(alerts)

        # 4. Tag delivery channel
        for alert in alerts:
            is_high_severity = alert.get("severity") in ("critical", "high")
            is_high_confidence = alert.get("confidence", 0) >= self._confidence_threshold
            alert["delivery"] = "push" if (is_high_severity and is_high_confidence) else "dashboard"

        # 5. Strip internal source tag before returning
        for alert in alerts:
            alert.pop("source", None)

        return alerts

    def _cap_with_gemini_guarantee(self, ranked_alerts):
        """Cap to max alerts, but guarantee at least 1 Gemini alert if any exist."""
        if len(ranked_alerts) <= self._max_alerts:
            return ranked_alerts

        top = ranked_alerts[:self._max_alerts]
        has_gemini = any(a.get("source") == "gemini" for a in top)

        if has_gemini:
            return top

        # No Gemini alert in top N — find the best one and swap it in
        best_gemini = next(
            (a for a in ranked_alerts if a.get("source") == "gemini"), None
        )
        if best_gemini is None:
            return top

        # Replace the last (lowest priority) stub alert with the best Gemini one
        top[-1] = best_gemini
        return top

    def _dedup(self, alerts, session, now):
        if not session:
            return alerts

        last_ts_str = session.get("last_update_timestamp")
        if not last_ts_str:
            return alerts

        try:
            last_ts = datetime.fromisoformat(last_ts_str)
            if last_ts.tzinfo is None:
                last_ts = last_ts.replace(tzinfo=timezone.utc)
        except (ValueError, TypeError):
            return alerts

        if (now - last_ts) >= timedelta(hours=self._dedup_hours):
            return alerts

        shown_categories = set(session.get("last_alerts_shown", []))
        return [a for a in alerts if a.get("category") not in shown_categories]

    def _rank(self, alerts):
        def sort_key(alert):
            sev = self._severity_priority.get(alert.get("severity", "low"), 99)
            cat = alert.get("category", "")
            cat_rank = (
                self._category_priority.index(cat)
                if cat in self._category_priority
                else 99
            )
            conf = -alert.get("confidence", 0)
            return (sev, cat_rank, conf)

        return sorted(alerts, key=sort_key)
