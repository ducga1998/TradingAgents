# TradingAgents Dashboard - Technical Specification

**Version**: 1.0
**Last Updated**: October 10, 2025
**Status**: Draft

---

## 🎯 Overview

This document provides detailed technical specifications for the TradingAgents Dashboard frontend application built with React.js, Next.js 14, and TypeScript.

---

## 🏗️ Technology Stack

### **Core Framework**
```json
{
  "framework": "Next.js 14.2.0",
  "react": "18.3.0",
  "typescript": "5.5.0",
  "node": ">=18.17.0"
}
```

### **UI & Styling**
```json
{
  "tailwindcss": "3.4.0",
  "shadcn-ui": "latest",
  "@radix-ui/react-*": "latest",
  "framer-motion": "11.0.0",
  "lucide-react": "0.395.0"
}
```

### **State Management**
```json
{
  "zustand": "4.5.0",
  "@tanstack/react-query": "5.51.0",
  "socket.io-client": "4.7.0"
}
```

### **Data Visualization**
```json
{
  "lightweight-charts": "4.1.0",
  "recharts": "2.12.0",
  "@tanstack/react-table": "8.17.0"
}
```

### **Development Tools**
```json
{
  "vite": "5.3.0",
  "vitest": "1.6.0",
  "@testing-library/react": "16.0.0",
  "@playwright/test": "1.45.0",
  "eslint": "8.57.0",
  "prettier": "3.3.0"
}
```

---

## 📦 Package.json

```json
{
  "name": "tradingagents-dashboard",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:e2e": "playwright test",
    "type-check": "tsc --noEmit",
    "format": "prettier --write \"**/*.{ts,tsx,md,json}\""
  },
  "dependencies": {
    "next": "14.2.5",
    "react": "18.3.1",
    "react-dom": "18.3.1",
    "@tanstack/react-query": "^5.51.11",
    "@tanstack/react-table": "^8.17.3",
    "zustand": "^4.5.4",
    "socket.io-client": "^4.7.2",
    "lightweight-charts": "^4.1.3",
    "recharts": "^2.12.7",
    "tailwindcss": "^3.4.6",
    "@radix-ui/react-dialog": "^1.1.1",
    "@radix-ui/react-dropdown-menu": "^2.1.1",
    "@radix-ui/react-select": "^2.1.1",
    "@radix-ui/react-tabs": "^1.1.0",
    "framer-motion": "^11.3.6",
    "lucide-react": "^0.408.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.1",
    "tailwind-merge": "^2.4.0",
    "date-fns": "^3.6.0",
    "zod": "^3.23.8",
    "react-hook-form": "^7.52.1"
  },
  "devDependencies": {
    "@types/node": "^20.14.11",
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.0",
    "typescript": "^5.5.3",
    "@vitejs/plugin-react": "^4.3.1",
    "vitest": "^1.6.0",
    "@testing-library/react": "^16.0.0",
    "@testing-library/jest-dom": "^6.4.6",
    "@playwright/test": "^1.45.2",
    "eslint": "^8.57.0",
    "eslint-config-next": "14.2.5",
    "prettier": "^3.3.3",
    "prettier-plugin-tailwindcss": "^0.6.5",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.39"
  }
}
```

---

## 🎨 Design System

### **Color Palette**

```css
/* Tailwind CSS Custom Colors */
:root {
  /* Brand Colors */
  --brand-primary: 59 130 246;      /* Blue */
  --brand-secondary: 16 185 129;     /* Green */
  --brand-accent: 249 115 22;        /* Orange */

  /* Semantic Colors */
  --success: 34 197 94;              /* Green */
  --warning: 234 179 8;              /* Yellow */
  --error: 239 68 68;                /* Red */
  --info: 59 130 246;                /* Blue */

  /* Trading Colors */
  --buy: 34 197 94;                  /* Green */
  --sell: 239 68 68;                 /* Red */
  --hold: 234 179 8;                 /* Yellow */

  /* Neutral Colors */
  --background: 255 255 255;
  --foreground: 15 23 42;
  --muted: 241 245 249;
  --border: 226 232 240;
}

.dark {
  --background: 15 23 42;
  --foreground: 248 250 252;
  --muted: 30 41 59;
  --border: 51 65 85;
}
```

### **Typography**

```typescript
// Font Configuration
export const fontConfig = {
  sans: ['Inter', 'system-ui', 'sans-serif'],
  mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
  sizes: {
    xs: '0.75rem',    // 12px
    sm: '0.875rem',   // 14px
    base: '1rem',     // 16px
    lg: '1.125rem',   // 18px
    xl: '1.25rem',    // 20px
    '2xl': '1.5rem',  // 24px
    '3xl': '1.875rem',// 30px
    '4xl': '2.25rem', // 36px
  }
};
```

### **Spacing System**

```typescript
// Tailwind spacing scale (matches 4px base)
export const spacing = {
  0: '0px',
  1: '0.25rem',  // 4px
  2: '0.5rem',   // 8px
  3: '0.75rem',  // 12px
  4: '1rem',     // 16px
  6: '1.5rem',   // 24px
  8: '2rem',     // 32px
  12: '3rem',    // 48px
  16: '4rem',    // 64px
};
```

---

## 🗂️ Type Definitions

### **Core Types**

```typescript
// types/analysis.ts

export type AssetType = 'equity' | 'crypto';

export type TradingAction = 'BUY' | 'SELL' | 'HOLD';

export type AnalystType =
  | 'technical'
  | 'sentiment'
  | 'news'
  | 'fundamentals'
  | 'crypto_technical'
  | 'crypto_onchain'
  | 'crypto_sentiment'
  | 'crypto_fundamentals';

export type AnalysisStatus = 'queued' | 'running' | 'completed' | 'error';

export type AgentStatus = 'pending' | 'running' | 'completed' | 'error';

export interface AnalysisConfig {
  symbol: string;
  assetType: AssetType;
  date: Date;
  analysts: AnalystType[];
  researchDepth: 1 | 2 | 3 | 4 | 5;
  llmModel: string;
}

export interface TradingDecision {
  symbol: string;
  action: TradingAction;
  confidence: number; // 0-10
  positionSize: number; // percentage
  entryPrice: number;
  stopLoss: number;
  takeProfit: number;
  reasoning: string;
  createdAt: string;
}

export interface AnalystReport {
  analyst: AnalystType;
  summary: string;
  score: number; // 0-10
  keyPoints: string[];
  sentiment: 'bullish' | 'bearish' | 'neutral';
  confidence: number;
}

export interface RiskMetrics {
  volatility: 'low' | 'moderate' | 'high';
  beta?: number;
  maxDrawdown: number;
  liquidity: 'low' | 'moderate' | 'high' | 'excellent';
  concerns: string[];
}

export interface ResearchDebate {
  rounds: DebateRound[];
  finalVerdict: string;
}

export interface DebateRound {
  roundNumber: number;
  bullArgument: string;
  bearArgument: string;
  judgeDecision: string;
}

export interface AnalysisProgress {
  agents: AgentProgress[];
  overall: number; // 0-100
  estimatedTime?: number; // seconds
}

export interface AgentProgress {
  name: string;
  status: AgentStatus;
  duration?: number;
  error?: string;
}

export interface AnalysisResults {
  id: string;
  decision: TradingDecision;
  reports: Record<AnalystType, string>;
  debate: ResearchDebate;
  riskAssessment: RiskMetrics;
  metadata: {
    symbol: string;
    date: string;
    completedAt: string;
    duration: number;
  };
}
```

### **Portfolio Types**

```typescript
// types/portfolio.ts

export type PositionStatus = 'hold' | 'review' | 'alert';

export interface Position {
  id: string;
  symbol: string;
  assetType: AssetType;
  quantity: number;
  avgEntryPrice: number;
  currentPrice: number;
  currentValue: number;
  returnPercent: number;
  returnAbsolute: number;
  aiStatus: PositionStatus;
  lastAnalyzedAt?: string;
}

export interface Portfolio {
  userId: string;
  totalValue: number;
  totalReturn: number;
  totalReturnPercent: number;
  positions: Position[];
  performance: {
    daily: number;
    weekly: number;
    monthly: number;
    yearly: number;
  };
  updatedAt: string;
}

export interface Recommendation {
  id: string;
  analysisId: string;
  symbol: string;
  action: TradingAction;
  confidence: number;
  positionSize: number;
  createdAt: string;
  expiresAt: string;
  status: 'pending' | 'executed' | 'rejected' | 'expired';
}
```

### **API Response Types**

```typescript
// types/api.ts

export interface ApiResponse<T> {
  data: T;
  success: boolean;
  error?: string;
  timestamp: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  hasNext: boolean;
}

export interface AnalysisApiResponse {
  analysisId: string;
  status: AnalysisStatus;
  estimatedTime: number;
}

export interface WebSocketEvent<T = unknown> {
  event: string;
  data: T;
  timestamp: string;
}
```

---

## 🔌 API Client Implementation

### **Base API Client**

```typescript
// lib/api/client.ts

import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';

class ApiClient {
  private client: AxiosInstance;

  constructor(baseURL: string) {
    this.client = axios.create({
      baseURL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor (add auth token)
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('auth_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor (error handling)
    this.client.interceptors.response.use(
      (response) => response.data,
      (error) => {
        if (error.response?.status === 401) {
          // Handle unauthorized
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return this.client.get(url, config);
  }

  async post<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> {
    return this.client.post(url, data, config);
  }

  async put<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> {
    return this.client.put(url, data, config);
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return this.client.delete(url, config);
  }
}

export const apiClient = new ApiClient(
  process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
);
```

### **Trading Agents API**

```typescript
// lib/api/trading-agents.ts

import { apiClient } from './client';
import type {
  AnalysisConfig,
  AnalysisApiResponse,
  AnalysisResults,
  AnalysisProgress,
} from '@/types';

export const tradingAgentsApi = {
  // Launch new analysis
  launchAnalysis: async (config: AnalysisConfig): Promise<AnalysisApiResponse> => {
    return apiClient.post('/api/analyze', config);
  },

  // Get analysis status
  getAnalysisStatus: async (analysisId: string): Promise<AnalysisProgress> => {
    return apiClient.get(`/api/analyze/${analysisId}/status`);
  },

  // Get analysis results
  getAnalysisResults: async (analysisId: string): Promise<AnalysisResults> => {
    return apiClient.get(`/api/analyze/${analysisId}/results`);
  },

  // Get historical analyses
  getHistory: async (params: {
    symbol?: string;
    days?: number;
    limit?: number;
  }): Promise<AnalysisResults[]> => {
    const queryString = new URLSearchParams(params as any).toString();
    return apiClient.get(`/api/history?${queryString}`);
  },
};
```

### **Portfolio API**

```typescript
// lib/api/portfolio.ts

import { apiClient } from './client';
import type { Portfolio, Recommendation } from '@/types';

export const portfolioApi = {
  // Get user portfolio
  getPortfolio: async (): Promise<Portfolio> => {
    return apiClient.get('/api/portfolio');
  },

  // Get recommendations
  getRecommendations: async (): Promise<Recommendation[]> => {
    return apiClient.get('/api/portfolio/recommendations');
  },

  // Execute recommendation
  executeRecommendation: async (recommendationId: string): Promise<void> => {
    return apiClient.post(`/api/portfolio/recommendations/${recommendationId}/execute`);
  },

  // Reject recommendation
  rejectRecommendation: async (recommendationId: string): Promise<void> => {
    return apiClient.post(`/api/portfolio/recommendations/${recommendationId}/reject`);
  },
};
```

---

## 🔄 WebSocket Implementation

```typescript
// lib/websocket.ts

import { io, Socket } from 'socket.io-client';
import type { WebSocketEvent } from '@/types';

class WebSocketClient {
  private socket: Socket | null = null;
  private listeners: Map<string, Set<Function>> = new Map();

  connect(url: string = process.env.NEXT_PUBLIC_WS_URL || 'http://localhost:8000') {
    this.socket = io(url, {
      transports: ['websocket'],
      auth: {
        token: localStorage.getItem('auth_token'),
      },
    });

    this.socket.on('connect', () => {
      console.log('WebSocket connected');
    });

    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected');
    });

    // Generic event handler
    this.socket.onAny((event: string, data: unknown) => {
      this.emit(event, data);
    });
  }

  disconnect() {
    this.socket?.disconnect();
    this.socket = null;
  }

  subscribeToAnalysis(analysisId: string) {
    this.socket?.emit('subscribe_analysis', { analysisId });
  }

  unsubscribeFromAnalysis(analysisId: string) {
    this.socket?.emit('unsubscribe_analysis', { analysisId });
  }

  on<T>(event: string, callback: (data: T) => void) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(callback);
  }

  off(event: string, callback: Function) {
    this.listeners.get(event)?.delete(callback);
  }

  private emit(event: string, data: unknown) {
    this.listeners.get(event)?.forEach((callback) => callback(data));
  }
}

export const wsClient = new WebSocketClient();
```

---

## 🪝 Custom Hooks

### **useAnalysis Hook**

```typescript
// lib/hooks/useAnalysis.ts

import { useMutation, useQuery } from '@tanstack/react-query';
import { tradingAgentsApi } from '@/lib/api/trading-agents';
import type { AnalysisConfig } from '@/types';

export function useAnalysis(analysisId?: string) {
  // Launch analysis mutation
  const launchAnalysis = useMutation({
    mutationFn: (config: AnalysisConfig) =>
      tradingAgentsApi.launchAnalysis(config),
    onSuccess: (data) => {
      console.log('Analysis launched:', data.analysisId);
    },
  });

  // Get analysis status query
  const status = useQuery({
    queryKey: ['analysis-status', analysisId],
    queryFn: () => tradingAgentsApi.getAnalysisStatus(analysisId!),
    enabled: !!analysisId,
    refetchInterval: (data) =>
      data?.overall === 100 ? false : 2000, // Poll every 2s
  });

  // Get analysis results query
  const results = useQuery({
    queryKey: ['analysis-results', analysisId],
    queryFn: () => tradingAgentsApi.getAnalysisResults(analysisId!),
    enabled: !!analysisId && status.data?.overall === 100,
  });

  return {
    launchAnalysis,
    status,
    results,
    isLaunching: launchAnalysis.isPending,
    isRunning: status.data?.overall !== 100,
    isComplete: status.data?.overall === 100,
  };
}
```

### **useWebSocket Hook**

```typescript
// lib/hooks/useWebSocket.ts

import { useEffect } from 'react';
import { wsClient } from '@/lib/websocket';

export function useWebSocket<T = unknown>(
  event: string,
  callback: (data: T) => void
) {
  useEffect(() => {
    // Connect on mount
    if (!wsClient['socket']) {
      wsClient.connect();
    }

    // Subscribe to event
    wsClient.on(event, callback);

    // Cleanup
    return () => {
      wsClient.off(event, callback);
    };
  }, [event, callback]);
}

export function useAnalysisProgress(analysisId: string | null) {
  const [progress, setProgress] = useState<AnalysisProgress | null>(null);

  useEffect(() => {
    if (!analysisId) return;

    wsClient.subscribeToAnalysis(analysisId);

    return () => {
      wsClient.unsubscribeFromAnalysis(analysisId);
    };
  }, [analysisId]);

  useWebSocket('analysis_progress', setProgress);
  useWebSocket('analysis_complete', (data) => {
    console.log('Analysis complete:', data);
  });

  return progress;
}
```

---

## 🎨 Component Examples

### **AnalysisLauncher Component**

```typescript
// components/dashboard/AnalysisLauncher.tsx

'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';
import { useAnalysis } from '@/lib/hooks/useAnalysis';
import type { AnalysisConfig } from '@/types';

const analysisSchema = z.object({
  symbol: z.string().min(1, 'Symbol is required'),
  assetType: z.enum(['equity', 'crypto']),
  date: z.date(),
  analysts: z.array(z.string()).min(1, 'Select at least one analyst'),
  researchDepth: z.number().min(1).max(5),
  llmModel: z.string(),
});

export function AnalysisLauncher() {
  const { launchAnalysis, isLaunching } = useAnalysis();
  const [selectedAnalysts, setSelectedAnalysts] = useState<string[]>([]);

  const form = useForm<AnalysisConfig>({
    resolver: zodResolver(analysisSchema),
    defaultValues: {
      symbol: '',
      assetType: 'equity',
      date: new Date(),
      analysts: [],
      researchDepth: 3,
      llmModel: 'gpt-4o-mini',
    },
  });

  const onSubmit = async (data: AnalysisConfig) => {
    const result = await launchAnalysis.mutateAsync(data);
    // Navigate to progress tracker
    window.location.href = `/analysis/${result.analysisId}`;
  };

  return (
    <div className="rounded-lg border bg-card p-6">
      <h2 className="text-2xl font-bold mb-4">New Analysis</h2>

      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        {/* Symbol Input */}
        <div>
          <label className="text-sm font-medium">Symbol</label>
          <Input
            {...form.register('symbol')}
            placeholder="NVDA, BTC, etc."
            className="mt-1"
          />
          {form.formState.errors.symbol && (
            <p className="text-sm text-red-500 mt-1">
              {form.formState.errors.symbol.message}
            </p>
          )}
        </div>

        {/* Asset Type */}
        <div>
          <label className="text-sm font-medium">Asset Type</label>
          <Select {...form.register('assetType')}>
            <option value="equity">Equities</option>
            <option value="crypto">Cryptocurrency</option>
          </Select>
        </div>

        {/* Analyst Selection */}
        <div>
          <label className="text-sm font-medium">Analyst Team</label>
          <div className="grid grid-cols-2 gap-3 mt-2">
            {['technical', 'sentiment', 'news', 'fundamentals'].map((analyst) => (
              <div key={analyst} className="flex items-center space-x-2">
                <Checkbox
                  id={analyst}
                  checked={selectedAnalysts.includes(analyst)}
                  onCheckedChange={(checked) => {
                    if (checked) {
                      setSelectedAnalysts([...selectedAnalysts, analyst]);
                      form.setValue('analysts', [...selectedAnalysts, analyst]);
                    } else {
                      const filtered = selectedAnalysts.filter(a => a !== analyst);
                      setSelectedAnalysts(filtered);
                      form.setValue('analysts', filtered);
                    }
                  }}
                />
                <label htmlFor={analyst} className="capitalize cursor-pointer">
                  {analyst}
                </label>
              </div>
            ))}
          </div>
        </div>

        {/* Research Depth */}
        <div>
          <label className="text-sm font-medium">Research Depth: {form.watch('researchDepth')}</label>
          <input
            type="range"
            min="1"
            max="5"
            {...form.register('researchDepth', { valueAsNumber: true })}
            className="w-full mt-2"
          />
        </div>

        {/* Submit */}
        <Button
          type="submit"
          disabled={isLaunching}
          className="w-full"
        >
          {isLaunching ? 'Launching...' : '🚀 Run Analysis'}
        </Button>
      </form>
    </div>
  );
}
```

### **ProgressTracker Component**

```typescript
// components/dashboard/ProgressTracker.tsx

'use client';

import { useAnalysisProgress } from '@/lib/hooks/useWebSocket';
import { Progress } from '@/components/ui/progress';
import { CheckCircle, Clock, Loader2, XCircle } from 'lucide-react';

interface ProgressTrackerProps {
  analysisId: string;
}

export function ProgressTracker({ analysisId }: ProgressTrackerProps) {
  const progress = useAnalysisProgress(analysisId);

  if (!progress) {
    return <div>Connecting...</div>;
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'running':
        return <Loader2 className="h-5 w-5 animate-spin text-blue-500" />;
      case 'error':
        return <XCircle className="h-5 w-5 text-red-500" />;
      default:
        return <Clock className="h-5 w-5 text-gray-400" />;
    }
  };

  return (
    <div className="rounded-lg border bg-card p-6">
      <h2 className="text-xl font-bold mb-4">
        Running Analysis
      </h2>

      {/* Overall Progress */}
      <div className="mb-6">
        <div className="flex justify-between text-sm mb-2">
          <span>Progress: {progress.overall}%</span>
          {progress.estimatedTime && (
            <span className="text-muted-foreground">
              {progress.estimatedTime}s remaining
            </span>
          )}
        </div>
        <Progress value={progress.overall} className="h-2" />
      </div>

      {/* Agent Status */}
      <div className="space-y-3">
        {progress.agents.map((agent) => (
          <div
            key={agent.name}
            className="flex items-center justify-between p-3 rounded-md bg-muted/50"
          >
            <div className="flex items-center space-x-3">
              {getStatusIcon(agent.status)}
              <span className="font-medium capitalize">{agent.name}</span>
            </div>

            {agent.duration && (
              <span className="text-sm text-muted-foreground">
                {agent.duration}s
              </span>
            )}

            {agent.error && (
              <span className="text-sm text-red-500">
                {agent.error}
              </span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## 🧪 Testing Strategy

### **Unit Tests (Vitest)**

```typescript
// components/dashboard/__tests__/AnalysisLauncher.test.tsx

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { AnalysisLauncher } from '../AnalysisLauncher';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

describe('AnalysisLauncher', () => {
  const queryClient = new QueryClient();

  it('renders form correctly', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <AnalysisLauncher />
      </QueryClientProvider>
    );

    expect(screen.getByText('New Analysis')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('NVDA, BTC, etc.')).toBeInTheDocument();
  });

  it('validates symbol input', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <AnalysisLauncher />
      </QueryClientProvider>
    );

    const submitButton = screen.getByRole('button', { name: /run analysis/i });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('Symbol is required')).toBeInTheDocument();
    });
  });

  it('submits form with valid data', async () => {
    // Test implementation
  });
});
```

### **Integration Tests**

```typescript
// tests/integration/analysis-flow.test.ts

import { test, expect } from '@playwright/test';

test.describe('Analysis Flow', () => {
  test('should launch analysis and display results', async ({ page }) => {
    // Navigate to dashboard
    await page.goto('/');

    // Fill in analysis form
    await page.fill('input[name="symbol"]', 'NVDA');
    await page.selectOption('select[name="assetType"]', 'equity');
    await page.check('input[id="technical"]');
    await page.check('input[id="sentiment"]');

    // Launch analysis
    await page.click('button:has-text("Run Analysis")');

    // Wait for progress tracker
    await expect(page.locator('text=Running Analysis')).toBeVisible();

    // Wait for completion
    await expect(page.locator('text=Analysis Complete')).toBeVisible({ timeout: 120000 });

    // Verify decision card
    await expect(page.locator('[data-testid="decision-card"]')).toBeVisible();
  });
});
```

---

## 📊 Performance Optimization

### **Code Splitting**

```typescript
// app/page.tsx

import dynamic from 'next/dynamic';

// Lazy load heavy components
const AnalysisLauncher = dynamic(() =>
  import('@/components/dashboard/AnalysisLauncher').then(mod => ({ default: mod.AnalysisLauncher })),
  { loading: () => <LoadingSkeleton /> }
);

const TradingChart = dynamic(() =>
  import('@/components/charts/TradingChart'),
  { ssr: false } // Disable SSR for chart
);
```

### **Image Optimization**

```typescript
import Image from 'next/image';

<Image
  src="/logo.png"
  alt="TradingAgents"
  width={200}
  height={50}
  priority // Above the fold
/>
```

### **API Response Caching**

```typescript
// lib/hooks/useAnalysis.ts

const results = useQuery({
  queryKey: ['analysis-results', analysisId],
  queryFn: () => tradingAgentsApi.getAnalysisResults(analysisId!),
  staleTime: 5 * 60 * 1000, // 5 minutes
  cacheTime: 30 * 60 * 1000, // 30 minutes
});
```

---

## 🔐 Security Best Practices

### **Environment Variables**

```bash
# .env.local

NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
NEXTAUTH_SECRET=your_secret_here
NEXTAUTH_URL=http://localhost:3000
```

### **Content Security Policy**

```typescript
// next.config.js

const cspHeader = `
  default-src 'self';
  script-src 'self' 'unsafe-eval' 'unsafe-inline';
  style-src 'self' 'unsafe-inline';
  img-src 'self' blob: data:;
  connect-src 'self' ${process.env.NEXT_PUBLIC_API_URL};
`;

module.exports = {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Content-Security-Policy',
            value: cspHeader.replace(/\n/g, ''),
          },
        ],
      },
    ];
  },
};
```

---

## 📝 Configuration Files

### **tsconfig.json**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "jsx": "preserve",
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "allowJs": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "incremental": true,
    "paths": {
      "@/*": ["./src/*"]
    },
    "plugins": [
      {
        "name": "next"
      }
    ]
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

### **tailwind.config.js**

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        border: 'hsl(var(--border))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        buy: 'hsl(var(--buy))',
        sell: 'hsl(var(--sell))',
        hold: 'hsl(var(--hold))',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
};
```

---

## 🚀 Deployment Configuration

### **Vercel Deployment**

```json
// vercel.json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "env": {
    "NEXT_PUBLIC_API_URL": "@api-url",
    "NEXT_PUBLIC_WS_URL": "@ws-url"
  },
  "build": {
    "env": {
      "NEXT_TELEMETRY_DISABLED": "1"
    }
  }
}
```

### **Docker Configuration**

```dockerfile
# Dockerfile

FROM node:18-alpine AS base

# Dependencies
FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Builder
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Runner
FROM base AS runner
WORKDIR /app
ENV NODE_ENV production
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000
CMD ["node", "server.js"]
```

---

**End of Technical Specification**

For questions or clarification, contact the frontend team lead.
