import * as admin from 'firebase-admin';
import * as functions from 'firebase-functions';
import { onDocumentCreated } from 'firebase-functions/v2/firestore';
import express from 'express';
import cors from 'cors';
import { authMiddleware } from './middleware/auth';
import regionsRouter from './routes/regions';
import qaRouter from './routes/qa';
import usersRouter from './routes/users';
import crossingsRouter from './routes/crossings';
import * as fcmService from './services/fcm';

// Initialize Firebase Admin
admin.initializeApp();

const app = express();

// Middleware
app.use(cors({ origin: true }));
app.use(express.json());

// Health check (no auth required)
app.get('/health', (_req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Apply auth middleware to all other routes
app.use(authMiddleware);

// Routes
app.use('/regions', regionsRouter);
app.use('/qa', qaRouter);
app.use('/users', usersRouter);
app.use('/crossings', crossingsRouter);

// Export as Firebase Cloud Function
export const api = functions.https.onRequest(app);

// Firestore trigger: send push notifications when a new alert is created
export const onAlertCreated = onDocumentCreated(
  'regions/{regionId}/alerts/{alertId}',
  async (event) => {
    const snapshot = event.data;
    if (!snapshot) return;

    const regionId = event.params.regionId;
    const alertData = snapshot.data();

    if (!alertData || !alertData.active) return;

    try {
      const userIds = await fcmService.getUsersByCurrentRegion(regionId);

      const sendPromises = userIds.map((userId) =>
        fcmService.sendAlertNotification(userId, regionId, {
          title: alertData.title || 'New Alert',
          description: alertData.description || 'A new alert has been posted for your region',
          severity: alertData.severity || 'informational',
          category: alertData.category || 'behavioral',
        }),
      );

      await Promise.all(sendPromises);
      console.log(`Sent push notifications to ${userIds.length} users for alert in region ${regionId}`);
    } catch (error) {
      console.error('Error sending alert notifications:', error);
    }
  },
);
