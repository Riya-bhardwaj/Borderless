import { Router } from 'express';
import { AuthenticatedRequest } from '../middleware/auth';
import * as firestoreService from '../services/firestore';
import * as fcmService from '../services/fcm';

const router = Router();

// POST /users/profile — Create or update user profile
router.post('/profile', async (req, res) => {
  try {
    const { uid } = req as AuthenticatedRequest;
    const { displayName, language, alertFilters } = req.body;

    if (!displayName) {
      res.status(400).json({ error: 'displayName is required' });
      return;
    }

    // Check if user exists
    const existingUser = await firestoreService.getUser(uid);

    if (existingUser) {
      // Update existing user
      await firestoreService.updateUser(uid, {
        displayName,
        language: language || existingUser.language,
        alertFilters: alertFilters || existingUser.alertFilters,
      });

      const updatedUser = await firestoreService.getUser(uid);
      res.json({
        uid,
        displayName: updatedUser?.displayName || displayName,
        language: updatedUser?.language || language || 'en',
        alertFilters: updatedUser?.alertFilters || { critical: true, important: true, informational: true },
        createdAt: updatedUser?.createdAt?.toDate?.()?.toISOString() || new Date().toISOString(),
        updatedAt: updatedUser?.updatedAt?.toDate?.()?.toISOString() || new Date().toISOString(),
      });
    } else {
      // Create new user
      const newUser = await firestoreService.createUser(uid, {
        displayName,
        language: language || 'en',
        alertFilters: alertFilters || { critical: true, important: true, informational: true },
      });

      res.json({
        uid,
        displayName: newUser.displayName,
        language: newUser.language,
        alertFilters: newUser.alertFilters,
        createdAt: newUser.createdAt?.toDate?.()?.toISOString() || new Date().toISOString(),
        updatedAt: newUser.updatedAt?.toDate?.()?.toISOString() || new Date().toISOString(),
      });
    }
  } catch (error) {
    console.error('Profile error:', error);
    res.status(500).json({ error: 'Failed to update profile' });
  }
});

// POST /users/device-token — Register FCM device token
router.post('/device-token', async (req, res) => {
  try {
    const { uid } = req as AuthenticatedRequest;
    const { token, platform } = req.body;

    if (!token || typeof token !== 'string' || token.length < 10) {
      res.status(400).json({ error: 'Valid token is required' });
      return;
    }

    await fcmService.storeDeviceToken(uid, token, platform || 'android');
    res.json({ success: true });
  } catch (error) {
    console.error('Device token registration error:', error);
    res.status(500).json({ error: 'Failed to register device token' });
  }
});

export default router;
