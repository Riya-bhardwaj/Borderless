import * as admin from 'firebase-admin';
import * as fs from 'fs';
import * as path from 'path';

// Initialize Firebase Admin with service account
const serviceAccountPath = path.resolve(__dirname, '../service-account.json');
if (fs.existsSync(serviceAccountPath)) {
  const serviceAccount = JSON.parse(fs.readFileSync(serviceAccountPath, 'utf-8'));
  admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
  });
} else {
  // Use default credentials (emulator or ADC)
  admin.initializeApp();
}

const db = admin.firestore();

interface SeedAlert {
  id: string;
  category: string;
  severity: string;
  title: string;
  description: string;
  source: string;
  tags: string[];
  effectiveDate: string;
  expiryDate: string | null;
  active: boolean;
}

interface SeedRegion {
  id: string;
  name: string;
  type: string;
  parentId: string;
  geofences: Array<{
    lat: number;
    lng: number;
    radiusMeters: number;
    label: string;
  }>;
  quickFacts: string[];
  active: boolean;
}

interface SeedData {
  region: SeedRegion;
  city: SeedRegion;
  alerts: SeedAlert[];
}

const DATA_DIR = path.resolve(__dirname, 'data');
const UPDATE_MODE = process.argv.includes('--update');

async function seedRegion(data: SeedData): Promise<void> {
  const { region, city, alerts } = data;
  const now = admin.firestore.Timestamp.now();

  console.log(`  Seeding region: ${region.name} (${alerts.length} alerts)`);

  // Create region document
  const regionRef = db.collection('regions').doc(region.id);

  if (UPDATE_MODE) {
    const existing = await regionRef.get();
    if (existing.exists) {
      console.log(`    Region ${region.id} exists, updating...`);
      await regionRef.update({ ...region, updatedAt: now });
    } else {
      await regionRef.set({ ...region, updatedAt: now });
    }
  } else {
    await regionRef.set({ ...region, updatedAt: now });
  }

  // Create city document
  const cityRef = db.collection('regions').doc(city.id);
  if (UPDATE_MODE) {
    const existing = await cityRef.get();
    if (existing.exists) {
      console.log(`    City ${city.id} exists, updating...`);
      await cityRef.update({ ...city, updatedAt: now });
    } else {
      await cityRef.set({ ...city, updatedAt: now });
    }
  } else {
    await cityRef.set({ ...city, updatedAt: now });
  }

  // Seed alerts as subcollection under region
  const alertsRef = regionRef.collection('alerts');

  if (!UPDATE_MODE) {
    // Delete existing alerts first
    const existingAlerts = await alertsRef.get();
    const batch = db.batch();
    existingAlerts.docs.forEach((doc) => batch.delete(doc.ref));
    if (!existingAlerts.empty) {
      await batch.commit();
      console.log(`    Deleted ${existingAlerts.size} existing alerts`);
    }
  }

  // Add alerts in batches of 500
  const BATCH_SIZE = 500;
  for (let i = 0; i < alerts.length; i += BATCH_SIZE) {
    const batch = db.batch();
    const chunk = alerts.slice(i, i + BATCH_SIZE);

    for (const alert of chunk) {
      const alertRef = alertsRef.doc(alert.id);

      if (UPDATE_MODE) {
        const existing = await alertRef.get();
        if (existing.exists) {
          batch.update(alertRef, { ...alert, updatedAt: now });
        } else {
          batch.set(alertRef, { ...alert, updatedAt: now });
        }
      } else {
        batch.set(alertRef, { ...alert, updatedAt: now });
      }
    }

    await batch.commit();
  }

  console.log(`    Seeded ${alerts.length} alerts for ${region.name}`);
}

async function createIndiaParent(): Promise<void> {
  const now = admin.firestore.Timestamp.now();
  const indiaRef = db.collection('regions').doc('india');

  const existing = await indiaRef.get();
  if (!existing.exists || !UPDATE_MODE) {
    await indiaRef.set({
      id: 'india',
      name: 'India',
      type: 'country',
      parentId: null,
      geofences: [],
      quickFacts: [
        'World\'s largest democracy',
        '28 states and 8 union territories',
        'Hindi and English are official languages',
        'Diverse cultural heritage spanning millennia',
      ],
      active: true,
      updatedAt: now,
    });
    console.log('  Created India parent region');
  }
}

async function main(): Promise<void> {
  console.log(`\nBorderless Seed Script ${UPDATE_MODE ? '(UPDATE MODE)' : '(FULL SEED)'}`);
  console.log('='.repeat(50));

  // Create parent India region
  await createIndiaParent();

  // Read all seed data files
  const dataFiles = fs.readdirSync(DATA_DIR).filter((f) => f.endsWith('.json'));

  if (dataFiles.length === 0) {
    console.error('No seed data files found in', DATA_DIR);
    process.exit(1);
  }

  console.log(`\nFound ${dataFiles.length} seed data files\n`);

  let totalAlerts = 0;

  for (const file of dataFiles) {
    const filePath = path.join(DATA_DIR, file);
    const data: SeedData = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    await seedRegion(data);
    totalAlerts += data.alerts.length;
  }

  console.log(`\nSeed complete!`);
  console.log(`  Regions: ${dataFiles.length} states + ${dataFiles.length} cities + 1 country`);
  console.log(`  Alerts: ${totalAlerts} total`);
  console.log('='.repeat(50));

  process.exit(0);
}

main().catch((error) => {
  console.error('Seed failed:', error);
  process.exit(1);
});
