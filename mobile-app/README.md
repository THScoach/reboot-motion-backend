# Reboot Motion Mobile App

**React Native + Expo Mobile Application**  
**Priority 15: Mobile App Development**

A cross-platform mobile app (iOS & Android) for the Reboot Motion biomechanics analysis and training platform.

---

## 📱 **Features**

### **Completed Features:**

1. **🎯 Swing Analysis**
   - Input athlete data and video analysis scores
   - Real-time biomechanics analysis
   - Motor preference detection (SPINNER/GLIDER/LAUNCHER)
   - Fair, motor-aware scoring adjustments

2. **📊 Results Dashboard**
   - Motor Preference Card with confidence indicators
   - Adjusted Scores Display (raw → adjusted transformation)
   - Kinetic Capacity metrics (bat speed potential)
   - Energy leak identification
   - Personalized correction plan

3. **🎓 Drill Recommendations**
   - Progressive drill sequence (Stage 1 → 2 → 3)
   - Detailed drill instructions
   - Coaching cues and equipment lists
   - Expected outcomes

4. **🎬 Video Library**
   - Browse 11+ professional drill demonstrations
   - Search videos by keywords
   - Filter by category, stage, tags
   - Integrated video player support
   - Featured videos section

5. **💾 Offline Support**
   - Cached analysis results
   - Cached video library
   - Works without internet connection

### **Integrated APIs:**

- ✅ Priority 9: Kinetic Capacity Framework
- ✅ Priority 10: Recommendation Engine
- ✅ Priority 11: BioSwing Motor Preference
- ✅ Priority 12: Enhanced Analysis UI
- ✅ Priority 13: Video Library Integration

---

## 🚀 **Quick Start**

### **Prerequisites:**

- Node.js (v16 or higher)
- npm or yarn
- Expo CLI (`npm install -g expo-cli`)
- Expo Go app (for testing on physical devices)
  - [iOS App Store](https://apps.apple.com/app/expo-go/id982107779)
  - [Google Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent)

### **Installation:**

```bash
cd /home/user/webapp/mobile-app

# Install dependencies
npm install

# Start development server
npx expo start
```

### **Running on Devices:**

**Option 1: Expo Go (Recommended for development)**
```bash
npx expo start

# Scan QR code with:
# - iOS: Camera app
# - Android: Expo Go app
```

**Option 2: iOS Simulator**
```bash
npx expo start --ios
```

**Option 3: Android Emulator**
```bash
npx expo start --android
```

**Option 4: Web Browser**
```bash
npx expo start --web
```

---

## 📁 **Project Structure**

```
mobile-app/
├── App.js                          # Main app entry with navigation
├── app.json                        # Expo configuration
├── package.json                    # Dependencies
├── src/
│   ├── screens/
│   │   ├── HomeScreen.js          # Landing page
│   │   ├── AnalysisScreen.js      # Input form for swing analysis
│   │   ├── ResultsScreen.js       # Analysis results dashboard
│   │   ├── DrillDetailScreen.js   # Detailed drill information
│   │   └── VideoLibraryScreen.js  # Video browser & search
│   └── services/
│       └── api.js                  # API integration & caching
└── assets/                         # Icons, images, fonts
```

---

## 🔧 **API Configuration**

The app connects to the Priority 13 Video-Enhanced Test Server:

**Base URL:** `https://8002-i5cseikj92ei70k8wadux-2e77fc33.sandbox.novita.ai`

To change the API endpoint, edit `/src/services/api.js`:

```javascript
const API_BASE_URL = 'YOUR_API_URL_HERE';
```

---

## 📊 **Screens Overview**

### **1. Home Screen**
- Welcome page with feature overview
- Quick access to "New Analysis" and "Video Library"
- Feature highlights (motor preference, scoring, capacity, drills, videos)

### **2. Analysis Screen**
- Input form for athlete data:
  - Video analysis scores (Ground, Engine, Weapon)
  - Athlete information (height, wingspan, weight, age)
  - Optional data (actual bat speed, kinetic energy)
- "Load Sample Data" button (Eric Williams example)
- Real-time validation

### **3. Results Screen**
Comprehensive analysis dashboard:
- **Motor Preference Card**
  - Detected preference (SPINNER/GLIDER/LAUNCHER)
  - Confidence percentage
  - Coaching focus & avoidance guidance
- **Motor-Aware Scoring**
  - Raw vs. adjusted score comparison
  - Visual score bars
  - Adjustment badges
- **Kinetic Capacity**
  - Bat speed range & target
  - Predicted vs. actual performance
  - Gap to maximum potential
- **Correction Plan**
  - Timeline (4-6 weeks, etc.)
  - Issues identified with severity
  - Progressive drill sequence
  - Success metrics

### **4. Drill Detail Screen**
- Drill stage badge
- Complete description
- How it works
- Coaching cues (bullet list)
- Sets & reps
- Equipment needed
- Tool integration notes
- Expected outcomes
- Video demonstrations (tap to watch)

### **5. Video Library Screen**
- Search bar
- Video grid with thumbnails
- Category & stage badges
- Duration display
- Featured videos highlighted
- Tap to play videos in external player

---

## 💾 **Offline Support & Caching**

The app caches the following data locally:

- **Analysis Results:** Most recent analysis (1 hour cache)
- **Featured Videos:** Video library metadata (1 hour cache)
- **Video Library:** Full video list (1 hour cache)

Cache is stored using AsyncStorage and automatically expires after 1 hour.

**Manual Cache Clear:**
```javascript
import { clearCache } from './src/services/api';
await clearCache();
```

---

## 🎨 **Design System**

### **Color Palette:**
- **Primary Blue:** `#3b82f6` (buttons, accents)
- **Dark Blue:** `#1e3a8a` (headers, titles)
- **Success Green:** `#10b981` (positive indicators)
- **Warning Orange:** `#f59e0b` (medium priority)
- **Danger Red:** `#ef4444` (critical issues)
- **Background:** `#f9fafb` (light gray)

### **Motor Preference Colors:**
- **SPINNER:** `#ec4899` (pink)
- **GLIDER:** `#3b82f6` (blue)
- **LAUNCHER:** `#10b981` (green)

### **Typography:**
- **System Fonts:** San Francisco (iOS), Roboto (Android)
- **Sizes:** 12-32px
- **Weights:** 400 (regular), 600 (semibold), 700/800 (bold)

---

## 🧪 **Testing**

### **Test with Sample Data:**

The app includes Eric Williams' data for testing:

1. Navigate to "New Analysis"
2. Tap "Load Sample Data (Eric Williams)"
3. Tap "🔬 Analyze Swing"
4. View results

**Expected Results:**
- Motor Preference: SPINNER (85.7% confidence)
- Ground Score: 38 → 72 (+34)
- Issues: 2 identified
- Drills: 4 progressive drills
- Expected Gain: +11 mph

---

## 📦 **Building for Production**

### **iOS Build:**
```bash
# Create production build
npx eas build --platform ios

# Submit to App Store
npx eas submit --platform ios
```

### **Android Build:**
```bash
# Create production build (APK)
npx eas build --platform android --profile preview

# Create production build (AAB for Play Store)
npx eas build --platform android

# Submit to Play Store
npx eas submit --platform android
```

**Note:** Requires Expo EAS (Expo Application Services) account.
Sign up at: https://expo.dev/

---

## 🔐 **Environment Variables**

For production deployment, configure:

```bash
# .env file
API_BASE_URL=https://your-production-api.com
API_TIMEOUT=30000
CACHE_MAX_AGE=3600000
```

---

## 📱 **App Store Listings**

### **App Name:**
Reboot Motion - Swing Analysis

### **Description:**
Professional biomechanics analysis and personalized training for baseball and softball players. Get instant swing analysis, motor preference detection, and progressive drill recommendations with video demonstrations.

**Features:**
- 🧬 Motor Preference Detection (SPINNER/GLIDER/LAUNCHER)
- 📊 Fair, Motor-Aware Scoring
- ⚡ Kinetic Capacity Analysis
- 🎓 Personalized Drill Progressions
- 🎬 Professional Video Demonstrations
- 💾 Offline Support

Based on Dr. Kwon's biomechanics research.

### **Keywords:**
baseball, softball, swing analysis, biomechanics, hitting, training, coaching, drills, motor preference, bat speed

### **Category:**
Sports / Health & Fitness

### **Screenshots Needed:**
1. Home screen
2. Analysis input screen
3. Results - Motor Preference
4. Results - Correction Plan
5. Drill Detail screen
6. Video Library

---

## 🐛 **Troubleshooting**

### **Common Issues:**

**1. Cannot connect to API**
- Check internet connection
- Verify API_BASE_URL in `/src/services/api.js`
- Test API health: `curl https://8002-i5cseikj92ei70k8wadux-2e77fc33.sandbox.novita.ai/health`

**2. Videos won't play**
- Ensure device has YouTube app or web browser
- Check video URLs in video library

**3. App crashes on startup**
- Clear Expo cache: `npx expo start -c`
- Reinstall dependencies: `rm -rf node_modules && npm install`

**4. Slow performance**
- Clear app cache
- Reduce cached data age
- Use production builds instead of development mode

---

## 📚 **Documentation**

- **Expo Docs:** https://docs.expo.dev/
- **React Native Docs:** https://reactnative.dev/docs/getting-started
- **React Navigation:** https://reactnavigation.org/docs/getting-started

---

## 🤝 **Contributing**

### **Adding New Screens:**
1. Create screen component in `/src/screens/`
2. Add to navigation in `App.js`
3. Update this README

### **Adding New API Endpoints:**
1. Add function to `/src/services/api.js`
2. Implement caching if needed
3. Handle errors gracefully

---

## 📄 **License**

Copyright © 2025 Reboot Motion. All rights reserved.

---

## 📞 **Support**

- **Repository:** https://github.com/THScoach/reboot-motion-backend
- **Issues:** https://github.com/THScoach/reboot-motion-backend/issues
- **Email:** support@rebootmotion.com (placeholder)

---

## 🎉 **Version History**

### **v1.0.0 (Current)**
- ✅ Initial release
- ✅ Swing analysis with Priority 9+10+11 integration
- ✅ Video library integration (Priority 13)
- ✅ Offline support & caching
- ✅ Cross-platform (iOS, Android, Web)

---

**Built with ❤️ by the Reboot Motion Development Team**  
**December 23, 2025**
