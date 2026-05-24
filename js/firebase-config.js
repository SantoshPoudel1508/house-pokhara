// ═══════════════════════════════════════════════════════════
//  FIREBASE CONFIGURATION
//  Replace the values below with your own Firebase project.
//  Follow the steps in budget.html to set this up.
// ═══════════════════════════════════════════════════════════

const FIREBASE_CONFIG = {
  apiKey:            "YOUR_API_KEY",
  authDomain:        "YOUR_PROJECT_ID.firebaseapp.com",
  projectId:         "YOUR_PROJECT_ID",
  storageBucket:     "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId:             "YOUR_APP_ID"
};

// ── Allowed editor emails ───────────────────────────────────
// Only these email addresses can ADD or EDIT expenses.
// Anyone can VIEW the budget page without logging in.
// Add the Gmail addresses of people who should be able to edit.
const ALLOWED_EDITORS = [
  "your-email@gmail.com",
  // "father-email@gmail.com",
  // add more emails here
];

// ── Currency Settings ───────────────────────────────────────
// This is the default conversion rate: 1 INR = X NPR
// The app will try to fetch a live rate, but this is the fallback.
const DEFAULT_INR_TO_NPR = 1.60;

// ── Is Firebase configured? ─────────────────────────────────
const IS_FIREBASE_READY = !FIREBASE_CONFIG.apiKey.includes('YOUR_');
