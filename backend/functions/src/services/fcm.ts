import * as admin from 'firebase-admin';

function getDb() {
  return admin.firestore();
}

interface AlertPayload {
  title: string;
  description: string;
  severity: string;
  category: string;
}

export async function storeDeviceToken(
  userId: string,
  token: string,
  platform: string = 'android',
): Promise<void> {
  await getDb()
    .collection('users')
    .doc(userId)
    .collection('tokens')
    .doc(token)
    .set({
      token,
      platform,
      createdAt: admin.firestore.Timestamp.now(),
    });
}

export async function getUserTokens(userId: string): Promise<string[]> {
  const snapshot = await getDb()
    .collection('users')
    .doc(userId)
    .collection('tokens')
    .get();

  return snapshot.docs.map((doc) => doc.data().token as string);
}

export async function sendAlertNotification(
  userId: string,
  regionId: string,
  alert: AlertPayload,
): Promise<void> {
  const tokens = await getUserTokens(userId);
  if (tokens.length === 0) return;

  const message: admin.messaging.MulticastMessage = {
    tokens,
    data: {
      regionId,
      title: alert.title,
      body: alert.description,
      severity: alert.severity,
      category: alert.category,
    },
    android: {
      priority: alert.severity === 'critical' ? 'high' : 'normal',
    },
  };

  try {
    const response = await admin.messaging().sendEachForMulticast(message);

    // Clean up invalid tokens
    if (response.failureCount > 0) {
      const invalidTokens: string[] = [];
      response.responses.forEach((resp, idx) => {
        if (!resp.success) {
          const errorCode = resp.error?.code;
          if (
            errorCode === 'messaging/invalid-registration-token' ||
            errorCode === 'messaging/registration-token-not-registered'
          ) {
            invalidTokens.push(tokens[idx]);
          }
        }
      });

      // Delete invalid tokens
      const batch = getDb().batch();
      for (const token of invalidTokens) {
        batch.delete(
          getDb().collection('users').doc(userId).collection('tokens').doc(token),
        );
      }
      if (invalidTokens.length > 0) {
        await batch.commit();
      }
    }
  } catch (error) {
    console.error(`Failed to send FCM to user ${userId}:`, error);
  }
}

export async function getUsersByCurrentRegion(regionId: string): Promise<string[]> {
  const snapshot = await getDb()
    .collection('users')
    .where('currentRegionId', '==', regionId)
    .get();

  return snapshot.docs.map((doc) => doc.id);
}
