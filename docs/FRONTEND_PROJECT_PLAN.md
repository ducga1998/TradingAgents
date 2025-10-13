# TradingAgents Dashboard - Frontend Project Plan

**Project Manager**: Planning Document
**Last Updated**: October 10, 2025
**Status**: Planning Phase
**Tech Stack**: React.js + Next.js 14 + TypeScript

---

## 📋 Executive Summary

Build a modern, real-time web dashboard for the TradingAgents multi-agent trading system. The frontend will provide an intuitive interface for launching analyses, monitoring agent execution, viewing trading decisions, and tracking portfolio performance.

**Key Objectives**:
- ✅ Enable non-technical users to interact with AI trading agents
- ✅ Provide real-time visibility into multi-agent analysis pipeline
- ✅ Display actionable trading recommendations with risk metrics
- ✅ Track historical performance and agent accuracy
- ✅ Support both equities and cryptocurrency trading

---

## 🎯 Project Scope

### **In Scope**
- Web-based dashboard (desktop + tablet responsive)
- Real-time analysis execution and progress tracking
- Multi-agent decision visualization
- Portfolio management interface
- Historical analysis library
- Performance analytics
- API integration with Python backend

### **Out of Scope (Future Phases)**
- Native mobile apps (iOS/Android)
- Direct broker integration (will use backend APIs)
- Live trading automation (backend handles execution)
- Custom strategy builder UI
- Social trading / community features

---

## 🏗️ Technical Architecture

### **Frontend Stack**

```
┌─────────────────────────────────────────┐
│           React 18.3 + TypeScript       │
├─────────────────────────────────────────┤
│  Next.js 14 (App Router)                │
│  - Server Components for SEO            │
│  - API Routes for backend proxy         │
│  - Streaming for real-time updates      │
├─────────────────────────────────────────┤
│  State Management                       │
│  - Zustand (global state)               │
│  - TanStack Query (server state)        │
│  - WebSocket (real-time events)         │
├─────────────────────────────────────────┤
│  UI Components                          │
│  - Tailwind CSS (styling)               │
│  - shadcn/ui (component library)        │
│  - Radix UI (primitives)                │
│  - Framer Motion (animations)           │
├─────────────────────────────────────────┤
│  Data Visualization                     │
│  - TradingView Lightweight Charts       │
│  - Recharts (analytics)                 │
│  - React Table (data grids)             │
├─────────────────────────────────────────┤
│  Development Tools                      │
│  - Vite (dev server)                    │
│  - ESLint + Prettier (code quality)     │
│  - Vitest + React Testing Library       │
└─────────────────────────────────────────┘
```

### **Backend Integration**

```
Frontend (Next.js)  ←→  Backend API (FastAPI/Flask)  ←→  TradingAgents (Python)
                          ↓
                    PostgreSQL Database
                          ↓
                    Redis (real-time cache)
                          ↓
                    WebSocket Server (Socket.io)
```

**API Communication**:
- REST API for CRUD operations
- WebSocket for live analysis progress
- Server-Sent Events (SSE) for streaming updates
- JWT authentication

---

## 📁 Project Structure

```
frontend/
├── public/                          # Static assets
│   ├── icons/
│   └── images/
│
├── src/
│   ├── app/                         # Next.js App Router
│   │   ├── (dashboard)/             # Dashboard routes
│   │   │   ├── page.tsx            # Main dashboard
│   │   │   ├── analysis/           # Analysis views
│   │   │   ├── portfolio/          # Portfolio management
│   │   │   └── history/            # Historical analyses
│   │   ├── api/                    # API routes (proxy)
│   │   │   ├── analyze/
│   │   │   ├── portfolio/
│   │   │   └── websocket/
│   │   └── layout.tsx              # Root layout
│   │
│   ├── components/                  # React components
│   │   ├── ui/                     # shadcn/ui components
│   │   ├── dashboard/              # Dashboard-specific
│   │   │   ├── AnalysisLauncher.tsx
│   │   │   ├── ProgressTracker.tsx
│   │   │   ├── DecisionCard.tsx
│   │   │   ├── DebateViewer.tsx
│   │   │   └── PortfolioOverview.tsx
│   │   ├── charts/                 # Chart components
│   │   │   ├── PriceChart.tsx
│   │   │   ├── PerformanceChart.tsx
│   │   │   └── RiskHeatmap.tsx
│   │   └── shared/                 # Reusable components
│   │       ├── Header.tsx
│   │       ├── Sidebar.tsx
│   │       └── LoadingStates.tsx
│   │
│   ├── lib/                        # Utilities
│   │   ├── api/                    # API clients
│   │   │   ├── trading-agents.ts
│   │   │   ├── portfolio.ts
│   │   │   └── websocket.ts
│   │   ├── hooks/                  # Custom hooks
│   │   │   ├── useAnalysis.ts
│   │   │   ├── usePortfolio.ts
│   │   │   └── useWebSocket.ts
│   │   ├── utils/                  # Helper functions
│   │   │   ├── formatters.ts
│   │   │   ├── validators.ts
│   │   │   └── calculations.ts
│   │   └── constants/              # Constants
│   │       ├── config.ts
│   │       └── types.ts
│   │
│   ├── stores/                     # Zustand stores
│   │   ├── analysis-store.ts
│   │   ├── portfolio-store.ts
│   │   └── ui-store.ts
│   │
│   ├── types/                      # TypeScript types
│   │   ├── analysis.ts
│   │   ├── portfolio.ts
│   │   └── agent.ts
│   │
│   └── styles/                     # Global styles
│       └── globals.css
│
├── tests/                          # Test files
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── .env.example                    # Environment template
├── .env.local                      # Local environment
├── next.config.js                  # Next.js config
├── tailwind.config.js              # Tailwind config
├── tsconfig.json                   # TypeScript config
└── package.json                    # Dependencies
```

---

## 🎨 Component Architecture

### **Core Components**

#### 1. **AnalysisLauncher** (`components/dashboard/AnalysisLauncher.tsx`)
```typescript
interface AnalysisLauncherProps {
  onLaunch: (config: AnalysisConfig) => Promise<string>; // Returns analysis_id
}

type AnalysisConfig = {
  symbol: string;
  assetType: 'equity' | 'crypto';
  date: Date;
  analysts: Analyst[];
  researchDepth: 1 | 2 | 3 | 4 | 5;
  llmModel: string;
}
```

**Features**:
- Asset search with autocomplete
- Analyst team selection (checkboxes)
- Saved configuration presets
- Validation before launch

---

#### 2. **ProgressTracker** (`components/dashboard/ProgressTracker.tsx`)
```typescript
interface ProgressTrackerProps {
  analysisId: string;
  onComplete: (results: AnalysisResults) => void;
}

type AgentStatus = 'pending' | 'running' | 'completed' | 'error';

type ProgressState = {
  agents: Array<{
    name: string;
    status: AgentStatus;
    duration?: number;
    error?: string;
  }>;
  overall: number; // 0-100
  estimatedTime?: number;
}
```

**Features**:
- Real-time WebSocket updates
- Per-agent status indicators
- Progress bar with ETA
- Error handling with retry

---

#### 3. **DecisionCard** (`components/dashboard/DecisionCard.tsx`)
```typescript
interface DecisionCardProps {
  decision: TradingDecision;
  expanded?: boolean;
}

type TradingDecision = {
  symbol: string;
  action: 'BUY' | 'SELL' | 'HOLD';
  confidence: number; // 0-10
  positionSize: number; // percentage
  entryPrice: number;
  stopLoss: number;
  takeProfit: number;
  analystSummary: AnalystReport[];
  riskAssessment: RiskMetrics;
  reasoning: string;
}
```

**Features**:
- Color-coded action (green/red/yellow)
- Expandable details
- Quick trade button
- Export to PDF

---

#### 4. **DebateViewer** (`components/dashboard/DebateViewer.tsx`)
```typescript
interface DebateViewerProps {
  debate: ResearchDebate;
}

type ResearchDebate = {
  rounds: Array<{
    roundNumber: number;
    bullArgument: string;
    bearArgument: string;
    judgeDecision: string;
  }>;
  finalVerdict: string;
}
```

**Features**:
- Round-by-round navigation
- Bull/Bear argument cards
- Judge decision highlighting
- Copy to clipboard

---

#### 5. **PortfolioOverview** (`components/dashboard/PortfolioOverview.tsx`)
```typescript
interface PortfolioOverviewProps {
  userId: string;
}

type Portfolio = {
  totalValue: number;
  totalReturn: number;
  positions: Position[];
  pendingRecommendations: Recommendation[];
}

type Position = {
  symbol: string;
  quantity: number;
  currentValue: number;
  returnPercent: number;
  aiStatus: 'hold' | 'review' | 'alert';
}
```

**Features**:
- Live position tracking
- AI recommendation badges
- One-click re-analysis
- Performance charts

---

## 🔌 API Integration Specifications

### **REST API Endpoints**

#### 1. **Analysis Endpoints**

```typescript
// Launch new analysis
POST /api/analyze
Request: {
  symbol: string;
  assetType: 'equity' | 'crypto';
  date: string; // ISO format
  analysts: string[]; // ['technical', 'sentiment', ...]
  config: {
    researchDepth: number;
    llmModel: string;
  }
}
Response: {
  analysisId: string;
  status: 'queued' | 'running';
  estimatedTime: number; // seconds
}

// Get analysis status
GET /api/analyze/{analysisId}/status
Response: {
  status: 'queued' | 'running' | 'completed' | 'error';
  progress: {
    currentAgent: string;
    completedAgents: string[];
    overallPercent: number;
  };
  error?: string;
}

// Get analysis results
GET /api/analyze/{analysisId}/results
Response: {
  decision: TradingDecision;
  reports: {
    technical?: string;
    sentiment?: string;
    news?: string;
    fundamentals?: string;
  };
  debate: ResearchDebate;
  riskAssessment: RiskMetrics;
  metadata: {
    symbol: string;
    date: string;
    completedAt: string;
    duration: number;
  }
}
```

#### 2. **Portfolio Endpoints**

```typescript
// Get user portfolio
GET /api/portfolio
Response: {
  positions: Position[];
  totalValue: number;
  totalReturn: number;
  performance: {
    daily: number;
    weekly: number;
    monthly: number;
  }
}

// Get pending recommendations
GET /api/portfolio/recommendations
Response: {
  recommendations: Array<{
    analysisId: string;
    symbol: string;
    action: 'BUY' | 'SELL' | 'HOLD';
    confidence: number;
    createdAt: string;
    expiresAt: string;
  }>
}
```

#### 3. **History Endpoints**

```typescript
// Get analysis history
GET /api/history?symbol={symbol}&days={days}&limit={limit}
Response: {
  analyses: Array<{
    id: string;
    symbol: string;
    action: 'BUY' | 'SELL' | 'HOLD';
    confidence: number;
    date: string;
    actualReturn?: number; // if enough time passed
  }>;
  metrics: {
    winRate: number;
    avgReturn: number;
    sharpeRatio: number;
  }
}
```

---

### **WebSocket Events**

```typescript
// Client subscribes to analysis
socket.emit('subscribe_analysis', { analysisId: string });

// Server sends progress updates
socket.on('analysis_progress', (data: {
  analysisId: string;
  agent: string;
  status: 'started' | 'completed' | 'error';
  progress: number;
  message?: string;
}));

// Server sends completion
socket.on('analysis_complete', (data: {
  analysisId: string;
  decision: TradingDecision;
}));

// Client unsubscribes
socket.emit('unsubscribe_analysis', { analysisId: string });
```

---

## 🗓️ Development Roadmap

### **Phase 1: Foundation (Weeks 1-2)**
**Goal**: Setup + Core UI

**Tasks**:
- ✅ Initialize Next.js 14 project with TypeScript
- ✅ Setup Tailwind CSS + shadcn/ui
- ✅ Configure ESLint, Prettier, Vitest
- ✅ Create project structure
- ✅ Build basic layout (Header, Sidebar)
- ✅ Setup API client utilities
- ✅ Create authentication flow (if needed)

**Deliverables**:
- Working Next.js app with routing
- Basic UI components library
- API integration foundation

---

### **Phase 2: Analysis Features (Weeks 3-4)**
**Goal**: Launch & Track Analyses

**Tasks**:
- ✅ Build AnalysisLauncher component
- ✅ Implement ProgressTracker with WebSocket
- ✅ Create DecisionCard component
- ✅ Build report viewer (Technical, Sentiment, etc.)
- ✅ Implement DebateViewer
- ✅ Add error handling & retries

**Deliverables**:
- Fully functional analysis workflow
- Real-time progress tracking
- Decision visualization

---

### **Phase 3: Portfolio & History (Weeks 5-6)**
**Goal**: Portfolio Management

**Tasks**:
- ✅ Build PortfolioOverview component
- ✅ Create position tracking UI
- ✅ Implement historical analysis library
- ✅ Build performance analytics charts
- ✅ Add agent accuracy metrics
- ✅ Create export functionality (PDF, CSV)

**Deliverables**:
- Portfolio dashboard
- Historical analysis browser
- Performance tracking

---

### **Phase 4: Polish & Testing (Weeks 7-8)**
**Goal**: Production Readiness

**Tasks**:
- ✅ Responsive design (tablet/mobile)
- ✅ Performance optimization (code splitting)
- ✅ Unit tests (80%+ coverage)
- ✅ Integration tests (API mocking)
- ✅ E2E tests (Playwright)
- ✅ Accessibility audit (WCAG 2.1 AA)
- ✅ Documentation (user guide)

**Deliverables**:
- Production-ready application
- Comprehensive test suite
- User documentation

---

### **Phase 5: Advanced Features (Weeks 9-10)**
**Goal**: Power User Features

**Tasks**:
- ✅ Batch analysis (multiple symbols)
- ✅ Custom alerts & notifications
- ✅ Saved analysis presets
- ✅ Dark mode support
- ✅ Advanced charting (TradingView integration)
- ✅ Comparison view (multiple analyses)

**Deliverables**:
- Advanced analysis tools
- Enhanced UX features

---

## 📊 Success Metrics

### **Performance Targets**
- 📈 First Contentful Paint (FCP): < 1.5s
- 📈 Largest Contentful Paint (LCP): < 2.5s
- 📈 Time to Interactive (TTI): < 3.5s
- 📈 Cumulative Layout Shift (CLS): < 0.1
- 📈 WebSocket latency: < 100ms

### **User Experience**
- ✅ Analysis launch: < 10 seconds to start
- ✅ Decision display: < 2 seconds after completion
- ✅ Portfolio load: < 1 second
- ✅ Chart rendering: < 500ms

### **Quality Metrics**
- ✅ Test coverage: > 80%
- ✅ TypeScript coverage: 100%
- ✅ Accessibility score: > 90 (Lighthouse)
- ✅ Bundle size: < 500KB (initial load)

---

## 🚀 Deployment Strategy

### **Environments**

```
Development  →  Staging  →  Production
```

**Development** (`dev.tradingagents.local`):
- Local development
- Hot module replacement
- Mock API responses

**Staging** (`staging.tradingagents.com`):
- Production-like environment
- Real backend integration
- User acceptance testing

**Production** (`app.tradingagents.com`):
- Live application
- CDN delivery (Cloudflare)
- Auto-scaling (Vercel/AWS)

---

### **CI/CD Pipeline**

```yaml
# .github/workflows/deploy.yml
name: Deploy Frontend

on:
  push:
    branches: [main, develop]

jobs:
  test:
    - Run linting (ESLint)
    - Run type checking (tsc)
    - Run unit tests (Vitest)
    - Run E2E tests (Playwright)

  build:
    - Build Next.js app
    - Optimize images
    - Generate static pages

  deploy:
    - Deploy to Vercel (preview for PRs)
    - Deploy to production (main branch)
    - Notify team (Slack)
```

---

## 🔒 Security Considerations

### **Authentication & Authorization**
- JWT-based authentication
- Secure HTTP-only cookies
- Role-based access control (RBAC)
- Session management

### **Data Protection**
- HTTPS only (enforce SSL)
- API key encryption
- Input sanitization
- XSS protection (Content Security Policy)
- CSRF tokens

### **Rate Limiting**
- API request throttling
- WebSocket connection limits
- Prevent analysis spam

---

## 📝 Documentation Deliverables

### **For Developers**
1. ✅ `README.md` - Setup instructions
2. ✅ `CONTRIBUTING.md` - Contribution guidelines
3. ✅ `API_REFERENCE.md` - API documentation
4. ✅ `ARCHITECTURE.md` - Technical architecture
5. ✅ `COMPONENT_LIBRARY.md` - Component usage guide

### **For Users**
1. ✅ `USER_GUIDE.md` - How to use dashboard
2. ✅ `FAQ.md` - Common questions
3. ✅ Video tutorials (Loom/YouTube)

### **For Project Managers**
1. ✅ `PROJECT_PLAN.md` (this document)
2. ✅ `SPRINT_REPORTS.md` - Weekly progress
3. ✅ `TESTING_STRATEGY.md` - QA plan

---

## 💰 Budget & Resources

### **Team Requirements**
- **Frontend Lead** (1): React/Next.js expert
- **UI/UX Designer** (1): Dashboard design
- **Backend Developer** (0.5): API integration support
- **QA Engineer** (0.5): Testing & automation

**Total**: 3 FTE for 10 weeks

### **Tools & Services**
- Vercel Pro: $20/month
- Sentry (error tracking): $26/month
- Figma (design): $15/user/month
- GitHub Actions: Free (2000 min/month)

**Total**: ~$80/month

---

## ⚠️ Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|-----------|
| Backend API delays | High | Medium | Mock API during development |
| WebSocket scaling issues | High | Low | Use Redis pub/sub for scaling |
| Real-time performance | Medium | Medium | Implement caching, optimize re-renders |
| Browser compatibility | Low | Low | Target modern browsers only (Chrome 90+) |
| Complex state management | Medium | Medium | Use Zustand + TanStack Query properly |

---

## 📞 Communication Plan

### **Daily Standups** (15 min)
- What did you complete yesterday?
- What will you work on today?
- Any blockers?

### **Weekly Demos** (Friday, 30 min)
- Show working features
- Gather feedback
- Adjust priorities

### **Bi-weekly Retrospectives**
- What went well?
- What can improve?
- Action items

### **Communication Channels**
- Slack: `#tradingagents-frontend`
- GitHub: Issues & PRs
- Notion: Project documentation

---

## ✅ Acceptance Criteria

### **Minimum Viable Product (MVP)**
- [ ] Users can launch equity/crypto analyses
- [ ] Real-time progress tracking works
- [ ] Trading decisions display correctly
- [ ] Portfolio overview shows positions
- [ ] Historical analyses are searchable
- [ ] Responsive design (desktop + tablet)
- [ ] 80%+ test coverage
- [ ] < 3s page load time

### **Production Ready**
- [ ] All MVP criteria met
- [ ] User documentation complete
- [ ] Security audit passed
- [ ] Performance benchmarks met
- [ ] Accessibility compliant (WCAG AA)
- [ ] Error monitoring setup (Sentry)
- [ ] Analytics tracking (PostHog/Mixpanel)

---

## 🎯 Next Steps

1. **Review & Approve** this plan with stakeholders
2. **Setup project** (GitHub repo, Vercel, etc.)
3. **Design mockups** (Figma wireframes)
4. **Sprint 1 kickoff** (Week 1 tasks)
5. **Backend API coordination** (align endpoints)

---

**Project Manager Sign-off**: _______________
**Tech Lead Sign-off**: _______________
**Date**: October 10, 2025
