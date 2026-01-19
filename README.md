# SATYA-VERIFY 🔍

**AI-Powered Misinformation Fact-Checking Platform for Indian Regional News**

SATYA-VERIFY is an intelligent fact-checking platform designed to combat misinformation in Indian regional languages. It leverages advanced AI and NLP technologies to verify news content from text, images, and URLs, cross-referencing claims against trusted Indian news sources.

---

## 🎯 Project Overview

SATYA-VERIFY addresses the critical challenge of misinformation in India's multilingual digital landscape by:

- **Multi-format Input Support**: Verify content from text, images (OCR), and URLs
- **Multilingual Processing**: Supports Hindi, English, Tamil, Telugu, Bengali, Kannada, Malayalam, Marathi, and Mixed languages
- **AI-Powered Analysis**: Uses advanced LLMs (GPT-5.2) for claim extraction, language detection, and verification
- **Trusted Source Verification**: Cross-references claims against established Indian fact-checking organizations (PIB Fact Check, Alt News, BoomLive, The Hindu, PTI)
- **Credibility Scoring**: Rates sources and provides confidence levels for each verdict
- **Real-time Results**: Delivers comprehensive fact-check reports with supporting and contradicting evidence

---

## 🏗️ System Architecture

```
┌─────────────────┐
│   User Input    │
│ (Text/Image/URL)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Frontend      │
│   (React)       │◄──────┐
└────────┬────────┘       │
         │                │
         ▼                │
┌─────────────────┐       │
│  FastAPI Server │       │
│   (Backend)     │       │
└────────┬────────┘       │
         │                │
         ▼                │
    ┌────────────────┐    │
    │  OCR Service   │    │
    │  (Image→Text)  │    │
    └────────────────┘    │
         │                │
         ▼                │
    ┌────────────────┐    │
    │  NLP Service   │    │
    │ - Language Det │    │
    │ - Translation  │    │
    │ - Claim Extract│    │
    └────────────────┘    │
         │                │
         ▼                │
    ┌────────────────┐    │
    │ Verification   │    │
    │   Service      │    │
    │ - Source Search│    │
    │ - Similarity   │    │
    │ - Verdict      │    │
    └────────────────┘    │
         │                │
         ▼                │
    ┌────────────────┐    │
    │ Credibility    │    │
    │   Service      │    │
    │ - Source Rating│    │
    └────────────────┘    │
         │                │
         ▼                │
    ┌────────────────┐    │
    │   MongoDB      │    │
    │  (Database)    │    │
    └────────────────┘    │
         │                │
         └────────────────┘
```

**Flow**:
1. User submits content (text/image/URL)
2. Frontend sends request to backend API
3. OCR extracts text from images (if applicable)
4. NLP detects language and translates to English
5. AI extracts verifiable claims from content
6. Verification service searches trusted sources
7. Semantic similarity and credibility analysis performed
8. Final verdict determined (TRUE/FALSE/MISLEADING/UNVERIFIED)
9. Results stored in MongoDB and returned to user

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: React 19.0.0
- **Build Tool**: Create React App with CRACO
- **Styling**: Tailwind CSS 3.4.17
- **UI Components**: Radix UI (comprehensive component library)
- **State Management**: React Hooks
- **HTTP Client**: Axios 1.8.4
- **Routing**: React Router DOM 7.5.1
- **Animation**: Framer Motion 12.27.0

### Backend
- **Framework**: FastAPI 0.110.1
- **Runtime**: Python (async/await with uvicorn)
- **Database**: MongoDB (via Motor 3.3.1 - async driver)
- **AI/NLP**: 
  - emergentintegrations 0.1.0 (LLM integration)
  - OpenAI GPT-5.2 (via Emergent LLM Key)
  - scikit-learn 1.8.0 (embeddings, similarity)
- **Image Processing**: Pillow 12.1.0
- **OCR**: GPT-5.2 Vision API
- **Data Models**: Pydantic 2.12.5

### Database
- **MongoDB 27017** (local instance)
- **Collections**: articles, claims, verification_results

### Key Python Libraries
- `motor` - Async MongoDB driver
- `emergentintegrations` - Unified LLM API
- `beautifulsoup4` - HTML parsing
- `numpy`, `pandas` - Data processing
- `scikit-learn` - ML utilities (embeddings, cosine similarity)

---

## 📁 Repository Structure

```
satya-verify-repo/
│
├── backend/                      # FastAPI backend application
│   ├── server.py                 # Main API server with endpoints
│   ├── models.py                 # Pydantic data models
│   ├── nlp_service.py            # Language detection, translation, claim extraction
│   ├── ocr_service.py            # Image text extraction
│   ├── verification_service.py   # Claim verification logic
│   ├── credibility_service.py    # Source credibility rating
│   ├── requirements.txt          # Python dependencies
│   └── .env                      # Backend environment variables
│
├── frontend/                     # React frontend application
│   ├── public/                   # Static assets
│   ├── src/
│   │   ├── App.js                # Main application component
│   │   ├── App.css               # Application styles
│   │   ├── index.js              # React entry point
│   │   ├── index.css             # Global styles
│   │   ├── components/
│   │   │   ├── HomePage.js       # Input form page
│   │   │   ├── ResultsPage.js    # Verification results display
│   │   │   └── ui/               # Reusable UI components (Radix)
│   │   ├── hooks/
│   │   │   └── use-toast.js      # Toast notification hook
│   │   └── lib/
│   │       └── utils.js          # Utility functions
│   ├── package.json              # Node dependencies
│   ├── tailwind.config.js        # Tailwind configuration
│   ├── postcss.config.js         # PostCSS configuration
│   ├── craco.config.js           # Create React App configuration
│   └── .env                      # Frontend environment variables
│
├── tests/                        # Test directory
│   └── __init__.py
│
└── README.md                     # This file
```

### Key Files Explained

**Backend:**
- `server.py` - Main FastAPI application with 5 endpoints (/verify, /history, /sources, /stats, /)
- `models.py` - Defines data schemas (InputArticle, Claim, VerificationResult, etc.)
- `nlp_service.py` - Handles language detection, translation (8+ Indian languages), and claim extraction using GPT-5.2
- `ocr_service.py` - Extracts text from images using GPT-5.2 Vision API
- `verification_service.py` - Core verification logic: searches trusted sources, calculates semantic similarity, determines verdicts
- `credibility_service.py` - Maintains credibility scores for 20+ Indian news sources

**Frontend:**
- `HomePage.js` - User input form (text/image/URL upload)
- `ResultsPage.js` - Displays verification results with verdicts, confidence scores, and source evidence

---

## ⚙️ Setup Instructions

### Prerequisites

Before setting up the project, ensure you have:

- **Python 3.8+** (recommended: Python 3.10 or higher)
- **Node.js 16+** and **Yarn** (for frontend)
- **MongoDB 4.4+** (running locally or via Docker)
- **Git** (for cloning the repository)

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/Yuvrajps06/satya-verify.git
cd satya-verify
```

#### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

#### 3. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install Node dependencies using Yarn
yarn install
```

#### 4. Database Setup

**Option A: Local MongoDB**
```bash
# Install MongoDB (if not already installed)
# Ubuntu/Debian:
sudo apt-get install mongodb

# macOS (using Homebrew):
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB service
sudo systemctl start mongodb  # Ubuntu/Debian
brew services start mongodb-community  # macOS

# Verify MongoDB is running
mongosh --eval "db.version()"
```

**Option B: MongoDB via Docker**
```bash
docker run -d -p 27017:27017 --name satya-verify-mongo mongo:latest
```

---

## 🔐 Environment Variables

### Backend `.env` File

Create `/backend/.env` with the following variables:

```env
# MongoDB Connection
MONGO_URL=mongodb://localhost:27017
DB_NAME=satya_verify_db

# CORS Configuration
CORS_ORIGINS=*

# Emergent LLM API Key (required for AI features)
EMERGENT_LLM_KEY=your_api_key_here
```

**Important Notes:**
- `EMERGENT_LLM_KEY` is **REQUIRED** for all AI features (language detection, translation, claim extraction, verification)
- Get your API key from [Emergent Platform](https://emergent.sh)
- `MONGO_URL` should point to your MongoDB instance (default: localhost:27017)
- `DB_NAME` specifies the database name (can be any name you prefer)

### Frontend `.env` File

Create `/frontend/.env` with:

```env
# Backend API URL
REACT_APP_BACKEND_URL=http://localhost:8001

# WebSocket Port (for development)
WDS_SOCKET_PORT=3000

# Health Check
ENABLE_HEALTH_CHECK=false
```

**Important Notes:**
- `REACT_APP_BACKEND_URL` must point to your backend server (default: http://localhost:8001)
- Ensure the backend is running before starting the frontend
- All environment variables must be prefixed with `REACT_APP_` to be accessible in React

### `.env.example` Files

**Backend `.env.example`:**
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=satya_verify_db
CORS_ORIGINS=*
EMERGENT_LLM_KEY=your_emergent_llm_key_here
```

**Frontend `.env.example`:**
```env
REACT_APP_BACKEND_URL=http://localhost:8001
WDS_SOCKET_PORT=3000
ENABLE_HEALTH_CHECK=false
```

---

## 🚀 Running the Application

### Start Backend Server

```bash
cd backend
source venv/bin/activate  # Activate virtual environment
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

The backend API will be accessible at: **http://localhost:8001**
API Documentation (Swagger): **http://localhost:8001/docs**

### Start Frontend Server

In a **new terminal window**:

```bash
cd frontend
yarn start
```

**Expected Output:**
```
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

The frontend will open automatically at: **http://localhost:3000**

### Start Full System (Both Services)

You can run both services using separate terminal windows or use a process manager like `tmux` or `screen`:

**Terminal 1 (Backend):**
```bash
cd backend && uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend && yarn start
```

**Alternative: Using `tmux`**
```bash
# Start backend in background
tmux new-session -d -s backend 'cd backend && uvicorn server:app --host 0.0.0.0 --port 8001 --reload'

# Start frontend in background
tmux new-session -d -s frontend 'cd frontend && yarn start'

# Attach to see logs
tmux attach -t backend  # CTRL+B then D to detach
tmux attach -t frontend
```

---

## 💡 Sample Usage

### Example 1: Verify Text Content

**Input:**
```
Prime Minister announced a new scheme providing ₹5000 monthly to all farmers in India.
```

**Process:**
1. Navigate to http://localhost:3000
2. Select "Text" input type
3. Paste the claim
4. Click "Verify"

**Sample Output:**
```json
{
  "article_id": "abc-123",
  "detected_language": "English",
  "claims": [
    {
      "claim_text": "Prime Minister announced a new scheme providing ₹5000 monthly to all farmers",
      "verdict": "FALSE",
      "confidence": 85,
      "explanation": "Multiple trusted sources contradict this claim. The actual scheme provides different amounts...",
      "supporting_sources": [],
      "contradicting_sources": [
        {
          "source_name": "PIB Fact Check",
          "source_url": "https://factcheck.pib.gov.in/...",
          "credibility_score": 95,
          "relevant_text": "This claim is false..."
        }
      ]
    }
  ],
  "overall_assessment": "This content contains false claims and is likely misinformation."
}
```

### Example 2: Verify Image Content (Hindi Text)

**Input:** Upload an image containing Hindi news text

**Process:**
1. Select "Image" input type
2. Upload image file (JPG/PNG)
3. Click "Verify"

**What Happens:**
- OCR extracts Hindi text from image
- Language detected as "Hindi"
- Text translated to English
- Claims extracted and verified
- Results displayed with original Hindi text + English translation

### Example 3: Check Verification History

Navigate to: http://localhost:8001/api/history

**Sample Response:**
```json
{
  "history": [
    {
      "id": "xyz-789",
      "input_type": "text",
      "detected_language": "Hindi",
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ],
  "count": 1
}
```

---

## 🧪 Testing

### Backend Testing

#### 1. Test API Health

```bash
curl http://localhost:8001/api/
```

**Expected Response:**
```json
{
  "message": "SATYA-VERIFY API",
  "version": "1.0.0",
  "description": "AI-powered misinformation fact-checking for Indian regional news"
}
```

#### 2. Test Verification Endpoint

```bash
curl -X POST http://localhost:8001/api/verify \
  -H "Content-Type: application/json" \
  -d '{
    "input_type": "text",
    "content": "Test news claim about India"
  }'
```

#### 3. Test Database Connection

```bash
# Check MongoDB is running
mongosh --eval "db.adminCommand('ping')"

# Connect to database
mongosh
use satya_verify_db
show collections
```

### Frontend Testing

#### Manual UI Testing
1. Open http://localhost:3000
2. Test text input verification
3. Test image upload (use sample image with text)
4. Check results page display
5. Verify back navigation

#### Check Console for Errors
Open browser DevTools (F12) → Console tab → Look for any errors

### Integration Testing

Run a complete end-to-end test:

```bash
# 1. Ensure MongoDB is running
mongosh --eval "db.version()"

# 2. Start backend
cd backend && uvicorn server:app --port 8001 &

# 3. Wait for backend to start (5 seconds)
sleep 5

# 4. Test API
curl http://localhost:8001/api/

# 5. Start frontend
cd ../frontend && yarn start
```

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. **Backend fails to start**

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

---

**Error:** `pymongo.errors.ServerSelectionTimeoutError: localhost:27017: [Errno 111] Connection refused`

**Solution:** MongoDB is not running
```bash
# Ubuntu/Debian
sudo systemctl start mongodb
sudo systemctl status mongodb

# macOS
brew services start mongodb-community

# Docker
docker start satya-verify-mongo
```

---

**Error:** `KeyError: 'EMERGENT_LLM_KEY'`

**Solution:** Missing API key in `.env`
```bash
cd backend
echo "EMERGENT_LLM_KEY=your_key_here" >> .env
```

---

#### 2. **Frontend fails to start**

**Error:** `command not found: yarn`

**Solution:** Install Yarn
```bash
npm install -g yarn
```

---

**Error:** `Module not found: Can't resolve '@/components/HomePage'`

**Solution:** Install dependencies
```bash
cd frontend
yarn install
```

---

**Error:** `EADDRINUSE: address already in use :::3000`

**Solution:** Port 3000 is occupied
```bash
# Find and kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or use a different port
PORT=3001 yarn start
```

---

#### 3. **API Connection Issues**

**Error:** Frontend shows "Network Error" or "Failed to fetch"

**Solution:** Check backend URL in frontend `.env`
```bash
cd frontend
cat .env
# Ensure REACT_APP_BACKEND_URL=http://localhost:8001
```

**Solution:** Check if backend is running
```bash
curl http://localhost:8001/api/
```

**Solution:** Check CORS settings in backend `.env`
```bash
cd backend
# Ensure CORS_ORIGINS=*
```

---

#### 4. **Database Connection Issues**

**Error:** `Database connection failed`

**Solution:** Verify MongoDB is accessible
```bash
mongosh mongodb://localhost:27017
```

**Solution:** Check MongoDB logs
```bash
# Ubuntu/Debian
sudo journalctl -u mongodb

# macOS
tail -f /usr/local/var/log/mongodb/mongo.log
```

---

#### 5. **AI/LLM Features Not Working**

**Error:** `LLM API call failed` or `Authentication failed`

**Solution:** Verify EMERGENT_LLM_KEY is valid
```bash
cd backend
cat .env | grep EMERGENT_LLM_KEY
```

**Solution:** Test API key
```bash
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('Key found:', bool(os.environ.get('EMERGENT_LLM_KEY')))
"
```

---

#### 6. **Port Conflicts**

**Issue:** Backend or frontend won't start due to port in use

**Solution for Backend (8001):**
```bash
# Find process using port 8001
lsof -i :8001

# Kill the process
kill -9 <PID>

# Or use a different port
uvicorn server:app --host 0.0.0.0 --port 8002
```

**Solution for Frontend (3000):**
```bash
# Use a different port
PORT=3001 yarn start
```

---

#### 7. **Image Upload Not Working**

**Error:** `Could not extract text from image`

**Solution:** Ensure image is valid base64 or file upload is working
- Check image size (should be < 5MB)
- Verify image format (JPG, PNG, WEBP supported)
- Check browser console for errors

---

#### 8. **Slow Response Times**

**Issue:** Verification takes too long

**Reasons:**
- LLM API calls can take 10-30 seconds
- Multiple claims require multiple API calls
- Semantic similarity calculations are compute-intensive

**Solution:** This is expected behavior for MVP. For production:
- Implement caching
- Use batch processing
- Add loading indicators (already present in UI)

---

## 🎓 Final-Year Project Notes

This project demonstrates:

✅ **Full-stack Development**: React frontend + FastAPI backend + MongoDB database  
✅ **AI/ML Integration**: GPT-5.2 for NLP, vision, embeddings  
✅ **Real-world Problem Solving**: Addressing misinformation in Indian regional languages  
✅ **API Design**: RESTful APIs with proper error handling  
✅ **Async Programming**: Efficient async/await patterns in Python  
✅ **Modern UI/UX**: Tailwind CSS + Radix UI components  
✅ **Multilingual Support**: 8+ Indian languages supported  
✅ **Credibility Analysis**: Source rating and reputation scoring  

### Key Features for Demo:
1. **Live Fact-Checking**: Show real-time verification of a news claim
2. **Multilingual Support**: Verify Hindi/Tamil text and show translation
3. **Image OCR**: Upload image with text and extract claims
4. **Source Credibility**: Display trusted sources with credibility scores
5. **Verdict Explanation**: AI-generated explanations for each verdict

### Presentation Highlights:
- **Problem Statement**: Misinformation in Indian regional languages
- **Solution Approach**: AI-powered verification with trusted sources
- **Technical Architecture**: Modern async stack with LLM integration
- **Results**: Accurate verdicts with confidence scores and source citations
- **Future Scope**: Real-time monitoring, browser extension, WhatsApp bot

---

## 📊 API Endpoints Reference

| Endpoint | Method | Description | Input | Output |
|----------|--------|-------------|-------|--------|
| `/api/` | GET | API information | None | API metadata |
| `/api/verify` | POST | Verify content | `{input_type, content}` | Verification results |
| `/api/history` | GET | Get verification history | `?limit=20` | List of articles |
| `/api/sources` | GET | Get trusted sources | None | List of sources |
| `/api/stats` | GET | Get platform statistics | None | Stats object |

---

## 📜 License

This project is open-source and available for educational purposes.

---

## 👥 Contributors

- **Yuvraj** - Project Lead & Developer

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review MongoDB and API logs
3. Verify all environment variables are set correctly
4. Ensure all dependencies are installed

---

## 🚀 Future Enhancements

- [ ] Real-time news monitoring via RSS feeds
- [ ] Browser extension for instant fact-checking
- [ ] WhatsApp/Telegram bot integration
- [ ] Advanced caching for faster responses
- [ ] User authentication and personalized history
- [ ] Fact-check report generation (PDF export)
- [ ] Multi-source aggregation dashboard
- [ ] Mobile app (React Native)

---

**Built with ❤️ for combating misinformation in India**
