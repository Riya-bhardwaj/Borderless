import * as admin from 'firebase-admin';

const db = admin.firestore();

export interface RegionDoc {
  id: string;
  name: string;
  type: string;
  parentId: string | null;
  geofences: Array<{
    lat: number;
    lng: number;
    radiusMeters: number;
    label: string;
  }>;
  quickFacts: string[];
  active: boolean;
  updatedAt: FirebaseFirestore.Timestamp;
}

export interface AlertDoc {
  id: string;
  category: string;
  severity: string;
  title: string;
  description: string;
  source: string;
  tags: string[];
  effectiveDate: FirebaseFirestore.Timestamp;
  expiryDate: FirebaseFirestore.Timestamp | null;
  active: boolean;
  updatedAt: FirebaseFirestore.Timestamp;
}

export interface UserDoc {
  uid: string;
  displayName: string;
  language: string;
  alertFilters: {
    critical: boolean;
    important: boolean;
    informational: boolean;
  };
  currentRegionId: string | null;
  createdAt: FirebaseFirestore.Timestamp;
  updatedAt: FirebaseFirestore.Timestamp;
}

export async function getRegions(): Promise<RegionDoc[]> {
  const snapshot = await db
    .collection('regions')
    .where('active', '==', true)
    .get();

  return snapshot.docs.map((doc) => ({
    id: doc.id,
    ...doc.data(),
  })) as RegionDoc[];
}

export async function getRegionById(regionId: string): Promise<RegionDoc | null> {
  const doc = await db.collection('regions').doc(regionId).get();
  if (!doc.exists) return null;
  return { id: doc.id, ...doc.data() } as RegionDoc;
}

export async function getAlertsByRegion(
  regionId: string,
  severityFilter?: string,
): Promise<AlertDoc[]> {
  let query: FirebaseFirestore.Query = db
    .collection('regions')
    .doc(regionId)
    .collection('alerts')
    .where('active', '==', true);

  if (severityFilter && severityFilter !== 'all') {
    query = query.where('severity', '==', severityFilter);
  }

  const snapshot = await query.get();

  const severityOrder: Record<string, number> = {
    critical: 0,
    important: 1,
    informational: 2,
  };

  const alerts = snapshot.docs.map((doc) => ({
    id: doc.id,
    ...doc.data(),
  })) as AlertDoc[];

  return alerts.sort(
    (a, b) => (severityOrder[a.severity] ?? 3) - (severityOrder[b.severity] ?? 3),
  );
}

export async function getUser(uid: string): Promise<UserDoc | null> {
  const doc = await db.collection('users').doc(uid).get();
  if (!doc.exists) return null;
  return doc.data() as UserDoc;
}

export async function createUser(uid: string, data: Partial<UserDoc>): Promise<UserDoc> {
  const now = admin.firestore.Timestamp.now();
  const userData: UserDoc = {
    uid,
    displayName: data.displayName || '',
    language: data.language || 'en',
    alertFilters: data.alertFilters || {
      critical: true,
      important: true,
      informational: true,
    },
    currentRegionId: null,
    createdAt: now,
    updatedAt: now,
  };

  await db.collection('users').doc(uid).set(userData);
  return userData;
}

export async function updateUser(uid: string, data: Partial<UserDoc>): Promise<void> {
  await db.collection('users').doc(uid).update({
    ...data,
    updatedAt: admin.firestore.Timestamp.now(),
  });
}

export async function logCrossing(
  userId: string,
  data: {
    fromRegionId: string;
    toRegionId: string;
    latitude: number;
    longitude: number;
    alertsDelivered: number;
  },
): Promise<string> {
  const doc = await db.collection('crossings').add({
    userId,
    ...data,
    timestamp: admin.firestore.Timestamp.now(),
  });
  return doc.id;
}

export async function getCrossings(
  userId: string,
  limit: number = 20,
): Promise<Array<{ id: string; [key: string]: unknown }>> {
  const snapshot = await db
    .collection('crossings')
    .where('userId', '==', userId)
    .orderBy('timestamp', 'desc')
    .limit(Math.min(limit, 100))
    .get();

  return snapshot.docs.map((doc) => ({
    id: doc.id,
    ...doc.data(),
  }));
}

export async function logQa(
  userId: string,
  data: {
    regionId: string;
    question: string;
    answer: string;
    riskRating: string;
    sources: string[];
    language: string;
    responseTimeMs: number;
  },
): Promise<string> {
  const doc = await db.collection('qaLogs').add({
    userId,
    ...data,
    feedback: null,
    createdAt: admin.firestore.Timestamp.now(),
  });
  return doc.id;
}
