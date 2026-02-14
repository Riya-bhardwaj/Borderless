from google.cloud import firestore


class FirestoreClient:
    def __init__(self, config):
        self._db = firestore.Client(project=config.GOOGLE_CLOUD_PROJECT)
        self._regions_col = config.COLLECTION_REGIONS
        self._live_updates_col = config.COLLECTION_LIVE_UPDATES
        self._sessions_col = config.COLLECTION_USER_SESSIONS
        self._results_col = config.COLLECTION_TRANSITION_RESULTS

    @property
    def db(self):
        return self._db

    # --- Regions ---

    def get_region(self, region_id):
        doc = self._db.collection(self._regions_col).document(region_id).get()
        if not doc.exists:
            return None
        data = doc.to_dict()
        data["id"] = doc.id
        return data

    def get_all_regions(self):
        docs = self._db.collection(self._regions_col).stream()
        results = []
        for doc in docs:
            data = doc.to_dict()
            data["id"] = doc.id
            results.append(data)
        return results

    # --- Live updates ---

    def get_active_live_updates(self, region_id, now):
        ref = self._db.collection(self._live_updates_col)
        query = ref.where("region_id", "==", region_id).where("expires_at", ">", now)
        results = []
        for doc in query.stream():
            data = doc.to_dict()
            data["id"] = doc.id
            results.append(data)
        return results

    # --- User sessions ---

    def get_user_session(self, user_id):
        doc = self._db.collection(self._sessions_col).document(user_id).get()
        if not doc.exists:
            return None
        return doc.to_dict()

    def update_user_session(self, user_id, data):
        self._db.collection(self._sessions_col).document(user_id).set(data, merge=True)

    # --- Transition results ---

    def save_transition_result(self, transition_id, data):
        self._db.collection(self._results_col).document(transition_id).set(data)

    def get_transition_result(self, transition_id):
        doc = self._db.collection(self._results_col).document(transition_id).get()
        if not doc.exists:
            return None
        data = doc.to_dict()
        data["id"] = doc.id
        return data

    # --- Bulk write (for seeding) ---

    def set_document(self, collection, doc_id, data):
        self._db.collection(collection).document(doc_id).set(data)
