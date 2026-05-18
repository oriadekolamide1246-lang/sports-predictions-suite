# Sports Predictions Suite - Build & Install Guide

Complete step-by-step guide to build and install the Sports Predictions Suite mobile app.

## 📋 Prerequisites

### System Requirements
- **Windows, Mac, or Linux** (recommend 8GB+ RAM)
- **Android SDK** (API 24+) - for Android builds
- **Java Development Kit (JDK)** 17 or newer

### Required Tools

1. **Flutter SDK** (3.24.0 or newer)
   - Download: https://flutter.dev/docs/get-started/install
   - Add Flutter to PATH
   - Verify: `flutter doctor`

2. **Android Studio** or **Android SDK tools**
   - Download: https://developer.android.com/studio
   - Install Android SDK Platform 35+
   - Accept Android licenses: `flutter doctor --android-licenses`

3. **Git** (to clone the repository)
   - Download: https://git-scm.com/

---

## 🚀 Step 1: Clone the Repository

```bash
git clone https://github.com/oriadekolamide1246-lang/sports-predictions-suite.git
cd sports-predictions-suite
```

---

## 🔧 Step 2: Firebase Setup (REQUIRED)

### A. Create Firebase Project
1. Go to https://console.firebase.google.com/
2. Click **"Create a project"**
3. Name it: `sports-predictions` (or your choice)
4. Enable **Firestore** (Native mode)
5. Enable **Firebase Authentication** (Email/Password provider)

### B. Configure Android App in Firebase
1. In Firebase Console, click **Android** icon
2. Register app with package name: `com.flore.footballtips`
3. Download `google-services.json`
4. Place it in: `sports-predictions-suite/apps/end_user_app/android/app/`

### C. Generate Firebase Configuration
```bash
# Install FlutterFire CLI
dart pub global activate flutterfire_cli

# Generate firebase_options.dart
flutterfire configure --project=<your-firebase-project-id>
```

When prompted:
- Select Android platform
- Use package name: `com.flore.footballtips`
- Output to: `shared/lib/firebase_options.dart`

---

## 📦 Step 3: Install Dependencies

```bash
# Navigate to repository root
cd sports-predictions-suite

# Get dependencies for shared package
cd shared
flutter pub get
cd ..

# Get dependencies for end-user app
cd apps/end_user_app
flutter pub get
cd ../..
```

---

## 🛠️ Step 4: Build APK for Android

### Option A: Debug APK (for testing)
```bash
cd apps/end_user_app

flutter build apk --debug
```

**Output location:**
```
build/app/outputs/apk/debug/app-debug.apk
```

### Option B: Release APK (for production)

#### 4B.1 Create Keystore (one-time setup)
```bash
# From apps/end_user_app directory
keytool -genkey -v -keystore android/app/football_predictions.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias footballkey
```

**When prompted, enter:**
- Password: (remember this!)
- First/Last Name: Your Name
- Organization: Your Company
- City: Your City
- State: Your State
- Country: Your Country (e.g., US)
- Confirm all with "yes"

#### 4B.2 Create Keystore Properties File
Create `android/key.properties`:
```properties
storePassword=YOUR_PASSWORD_HERE
keyPassword=YOUR_PASSWORD_HERE
keyAlias=footballkey
storeFile=football_predictions.jks
```

#### 4B.3 Build Release APK
```bash
flutter build apk --release
```

**Output location:**
```
build/app/outputs/apk/release/app-release.apk
```

---

## 📱 Step 5: Install on Android Device

### Prerequisites
- Android phone with Android 6.0+ (API 24+)
- USB cable connected to computer
- USB debugging enabled on phone:
  1. Settings → Developer Options (enable in About Phone)
  2. Enable "USB Debugging"

### Installation Methods

#### Method A: Using Flutter
```bash
cd apps/end_user_app

# List connected devices
flutter devices

# Install and run
flutter install  # installs last built APK
```

#### Method B: Direct APK Installation
```bash
# Using ADB (Android Debug Bridge)
adb install build/app/outputs/apk/release/app-release.apk

# Or manually:
# 1. Copy app-release.apk to phone via USB
# 2. Open file manager on phone
# 3. Tap the APK file
# 4. Tap "Install"
```

#### Method C: Manual File Transfer
1. Copy APK to phone storage
2. Use File Manager app to navigate to APK
3. Tap to install
4. Grant permissions when prompted

---

## ✅ Step 6: Verify Installation

### On Your Phone:
1. Find app icon: **Sports Predictions** or **Football Tips**
2. Tap to open
3. Grant permissions (Camera, Storage, etc.)
4. App should open with Firebase data

### If App Crashes:
```bash
# Check logs
adb logcat | grep flutter
```

---

## 🔐 Step 7: Configure Firestore Security Rules

In Firebase Console:
1. Go to **Firestore Database**
2. Click **Rules** tab
3. Replace with:

```firestore
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow public read access
    match /predictions/{category}/matches/{document=**} {
      allow read: if true;
      allow write: if false;
    }
    match /history/{category}/matches/{document=**} {
      allow read: if true;
      allow write: if false;
    }
  }
}
```

4. Click **Publish**

---

## 📊 Step 8: Add Sample Data to Firestore

### Using Firebase Console:
1. Go to **Firestore Database**
2. Click **+ Start collection**
3. Create collection: `predictions`
4. Add sample match document:

```json
{
  "category": "daily",
  "matches": {
    "match_001": {
      "homeTeam": "Manchester United",
      "awayTeam": "Liverpool",
      "league": "Premier League",
      "matchTime": "2026-05-20T15:00:00Z",
      "prediction": "Draw",
      "score": "—",
      "result": "pending",
      "createdAt": "2026-05-18T10:00:00Z"
    }
  }
}
```

Or use the Firestore Console UI to add documents manually.

---

## 🎯 Troubleshooting

### Build Fails: "DefaultFirebaseOptions not found"
```bash
# Re-run flutterfire configure
flutterfire configure --project=<your-project-id>
```

### "SDK version mismatch"
```bash
# Check versions
flutter --version

# Update Flutter
flutter upgrade

# Update pubspec.yaml to match
cd apps/end_user_app
flutter pub upgrade
```

### Device Not Found
```bash
# Check connections
adb devices

# Kill and restart ADB
adb kill-server
adb start-server
```

### App Crashes on Open
```bash
# Check Android logs
adb logcat -s flutter

# Rebuild
flutter clean
flutter pub get
flutter build apk --release
```

### Firebase Auth Errors
- Ensure Firestore Database is created
- Ensure Authentication > Email/Password is enabled
- Check security rules allow read access

---

## 📦 Build Commands Summary

```bash
# Clean build
flutter clean

# Get dependencies
flutter pub get

# Debug build
flutter build apk --debug

# Release build
flutter build apk --release

# Build app bundle (for Google Play)
flutter build appbundle --release

# Run on connected device
flutter run --release

# View all build options
flutter build -h
```

---

## 🎉 Success!

Your Sports Predictions app should now be:
- ✅ Built as APK
- ✅ Installed on your phone
- ✅ Connected to Firebase
- ✅ Ready to use!

### Next Steps:
1. Add more matches to Firestore
2. Configure app theme in `shared/lib/design_system/app_theme.dart`
3. Add more sports categories in `shared/lib/constants/categories.dart`
4. Deploy to Google Play Store

---

## 📚 Additional Resources

- Flutter Docs: https://flutter.dev/docs
- Firebase Flutter Setup: https://firebase.flutter.dev/
- Android Build Guide: https://developer.android.com/studio/build
- Firestore Documentation: https://firebase.google.com/docs/firestore

---

## 💡 Tips

- **Always test on debug APK first** before building release
- **Keep your keystore file safe** - losing it means you can't update the app
- **Check `pubspec.yaml`** for required Flutter/Dart versions
- **Use Firebase emulator** for local testing: `firebase emulators:start`

---

**Happy building! 🚀**
