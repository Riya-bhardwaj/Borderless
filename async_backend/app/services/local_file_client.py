import json
import os
import threading


class LocalFileClient:
    """
    Drop-in replacement for FirestoreClient that uses local JSON files.
    - seed_data.json: regions + live_updates (read-only at runtime, written by seed script)
    - runtime_data.json: user_sessions + transition_results (written at runtime)
    """

    def __init__(self, config):
        self._seed_path = config.LOCAL_STORAGE_PATH
        self._runtime_path = config.LOCAL_RUNTIME_PATH
        self._lock = threading.Lock()
        self._regions_col = config.COLLECTION_REGIONS
        self._live_updates_col = config.COLLECTION_LIVE_UPDATES
        self._sessions_col = config.COLLECTION_USER_SESSIONS
        self._results_col = config.COLLECTION_TRANSITION_RESULTS

        if not os.path.exists(self._seed_path):
            self._write_file(self._seed_path, {})
        if not os.path.exists(self._runtime_path):
            self._write_file(self._runtime_path, {})

    @staticmethod
    def _read_file(path):
        with open(path, "r") as f:
            return json.load(f)

    @staticmethod
    def _write_file(path, store):
        with open(path, "w") as f:
            json.dump(store, f, indent=2, default=str)

    def _get_collection(self, store, collection):
        return store.setdefault(collection, {})

    # --- Regions (from seed file) ---

    def get_region(self, region_id):
        with self._lock:
            store = self._read_file(self._seed_path)
            col = self._get_collection(store, self._regions_col)
            data = col.get(region_id)
            if data is None:
                return None
            return {**data, "id": region_id}

    def get_all_regions(self):
        with self._lock:
            store = self._read_file(self._seed_path)
            col = self._get_collection(store, self._regions_col)
            return [{**v, "id": k} for k, v in col.items()]

    # --- Live updates (from seed file) ---

    def get_active_live_updates(self, region_id, now):
        with self._lock:
            store = self._read_file(self._seed_path)
            col = self._get_collection(store, self._live_updates_col)
            results = []
            for doc_id, data in col.items():
                if data.get("region_id") != region_id:
                    continue
                expires_at = data.get("expires_at", "")
                if isinstance(expires_at, str) and expires_at > now.isoformat():
                    results.append({**data, "id": doc_id})
                elif not isinstance(expires_at, str):
                    results.append({**data, "id": doc_id})
            return results

    # --- User sessions (runtime file) ---

    def get_user_session(self, user_id):
        with self._lock:
            store = self._read_file(self._runtime_path)
            col = self._get_collection(store, self._sessions_col)
            return col.get(user_id)

    def update_user_session(self, user_id, data):
        with self._lock:
            store = self._read_file(self._runtime_path)
            col = self._get_collection(store, self._sessions_col)
            existing = col.get(user_id, {})
            existing.update(data)
            col[user_id] = existing
            self._write_file(self._runtime_path, store)

    # --- Transition results (runtime file) ---

    def save_transition_result(self, transition_id, data):
        with self._lock:
            store = self._read_file(self._runtime_path)
            col = self._get_collection(store, self._results_col)
            col[transition_id] = data
            self._write_file(self._runtime_path, store)

    def get_transition_result(self, transition_id):
        with self._lock:
            store = self._read_file(self._runtime_path)
            col = self._get_collection(store, self._results_col)
            data = col.get(transition_id)
            if data is None:
                return None
            return {**data, "id": transition_id}

    # --- Bulk write (for seeding — goes to seed file) ---

    def set_document(self, collection, doc_id, data):
        with self._lock:
            store = self._read_file(self._seed_path)
            col = self._get_collection(store, collection)
            col[doc_id] = data
            self._write_file(self._seed_path, store)
