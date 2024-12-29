const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// Generate random values for secrets
const generateSecret = () => crypto.randomBytes(32).toString('hex');

// Default environment variables
const envVars = {
  // LiveKit Configuration
  NEXT_PUBLIC_LIVEKIT_URL: 'ws://localhost:7880',
  LIVEKIT_API_KEY: 'devkey',
  LIVEKIT_API_SECRET: 'secret',

  // Voice Assistant Configuration
  NEXT_PUBLIC_VOICE_ASSISTANT_NAME: 'AI Assistant',
  NEXT_PUBLIC_MAX_AUDIO_DURATION_MS: '30000',
  NEXT_PUBLIC_SILENCE_THRESHOLD_DB: '-45',

  // Feature Flags
  NEXT_PUBLIC_ENABLE_VOICE_ACTIVITY_DETECTION: 'true',
  NEXT_PUBLIC_ENABLE_NOISE_SUPPRESSION: 'true',
  NEXT_PUBLIC_ENABLE_ECHO_CANCELLATION: 'true',

  // API Configuration
  NEXT_PUBLIC_API_URL: 'http://localhost:8000',
  NEXT_PUBLIC_WS_URL: 'ws://localhost:8000/ws',
};

// Create environment files
const environments = {
  development: '.env.local',
  test: '.env.test.local',
  production: '.env.production.local'
};

// Create the environment files for each environment
Object.entries(environments).forEach(([env, filename]) => {
  const filePath = path.join(__dirname, '..', filename);
  
  // Check if file already exists
  if (fs.existsSync(filePath)) {
    console.log(`${filename} already exists, skipping...`);
    return;
  }

  // Generate environment-specific variables
  const envSpecificVars = { ...envVars };
  
  // Add environment-specific overrides
  if (env === 'production') {
    envSpecificVars.NEXT_PUBLIC_API_URL = 'https://api.yourdomain.com';
    envSpecificVars.NEXT_PUBLIC_WS_URL = 'wss://api.yourdomain.com/ws';
    envSpecificVars.LIVEKIT_API_SECRET = generateSecret();
  }

  // Create the environment file content
  const fileContent = Object.entries(envSpecificVars)
    .map(([key, value]) => `${key}=${value}`)
    .join('\n');

  // Write the file
  fs.writeFileSync(filePath, fileContent);
  console.log(`Created ${filename}`);
});

console.log('\nEnvironment setup complete! 🚀');
console.log('\nNote: Make sure to update the production URLs and secrets before deploying.');
