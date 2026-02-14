import { GoogleGenerativeAI } from '@google/generative-ai';
import * as fs from 'fs';
import * as path from 'path';

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || '');

function loadPrompt(filename: string): string {
  const promptPath = path.resolve(__dirname, '../prompts', filename);
  try {
    return fs.readFileSync(promptPath, 'utf-8');
  } catch {
    return '';
  }
}

export interface TranslationResult {
  translations: Array<{
    original: string;
    translated: string;
  }>;
}

export async function translateTexts(
  texts: Array<{ id: string; text: string }>,
  targetLanguage: string,
): Promise<Map<string, string>> {
  if (targetLanguage === 'en' || texts.length === 0) {
    return new Map(texts.map((t) => [t.id, t.text]));
  }

  const systemPrompt = loadPrompt('translate-system.txt');
  const model = genAI.getGenerativeModel({ model: 'gemini-2.0-flash' });

  const textsJson = JSON.stringify(texts);
  const prompt = `${systemPrompt}\n\nTarget language: ${targetLanguage}\n\nTexts to translate:\n${textsJson}\n\nReturn a JSON array of objects with "id" and "translated" fields.`;

  try {
    const result = await model.generateContent(prompt);
    const response = result.response.text();

    // Extract JSON from response
    const jsonMatch = response.match(/\[[\s\S]*\]/);
    if (!jsonMatch) {
      return new Map(texts.map((t) => [t.id, t.text]));
    }

    const translations = JSON.parse(jsonMatch[0]) as Array<{ id: string; translated: string }>;
    return new Map(translations.map((t) => [t.id, t.translated]));
  } catch (error) {
    console.error('Translation failed:', error);
    return new Map(texts.map((t) => [t.id, t.text]));
  }
}

export interface QaResult {
  answer: string;
  riskRating: string;
  sources: Array<{ alertId: string; title: string; source: string }>;
  responseTimeMs: number;
}

export async function answerQuestion(
  question: string,
  regionName: string,
  alertsContext: Array<{
    id: string;
    category: string;
    severity: string;
    title: string;
    description: string;
    source: string;
  }>,
  language: string = 'en',
): Promise<QaResult> {
  const startTime = Date.now();
  const systemPrompt = loadPrompt('qa-system.txt');
  const model = genAI.getGenerativeModel({ model: 'gemini-2.0-flash' });

  const contextJson = JSON.stringify(alertsContext, null, 2);
  const prompt = `${systemPrompt}\n\nRegion: ${regionName}\nLanguage: ${language}\n\nAvailable alert data for grounding:\n${contextJson}\n\nUser question: ${question}\n\nRespond with a JSON object containing: "answer" (string), "riskRating" (one of: "low", "medium", "high", "critical"), "sources" (array of {"alertId", "title", "source"} from the grounding data used).`;

  try {
    const result = await model.generateContent(prompt);
    const response = result.response.text();

    const jsonMatch = response.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      return {
        answer: 'I could not generate a response. Please try rephrasing your question.',
        riskRating: 'low',
        sources: [],
        responseTimeMs: Date.now() - startTime,
      };
    }

    const parsed = JSON.parse(jsonMatch[0]);
    return {
      answer: parsed.answer || 'No answer generated.',
      riskRating: parsed.riskRating || 'low',
      sources: parsed.sources || [],
      responseTimeMs: Date.now() - startTime,
    };
  } catch (error) {
    console.error('Q&A failed:', error);
    return {
      answer: 'An error occurred while processing your question. Please try again.',
      riskRating: 'low',
      sources: [],
      responseTimeMs: Date.now() - startTime,
    };
  }
}
