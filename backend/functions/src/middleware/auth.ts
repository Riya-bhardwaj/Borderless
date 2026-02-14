import { Request, Response, NextFunction } from 'express';
import * as admin from 'firebase-admin';

export interface AuthenticatedRequest extends Request {
  uid: string;
}

export function authMiddleware(req: Request, res: Response, next: NextFunction): void {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    res.status(401).json({ error: 'Missing or invalid authorization header' });
    return;
  }

  const token = authHeader.split('Bearer ')[1];

  admin
    .auth()
    .verifyIdToken(token)
    .then((decodedToken) => {
      (req as AuthenticatedRequest).uid = decodedToken.uid;
      next();
    })
    .catch((error) => {
      console.error('Auth token verification failed:', error.message);
      res.status(401).json({ error: 'Invalid or expired token' });
    });
}
