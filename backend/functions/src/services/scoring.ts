import { AlertDoc } from './firestore';

export interface ScoredAlert {
  id: string;
  category: string;
  severity: string;
  title: string;
  description: string;
  source: string;
  tags: string[];
  score: number;
}

const SEVERITY_WEIGHTS: Record<string, number> = {
  critical: 100,
  important: 60,
  informational: 20,
};

const CATEGORY_WEIGHTS: Record<string, number> = {
  legal: 1.5,
  cultural: 1.2,
  behavioral: 1.0,
};

export function scoreAlerts(alerts: AlertDoc[]): ScoredAlert[] {
  return alerts
    .map((alert) => {
      const severityWeight = SEVERITY_WEIGHTS[alert.severity] ?? 20;
      const categoryWeight = CATEGORY_WEIGHTS[alert.category] ?? 1.0;
      const score = severityWeight * categoryWeight;

      return {
        id: alert.id,
        category: alert.category,
        severity: alert.severity,
        title: alert.title,
        description: alert.description,
        source: alert.source,
        tags: alert.tags || [],
        score,
      };
    })
    .sort((a, b) => b.score - a.score);
}

export function sortBySeverity(alerts: AlertDoc[]): AlertDoc[] {
  const severityOrder: Record<string, number> = {
    critical: 0,
    important: 1,
    informational: 2,
  };

  return [...alerts].sort(
    (a, b) => (severityOrder[a.severity] ?? 3) - (severityOrder[b.severity] ?? 3),
  );
}

export function filterByUserPreferences(
  alerts: ScoredAlert[],
  filters: { critical: boolean; important: boolean; informational: boolean },
): ScoredAlert[] {
  return alerts.filter((alert) => {
    if (alert.severity === 'critical' && !filters.critical) return false;
    if (alert.severity === 'important' && !filters.important) return false;
    if (alert.severity === 'informational' && !filters.informational) return false;
    return true;
  });
}

export function getTopAlerts(alerts: ScoredAlert[], limit: number = 5): ScoredAlert[] {
  return alerts.slice(0, limit);
}

export function countByCategory(alerts: ScoredAlert[]): Record<string, number> {
  return alerts.reduce(
    (counts, alert) => {
      counts[alert.category] = (counts[alert.category] || 0) + 1;
      return counts;
    },
    {} as Record<string, number>,
  );
}

export function countBySeverity(alerts: ScoredAlert[]): Record<string, number> {
  return alerts.reduce(
    (counts, alert) => {
      counts[alert.severity] = (counts[alert.severity] || 0) + 1;
      return counts;
    },
    {} as Record<string, number>,
  );
}
