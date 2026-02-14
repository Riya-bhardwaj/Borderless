import { Router } from 'express';
import { AuthenticatedRequest } from '../middleware/auth';
import * as firestoreService from '../services/firestore';
import { answerQuestion } from '../services/gemini';

const router = Router();

// POST /qa — Submit a Q&A question grounded in regional metadata
router.post('/', async (req, res) => {
  try {
    const { uid } = req as AuthenticatedRequest;
    const { regionId, question, language } = req.body;

    // Validate request
    if (!regionId || !question) {
      res.status(400).json({ error: 'regionId and question are required' });
      return;
    }

    if (question.length > 500) {
      res.status(400).json({ error: 'Question must be 500 characters or less' });
      return;
    }

    // Verify region exists
    const region = await firestoreService.getRegionById(regionId);
    if (!region) {
      res.status(404).json({ error: 'Region not found' });
      return;
    }

    // Fetch alerts as grounding context
    const alerts = await firestoreService.getAlertsByRegion(regionId);
    const alertsContext = alerts.map((alert) => ({
      id: alert.id,
      category: alert.category,
      severity: alert.severity,
      title: alert.title,
      description: alert.description,
      source: alert.source,
    }));

    // Ask Gemini
    const targetLang = language || 'en';
    const result = await answerQuestion(question, region.name, alertsContext, targetLang);

    // Log the interaction
    await firestoreService.logQa(uid, {
      regionId,
      question,
      answer: result.answer,
      riskRating: result.riskRating,
      sources: result.sources.map((s) => s.alertId),
      language: targetLang,
      responseTimeMs: result.responseTimeMs,
    });

    res.json({
      answer: result.answer,
      riskRating: result.riskRating,
      sources: result.sources,
      language: targetLang,
      responseTimeMs: result.responseTimeMs,
    });
  } catch (error) {
    console.error('Q&A error:', error);
    res.status(503).json({ error: 'Failed to process question. Please try again.' });
  }
});

export default router;
