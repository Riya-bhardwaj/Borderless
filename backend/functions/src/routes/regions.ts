import { Router } from 'express';
import * as firestoreService from '../services/firestore';
import { scoreAlerts } from '../services/scoring';
import { translateTexts } from '../services/gemini';

const router = Router();

// GET /regions — Retrieve all active regions with geofence definitions
router.get('/', async (req, res) => {
  try {
    const regions = await firestoreService.getRegions();

    const regionsWithCounts = await Promise.all(
      regions.map(async (region) => {
        const alerts = await firestoreService.getAlertsByRegion(region.id);
        return {
          id: region.id,
          name: region.name,
          type: region.type,
          parentId: region.parentId,
          geofences: region.geofences,
          quickFacts: region.quickFacts,
          alertCount: alerts.length,
        };
      }),
    );

    res.json({
      regions: regionsWithCounts,
      lastUpdated: new Date().toISOString(),
    });
  } catch (error) {
    console.error('Error fetching regions:', error);
    res.status(500).json({ error: 'Failed to fetch regions' });
  }
});

// GET /regions/:regionId/alerts — Retrieve alerts for a specific region
router.get('/:regionId/alerts', async (req, res) => {
  try {
    const { regionId } = req.params;
    const { language, severity } = req.query;

    // Verify region exists
    const region = await firestoreService.getRegionById(regionId);
    if (!region) {
      res.status(404).json({ error: 'Region not found' });
      return;
    }

    // Fetch alerts
    const severityFilter = severity as string | undefined;
    const alerts = await firestoreService.getAlertsByRegion(regionId, severityFilter);

    // Score and sort alerts
    const scoredAlerts = scoreAlerts(alerts);

    // Translate if non-English language requested
    const targetLang = (language as string) || 'en';
    let responseAlerts;

    if (targetLang !== 'en') {
      const textsToTranslate = scoredAlerts.flatMap((alert) => [
        { id: `${alert.id}-title`, text: alert.title },
        { id: `${alert.id}-desc`, text: alert.description },
      ]);

      const translations = await translateTexts(textsToTranslate, targetLang);

      responseAlerts = scoredAlerts.map((alert) => ({
        id: alert.id,
        category: alert.category,
        severity: alert.severity,
        title: translations.get(`${alert.id}-title`) || alert.title,
        description: translations.get(`${alert.id}-desc`) || alert.description,
        source: alert.source,
        tags: alert.tags,
      }));
    } else {
      responseAlerts = scoredAlerts.map((alert) => ({
        id: alert.id,
        category: alert.category,
        severity: alert.severity,
        title: alert.title,
        description: alert.description,
        source: alert.source,
        tags: alert.tags,
      }));
    }

    res.json({
      regionId: region.id,
      regionName: region.name,
      alerts: responseAlerts,
      totalCount: responseAlerts.length,
      language: targetLang,
    });
  } catch (error) {
    console.error('Error fetching alerts:', error);
    res.status(500).json({ error: 'Failed to fetch alerts' });
  }
});

export default router;
