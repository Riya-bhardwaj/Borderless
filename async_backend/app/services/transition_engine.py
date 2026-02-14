import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class TransitionEngine:
    def __init__(self, firestore, gemini, governance, config):
        self._fs = firestore
        self._gemini = gemini
        self._gov = governance
        self._config = config

    def process_transition(self, transition_id, user_id, previous_region, current_region):
        """
        Runs the full alert pipeline and writes results to Firestore.
        Called from a background thread — does not return results to the caller.
        """
        now = datetime.now(timezone.utc)

        try:
            # Mark as processing
            self._fs.save_transition_result(transition_id, {
                "status": "processing",
                "user_id": user_id,
                "previous_region": previous_region,
                "current_region": current_region,
                "submitted_at": now.isoformat(),
            })

            # Step 1: Fetch region data
            prev_data = self._fs.get_region(previous_region)
            curr_data = self._fs.get_region(current_region)

            if not prev_data or not curr_data:
                missing = previous_region if not prev_data else current_region
                self._fs.save_transition_result(transition_id, {
                    "status": "failed",
                    "error": f"Region '{missing}' not found",
                    "completed_at": datetime.now(timezone.utc).isoformat(),
                })
                return

            # Step 2: Classify transition type
            transition_type = self._classify_transition(prev_data, curr_data)

            # Step 3: Fetch active live updates for current region
            live_updates = self._fs.get_active_live_updates(current_region, now)

            # Step 4: Generate candidate alerts via Gemini (stubbed)
            raw_alerts = self._gemini.generate_transition_alerts(
                prev_region=prev_data,
                curr_region=curr_data,
                live_updates=live_updates,
                transition_type=transition_type,
            )

            # Step 5: Apply governance rules
            session = self._fs.get_user_session(user_id)
            filtered_alerts = self._gov.apply(
                alerts=raw_alerts,
                session=session,
                now=now,
            )

            # Step 6: Update user session
            self._fs.update_user_session(user_id, {
                "user_id": user_id,
                "last_region": current_region,
                "last_transition_type": transition_type,
                "last_alerts_shown": [a["category"] for a in filtered_alerts],
                "last_update_timestamp": now.isoformat(),
            })

            # Step 7: Write completed result to Firestore
            self._fs.save_transition_result(transition_id, {
                "status": "completed",
                "user_id": user_id,
                "transition_type": transition_type,
                "previous_region": previous_region,
                "current_region": current_region,
                "alerts": filtered_alerts,
                "submitted_at": now.isoformat(),
                "completed_at": datetime.now(timezone.utc).isoformat(),
            })

            logger.info("Transition %s completed: %d alerts", transition_id, len(filtered_alerts))

        except Exception:
            logger.exception("Transition %s failed", transition_id)
            self._fs.save_transition_result(transition_id, {
                "status": "failed",
                "error": "Internal processing error",
                "completed_at": datetime.now(timezone.utc).isoformat(),
            })

    @staticmethod
    def _classify_transition(prev, curr):
        prev_type = prev.get("type", "state")
        curr_type = curr.get("type", "state")

        if curr_type == "zone":
            return "region_to_zone"

        if prev_type == "state" and curr_type == "state":
            return "state_to_state"

        if prev_type == "city" and curr_type == "city":
            if prev.get("parent_region") == curr.get("parent_region"):
                return "city_to_city_same_state"
            return "city_to_city_cross_state"

        return "state_to_state"
