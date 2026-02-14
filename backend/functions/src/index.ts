import * as admin from 'firebase-admin';
import * as functions from 'firebase-functions';
import express from 'express';
import cors from 'cors';
import { authMiddleware } from './middleware/auth';
import regionsRouter from './routes/regions';
import qaRouter from './routes/qa';
import usersRouter from './routes/users';
import crossingsRouter from './routes/crossings';

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
