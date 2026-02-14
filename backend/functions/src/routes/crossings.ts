import { Router } from 'express';
import { AuthenticatedRequest } from '../middleware/auth';
import * as firestoreService from '../services/firestore';

const router = Router();

// POST /crossings — Log a boundary crossing event
router.post('/', async (req, res) => {
  try {
    const { uid } = req as AuthenticatedRequest;
    const { fromRegionId, toRegionId, latitude, longitude, alertsDelivered } = req.body;

    if (!fromRegionId || !toRegionId) {
      res.status(400).json({ error: 'fromRegionId and toRegionId are required' });
      return;
    }

    const id = await firestoreService.logCrossing(uid, {
      fromRegionId,
      toRegionId,
      latitude: latitude || 0,
      longitude: longitude || 0,
      alertsDelivered: alertsDelivered || 0,
    });

    res.status(201).json({
      id,
      fromRegionId,
      toRegionId,
      alertsDelivered: alertsDelivered || 0,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error('Crossing log error:', error);
    res.status(500).json({ error: 'Failed to log crossing' });
  }
});

// GET /crossings — Retrieve crossing history for the authenticated user
router.get('/', async (req, res) => {
  try {
    const { uid } = req as AuthenticatedRequest;
    const limit = parseInt(req.query.limit as string) || 20;

    const crossings = await firestoreService.getCrossings(uid, limit);

    // Enrich with region names
    const enrichedCrossings = await Promise.all(
      crossings.map(async (crossing: any) => {
        const fromRegion = await firestoreService.getRegionById(crossing.fromRegionId);
        const toRegion = await firestoreService.getRegionById(crossing.toRegionId);

        return {
          id: crossing.id,
          fromRegion: {
            id: crossing.fromRegionId,
            name: fromRegion?.name || crossing.fromRegionId,
          },
          toRegion: {
            id: crossing.toRegionId,
            name: toRegion?.name || crossing.toRegionId,
          },
          alertsDelivered: crossing.alertsDelivered || 0,
          timestamp: crossing.timestamp?.toDate?.()?.toISOString() || new Date().toISOString(),
        };
      }),
    );

    res.json({
      crossings: enrichedCrossings,
      total: enrichedCrossings.length,
    });
  } catch (error) {
    console.error('Crossings fetch error:', error);
    res.status(500).json({ error: 'Failed to fetch crossings' });
  }
});

export default router;
