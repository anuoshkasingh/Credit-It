# Credit-It 💳✨
### AI-Powered Credit Card Recommendation & Personalized Financial Assistant

**Credit-It** is a modern Flutter mobile application with an optional Python/FastAPI backend designed to help users maximize their credit card rewards and savings. By analyzing user spending behaviors across merchant categories, Credit-It calculates personalized net annual savings for 90+ Indian credit cards and provides a friendly, personalized floating AI Assistant powered by Google Gemini.

---

## 🌟 Key Features

- **🎯 Smart AI Card Recommendations**:
  - Evaluates cards across 5 distinct spending categories: `All`, `Shopping`, `Travel`, `Utilities`, and `Food`.
  - Computes net annual value (gross rewards minus annual fees) based on actual spending behavior.

- **🤖 Credit It Assistant (Floating Chatbot)**:
  - Personal AI financial advisor built directly into the app using Google Gemini REST API.
  - Explains recommendation logic, compares specific cards according to user spending, clarifies terms like *5X rewards* or *Lounge Access*, and outputs clean plain-text responses.
  - Features dynamic soft keyboard avoidance, out-of-bounds tap-dismissal, and automatic search history cleanup when switching user profiles.

- **📊 100-Transaction History View**:
  - Displays 100 real, month-grouped transactions per user profile with real-time search filtering.

- **👥 Multi-Profile Switcher**:
  - Pre-configured spending profiles to test recommendations:
    1. **High Spender** (~₹18L Income / ₹14L Spend) — Travel, Fine Dining, Luxury Shopping.
    2. **Family Spender** (~₹5.5L Income / ₹3L Spend) — Groceries, Swiggy, Airtel Bills, Myntra.
    3. **Youth / Student** (~₹1.8L Income / ₹75k Spend) — Campus Food, Metro Rail, Mobile Recharges.

- **📝 Bank Issuer Direct Links & Application Flow**:
  - Direct application links to official bank issuer portals (ICICI, HDFC, Axis, SBI, Amex, AU, IDFC, OneCard, etc.).

- **⚙️ Live API Key Settings**:
  - In-app settings screen (`Profile → API Settings`) allowing users to easily configure and persist their own Google Gemini API key.

- **🚀 Standalone Mobile Engine**:
  - Built-in offline recommendation engine allows the mobile app to run seamlessly even without starting the Python backend server.

---

## 📁 Repository Structure

```
credit_it/
├── flutter_app/                # Flutter Mobile Application Source Code
│   ├── lib/
│   │   ├── app/
│   │   │   ├── models/        # Data models (CreditCard, User, Recommendation, etc.)
│   │   │   ├── providers/     # State management (UserProvider, ChatbotProvider)
│   │   │   ├── screens/       # App screens (Home, Cards AI, Details, History, API Settings)
│   │   │   ├── services/      # ApiService, ChatbotService, ApiKeyService
│   │   │   ├── theme/         # Paytm-inspired blue/white design theme
│   │   │   └── widgets/       # Reusable components & FloatingChatbotWidget
│   │   └── main.dart
│   └── assets/                # Credit card imagery assets
└── backend/                   # Python FastAPI Backend Server
    ├── main.py                # REST API endpoints
    ├── database.py            # SQLite database queries & spending analysis
    ├── recommendation.py      # Backend Gemini recommendation algorithm
    └── seed_data.py           # Database tables creation & 300+ sample transactions seed script
```

---

## 🛠️ Quick Start & Setup Guide

### 1. Flutter Mobile Application

#### Prerequisites
- Flutter SDK (`>=3.0.0`)
- Android Studio / VS Code with Flutter extension
- Android Emulator or physical device

#### Steps
```bash
# Navigate to flutter_app directory
cd flutter_app

# Fetch dependencies
flutter pub get

# Run on connected device or emulator
flutter run
```

---

### 2. Gemini AI Assistant Configuration

To use the **Credit It Assistant** floating chatbot:
1. Obtain a free Gemini API Key from [Google AI Studio](https://aistudio.google.com/).
2. In the running app, tap **Profile Icon** (Top-Left) or open **Cards AI** screen.
3. Tap **API Settings** (or the gear icon inside the chatbot header).
4. Enter your Gemini API key and tap **Save API Key**.

---

### 3. Python FastAPI Backend (Optional)

#### Prerequisites
- Python 3.9+

#### Steps
```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install fastapi uvicorn google-generativeai pydantic

# Seed SQLite database with sample transactions & card master data
python seed_data.py

# Launch FastAPI server
python main.py
```
The backend API server will start on `http://localhost:8000`.

---

## 🎨 Tech Stack & Frameworks

- **Mobile Client**: Flutter (Dart), Provider state management, `http`, `shared_preferences`.
- **Backend Service**: FastAPI (Python 3.9+), Uvicorn, SQLite3.
- **AI Engine**: Google Gemini API (`gemini-1.5-flash` direct REST & Python SDK integration).
- **Design System**: Paytm-inspired Paytm Navy Blue & White palette with modern card elevation and glassmorphic overlays.

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
