// ═══════════════════════════════════════════════════════════
//  FIREBASE CONFIGURATION — house-pokhara project
// ═══════════════════════════════════════════════════════════

const FIREBASE_CONFIG = {
  apiKey:            "AIzaSyAW8h8KE4mzjnOaE507tBOVPKSu8CGwCc4",
  authDomain:        "house-pokhara.firebaseapp.com",
  projectId:         "house-pokhara",
  storageBucket:     "house-pokhara.firebasestorage.app",
  messagingSenderId: "987044951918",
  appId:             "1:987044951918:web:2b7063a7f0bbad4259737f",
  measurementId:     "G-TJ1BHV6GG8"
};

// ── Allowed editor emails ───────────────────────────────────
// Only these Gmail accounts can ADD, EDIT, or DELETE expenses.
// Everyone else can VIEW the budget page without logging in.
const ALLOWED_EDITORS = [
  "santoshpoudel15@gmail.com",
  "pavitrapoudel9287@gmail.com",
];

// ── Default conversion rate: 1 INR = X NPR ─────────────────
const DEFAULT_INR_TO_NPR = 1.60;

// ── Config status check ─────────────────────────────────────
const IS_FIREBASE_READY = !FIREBASE_CONFIG.apiKey.includes('YOUR_');
