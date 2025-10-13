# TradingAgents Backend API Specification

**Version**: 1.0
**Last Updated**: October 10, 2025
**Backend Framework**: FastAPI (Python)

---

## 🎯 Overview

This document specifies the REST API and WebSocket interface that the React frontend will consume. The backend wraps the TradingAgents Python framework and exposes it via HTTP and WebSocket protocols.

---

## 🏗️ Backend Architecture

```
┌─────────────────────────────────────────┐
│           Frontend (React)              │
└────────────────┬────────────────────────┘
                 │ HTTP/WebSocket
┌────────────────▼────────────────────────┐
│         FastAPI Application             │
│  ┌─────────────────────────────────┐   │
│  │  REST API Routes                │   │
│  │  - /api/analyze                 │   │
│  │  - /api/portfolio               │   │
│  │  - /api/history                 │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │  WebSocket Server (Socket.io)   │   │
│  │  - Real-time progress updates   │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │  Task Queue (Celery/Redis)      │   │
│  │  - Async analysis execution     │   │
│  └─────────────────────────────────┘   │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│       TradingAgents Framework           │
│  - Multi-agent analysis                 │
│  - LangGraph orchestration              │
└─────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│       Data Persistence Layer            │
│  - PostgreSQL (analysis results)        │
│  - Redis (caching, pub/sub)             │
└─────────────────────────────────────────┘
```

---

## 📡 REST API Endpoints

### Base URL
```
Development: http://localhost:8000
Staging: https://api-staging.tradingagents.com
Production: https://api.tradingagents.com
```

### Authentication
All endpoints require JWT authentication via `Authorization` header:
```
Authorization: Bearer <jwt_token>
```

---

## 1. Analysis Endpoints

### 1.1 Launch Analysis

**POST** `/api/analyze`

Launch a new trading analysis for a given symbol.

**Request Body:**
```json
{
  "symbol": "NVDA",
  "assetType": "equity",
  "date": "2024-10-10",
  "analysts": ["technical", "sentiment", "news", "fundamentals"],
  "config": {
    "researchDepth": 3,
    "llmModel": "gpt-4o-mini",
    "llmProvider": "openai"
  }
}
```

**Request Schema:**
```typescript
interface LaunchAnalysisRequest {
  symbol: string;                    // Stock ticker or crypto symbol
  assetType: 'equity' | 'crypto';   // Asset type
  date: string;                      // ISO date (YYYY-MM-DD)
  analysts: string[];                // List of analysts to run
  config: {
    researchDepth: 1 | 2 | 3 | 4 | 5;  // Number of debate rounds
    llmModel: string;                   // LLM model name
    llmProvider?: string;               // Optional: 'openai', 'anthropic', etc.
  };
}
```

**Response (202 Accepted):**
```json
{
  "success": true,
  "data": {
    "analysisId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "status": "queued",
    "estimatedTime": 180,
    "queuePosition": 2
  },
  "timestamp": "2024-10-10T14:23:45Z"
}
```

**Response Schema:**
```typescript
interface LaunchAnalysisResponse {
  success: boolean;
  data: {
    analysisId: string;      // UUID for tracking
    status: 'queued' | 'running';
    estimatedTime: number;   // Estimated seconds to complete
    queuePosition?: number;  // Position in queue if queued
  };
  timestamp: string;
}
```

**Error Responses:**
- `400 Bad Request`: Invalid input (missing fields, invalid symbol)
- `401 Unauthorized`: Invalid or missing JWT token
- `429 Too Many Requests`: Rate limit exceeded
- `503 Service Unavailable`: Analysis queue full

---

### 1.2 Get Analysis Status

**GET** `/api/analyze/{analysisId}/status`

Get real-time status of a running or completed analysis.

**Path Parameters:**
- `analysisId` (string, required): Analysis UUID

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "status": "running",
    "progress": {
      "currentAgent": "sentiment_analyst",
      "completedAgents": ["technical_analyst"],
      "overallPercent": 25,
      "agents": [
        {
          "name": "technical_analyst",
          "status": "completed",
          "duration": 12
        },
        {
          "name": "sentiment_analyst",
          "status": "running",
          "duration": null
        },
        {
          "name": "news_analyst",
          "status": "pending",
          "duration": null
        }
      ]
    },
    "estimatedTimeRemaining": 135
  },
  "timestamp": "2024-10-10T14:25:12Z"
}
```

**Response Schema:**
```typescript
interface AnalysisStatusResponse {
  success: boolean;
  data: {
    status: 'queued' | 'running' | 'completed' | 'error';
    progress: {
      currentAgent: string;
      completedAgents: string[];
      overallPercent: number;  // 0-100
      agents: Array<{
        name: string;
        status: 'pending' | 'running' | 'completed' | 'error';
        duration?: number;  // seconds
        error?: string;
      }>;
    };
    estimatedTimeRemaining?: number;  // seconds
    error?: string;  // If status is 'error'
  };
  timestamp: string;
}
```

---

### 1.3 Get Analysis Results

**GET** `/api/analyze/{analysisId}/results`

Retrieve complete analysis results (only available when status = 'completed').

**Path Parameters:**
- `analysisId` (string, required): Analysis UUID

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "decision": {
      "symbol": "NVDA",
      "action": "BUY",
      "confidence": 8.5,
      "positionSize": 5,
      "entryPrice": 875.20,
      "stopLoss": 850.00,
      "takeProfit": 920.00,
      "reasoning": "Strong technical momentum combined with positive sentiment...",
      "createdAt": "2024-10-10T14:28:30Z"
    },
    "reports": {
      "technical": "# Technical Analysis\n\n**MACD**: Bullish crossover...",
      "sentiment": "# Sentiment Analysis\n\n**Social Score**: 7.8/10...",
      "news": "# News Analysis\n\n**Key Headlines**: AI chip demand...",
      "fundamentals": "# Fundamental Analysis\n\n**Revenue Growth**: 40% YoY..."
    },
    "debate": {
      "rounds": [
        {
          "roundNumber": 1,
          "bullArgument": "AI demand will drive 40% revenue growth...",
          "bearArgument": "Valuation stretched at 45x P/E...",
          "judgeDecision": "Bull case stronger on fundamentals..."
        }
      ],
      "finalVerdict": "Recommend BUY with 5% position size"
    },
    "riskAssessment": {
      "volatility": "moderate",
      "beta": 1.2,
      "maxDrawdown": 12,
      "liquidity": "excellent",
      "concerns": [
        "Tech sector concentration",
        "China export restrictions"
      ]
    },
    "metadata": {
      "symbol": "NVDA",
      "date": "2024-10-10",
      "completedAt": "2024-10-10T14:28:30Z",
      "duration": 180,
      "analystsUsed": ["technical", "sentiment", "news", "fundamentals"]
    }
  },
  "timestamp": "2024-10-10T14:28:35Z"
}
```

**Response Schema:**
```typescript
interface AnalysisResultsResponse {
  success: boolean;
  data: {
    id: string;
    decision: {
      symbol: string;
      action: 'BUY' | 'SELL' | 'HOLD';
      confidence: number;  // 0-10
      positionSize: number;  // percentage
      entryPrice: number;
      stopLoss: number;
      takeProfit: number;
      reasoning: string;
      createdAt: string;  // ISO timestamp
    };
    reports: {
      [analystName: string]: string;  // Markdown content
    };
    debate: {
      rounds: Array<{
        roundNumber: number;
        bullArgument: string;
        bearArgument: string;
        judgeDecision: string;
      }>;
      finalVerdict: string;
    };
    riskAssessment: {
      volatility: 'low' | 'moderate' | 'high';
      beta?: number;
      maxDrawdown: number;
      liquidity: 'low' | 'moderate' | 'high' | 'excellent';
      concerns: string[];
    };
    metadata: {
      symbol: string;
      date: string;
      completedAt: string;
      duration: number;  // seconds
      analystsUsed: string[];
    };
  };
  timestamp: string;
}
```

**Error Responses:**
- `404 Not Found`: Analysis ID not found
- `425 Too Early`: Analysis not yet completed (status != 'completed')

---

### 1.4 Get Historical Analyses

**GET** `/api/history`

Retrieve historical analyses with optional filtering.

**Query Parameters:**
- `symbol` (string, optional): Filter by symbol (e.g., "NVDA")
- `assetType` (string, optional): Filter by asset type ("equity" | "crypto")
- `days` (number, optional): Number of days to look back (default: 30)
- `limit` (number, optional): Max results to return (default: 50, max: 200)
- `page` (number, optional): Page number for pagination (default: 1)
- `sortBy` (string, optional): Sort field ("date" | "confidence" | "return") (default: "date")
- `sortOrder` (string, optional): Sort order ("asc" | "desc") (default: "desc")

**Example Request:**
```
GET /api/history?symbol=NVDA&days=30&limit=10&sortBy=confidence&sortOrder=desc
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "analyses": [
      {
        "id": "a1b2c3d4-...",
        "symbol": "NVDA",
        "assetType": "equity",
        "action": "BUY",
        "confidence": 8.5,
        "date": "2024-10-10",
        "actualReturn": 5.2,
        "returnPercent": 5.2,
        "createdAt": "2024-10-10T14:28:30Z"
      }
    ],
    "metrics": {
      "totalAnalyses": 15,
      "winRate": 68,
      "avgReturn": 4.2,
      "avgConfidence": 7.8,
      "sharpeRatio": 1.8
    },
    "pagination": {
      "total": 15,
      "page": 1,
      "pageSize": 10,
      "hasNext": true
    }
  },
  "timestamp": "2024-10-10T15:00:00Z"
}
```

---

## 2. Portfolio Endpoints

### 2.1 Get Portfolio

**GET** `/api/portfolio`

Get user's current portfolio with positions and performance.

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "userId": "user123",
    "totalValue": 125430.20,
    "totalReturn": 15530.20,
    "totalReturnPercent": 12.4,
    "positions": [
      {
        "id": "pos1",
        "symbol": "NVDA",
        "assetType": "equity",
        "quantity": 15,
        "avgEntryPrice": 850.00,
        "currentPrice": 875.20,
        "currentValue": 13128.00,
        "returnPercent": 8.2,
        "returnAbsolute": 1020.00,
        "aiStatus": "hold",
        "lastAnalyzedAt": "2024-10-10T14:28:30Z"
      }
    ],
    "performance": {
      "daily": 2.1,
      "weekly": 5.3,
      "monthly": 8.7,
      "yearly": 18.5
    },
    "updatedAt": "2024-10-10T15:30:00Z"
  },
  "timestamp": "2024-10-10T15:30:05Z"
}
```

**Response Schema:**
```typescript
interface PortfolioResponse {
  success: boolean;
  data: {
    userId: string;
    totalValue: number;
    totalReturn: number;
    totalReturnPercent: number;
    positions: Array<{
      id: string;
      symbol: string;
      assetType: 'equity' | 'crypto';
      quantity: number;
      avgEntryPrice: number;
      currentPrice: number;
      currentValue: number;
      returnPercent: number;
      returnAbsolute: number;
      aiStatus: 'hold' | 'review' | 'alert';
      lastAnalyzedAt?: string;
    }>;
    performance: {
      daily: number;
      weekly: number;
      monthly: number;
      yearly: number;
    };
    updatedAt: string;
  };
  timestamp: string;
}
```

---

### 2.2 Get Recommendations

**GET** `/api/portfolio/recommendations`

Get pending AI recommendations for portfolio.

**Response (200 OK):**
```json
{
  "success": true,
  "data": [
    {
      "id": "rec1",
      "analysisId": "a1b2c3d4-...",
      "symbol": "GOOGL",
      "action": "BUY",
      "confidence": 7.8,
      "positionSize": 5,
      "entryPrice": 140.50,
      "stopLoss": 135.00,
      "takeProfit": 150.00,
      "reasoning": "Strong fundamentals with AI integration...",
      "createdAt": "2024-10-10T12:30:00Z",
      "expiresAt": "2024-10-10T18:30:00Z",
      "status": "pending"
    }
  ],
  "timestamp": "2024-10-10T15:35:00Z"
}
```

---

### 2.3 Execute Recommendation

**POST** `/api/portfolio/recommendations/{recommendationId}/execute`

Execute a pending recommendation (buy/sell).

**Path Parameters:**
- `recommendationId` (string, required): Recommendation UUID

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "orderId": "order123",
    "status": "executed",
    "executedAt": "2024-10-10T15:40:00Z",
    "executionPrice": 140.55,
    "message": "Order executed successfully"
  },
  "timestamp": "2024-10-10T15:40:05Z"
}
```

---

### 2.4 Reject Recommendation

**POST** `/api/portfolio/recommendations/{recommendationId}/reject`

Reject a pending recommendation.

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "status": "rejected",
    "rejectedAt": "2024-10-10T15:42:00Z"
  },
  "timestamp": "2024-10-10T15:42:05Z"
}
```

---

## 3. User & Auth Endpoints

### 3.1 Login

**POST** `/api/auth/login`

Authenticate user and get JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "refresh_token_here",
    "expiresIn": 3600,
    "user": {
      "id": "user123",
      "email": "user@example.com",
      "name": "John Doe"
    }
  },
  "timestamp": "2024-10-10T16:00:00Z"
}
```

---

### 3.2 Refresh Token

**POST** `/api/auth/refresh`

Refresh expired JWT token.

**Request Body:**
```json
{
  "refreshToken": "refresh_token_here"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "token": "new_jwt_token_here",
    "expiresIn": 3600
  },
  "timestamp": "2024-10-10T16:30:00Z"
}
```

---

## 🔌 WebSocket API

### Connection

**URL**: `ws://localhost:8000/ws` (or `wss://api.tradingagents.com/ws` in production)

**Authentication**: Include JWT token in connection query:
```javascript
const socket = io('ws://localhost:8000', {
  auth: { token: 'your_jwt_token' }
});
```

---

### Events

#### 1. Subscribe to Analysis

**Client → Server**

```javascript
socket.emit('subscribe_analysis', {
  analysisId: 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
});
```

#### 2. Analysis Progress Update

**Server → Client**

```javascript
socket.on('analysis_progress', (data) => {
  console.log(data);
});
```

**Data Schema:**
```json
{
  "analysisId": "a1b2c3d4-...",
  "agent": "sentiment_analyst",
  "status": "completed",
  "progress": 50,
  "message": "Sentiment analysis completed",
  "timestamp": "2024-10-10T14:25:30Z"
}
```

#### 3. Analysis Complete

**Server → Client**

```javascript
socket.on('analysis_complete', (data) => {
  console.log(data);
});
```

**Data Schema:**
```json
{
  "analysisId": "a1b2c3d4-...",
  "status": "completed",
  "decision": {
    "action": "BUY",
    "confidence": 8.5
  },
  "timestamp": "2024-10-10T14:28:30Z"
}
```

#### 4. Analysis Error

**Server → Client**

```javascript
socket.on('analysis_error', (data) => {
  console.error(data);
});
```

**Data Schema:**
```json
{
  "analysisId": "a1b2c3d4-...",
  "error": "API rate limit exceeded",
  "agent": "news_analyst",
  "timestamp": "2024-10-10T14:27:00Z"
}
```

#### 5. Unsubscribe from Analysis

**Client → Server**

```javascript
socket.emit('unsubscribe_analysis', {
  analysisId: 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
});
```

---

## 📊 Backend Implementation Checklist

### FastAPI Setup
- [ ] Initialize FastAPI project
- [ ] Setup SQLAlchemy + PostgreSQL
- [ ] Configure Redis for caching/pub-sub
- [ ] Implement JWT authentication
- [ ] Setup CORS middleware
- [ ] Add rate limiting

### Analysis Service
- [ ] Create analysis task queue (Celery)
- [ ] Implement analysis orchestration
- [ ] Integrate TradingAgents framework
- [ ] Add WebSocket progress broadcasting
- [ ] Store results in PostgreSQL

### Portfolio Service
- [ ] Create portfolio database models
- [ ] Implement position tracking
- [ ] Build recommendation system
- [ ] Add broker integration (optional)

### WebSocket Server
- [ ] Setup Socket.io server
- [ ] Implement room-based subscriptions
- [ ] Add Redis pub/sub for scaling
- [ ] Handle connection/disconnection

### Testing
- [ ] Unit tests for services
- [ ] Integration tests for API
- [ ] WebSocket flow tests
- [ ] Load testing (k6)

---

## 🚀 Sample Backend Code

### FastAPI Main Application

```python
# main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import socketio

from .database import get_db
from .auth import get_current_user
from .routers import analyze, portfolio, auth

app = FastAPI(title="TradingAgents API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Socket.io
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio, app)

# Routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(analyze.router, prefix="/api/analyze", tags=["analysis"])
app.include_router(portfolio.router, prefix="/api/portfolio", tags=["portfolio"])

@app.get("/")
def root():
    return {"message": "TradingAgents API v1.0"}

# WebSocket events
@sio.on('subscribe_analysis')
async def subscribe_analysis(sid, data):
    analysis_id = data.get('analysisId')
    await sio.enter_room(sid, f"analysis_{analysis_id}")
    print(f"Client {sid} subscribed to analysis {analysis_id}")

@sio.on('unsubscribe_analysis')
async def unsubscribe_analysis(sid, data):
    analysis_id = data.get('analysisId')
    await sio.leave_room(sid, f"analysis_{analysis_id}")
    print(f"Client {sid} unsubscribed from analysis {analysis_id}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(socket_app, host="0.0.0.0", port=8000)
```

### Analysis Router

```python
# routers/analyze.py

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import uuid

from ..database import get_db
from ..auth import get_current_user
from ..schemas import LaunchAnalysisRequest, AnalysisResponse
from ..services.analysis_service import run_analysis

router = APIRouter()

@router.post("/", response_model=AnalysisResponse)
async def launch_analysis(
    request: LaunchAnalysisRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Generate analysis ID
    analysis_id = str(uuid.uuid4())

    # Queue analysis task
    background_tasks.add_task(
        run_analysis,
        analysis_id=analysis_id,
        symbol=request.symbol,
        asset_type=request.assetType,
        date=request.date,
        analysts=request.analysts,
        config=request.config,
        user_id=current_user.id
    )

    return {
        "success": True,
        "data": {
            "analysisId": analysis_id,
            "status": "queued",
            "estimatedTime": 180
        }
    }

@router.get("/{analysis_id}/status")
async def get_analysis_status(
    analysis_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Fetch from database or Redis cache
    # Return current status
    pass

@router.get("/{analysis_id}/results")
async def get_analysis_results(
    analysis_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Fetch results from database
    # Return complete analysis
    pass
```

---

## 📈 Performance Targets

- **API Response Time**: < 200ms (p95)
- **Analysis Execution**: 2-5 minutes
- **WebSocket Latency**: < 100ms
- **Concurrent Analyses**: 50+
- **Request Rate Limit**: 100 req/min per user

---

## 🔐 Security

- JWT expiration: 1 hour
- Refresh token expiration: 7 days
- Rate limiting: 100 req/min per user
- HTTPS only in production
- SQL injection prevention (parameterized queries)
- XSS protection (sanitize inputs)

---

**Backend Developer**: Implement this spec
**Frontend Developer**: Consume these APIs
**Last Review**: October 10, 2025
