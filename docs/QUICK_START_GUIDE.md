# TradingAgents Dashboard - Quick Start Guide

**For**: Developers building the React frontend
**Time to complete**: 30 minutes
**Last Updated**: October 10, 2025

---

## 🎯 What You'll Build

A modern React dashboard that lets users:
1. Launch AI trading analyses
2. Track real-time agent progress
3. View trading recommendations
4. Manage portfolio positions

---

## 📋 Prerequisites

### Required
- **Node.js**: 18.17.0 or higher
- **npm** or **yarn** or **pnpm**
- **Git**
- **Code editor**: VS Code (recommended)

### Recommended VS Code Extensions
- ES7+ React/Redux/React-Native snippets
- Tailwind CSS IntelliSense
- Prettier - Code formatter
- ESLint

---

## 🚀 Step 1: Initialize Project (5 min)

### Create Next.js App

```bash
# Navigate to TradingAgents directory
cd /Users/nguyenminhduc/Desktop/TradingAgents

# Create frontend directory
npx create-next-app@latest frontend \
  --typescript \
  --tailwind \
  --app \
  --src-dir \
  --import-alias "@/*"

# Navigate to frontend
cd frontend
```

**Options selected**:
- ✅ TypeScript
- ✅ Tailwind CSS
- ✅ App Router
- ✅ Src directory
- ✅ Import alias (@/*)
- ❌ Turbopack (not yet)

---

## 🎨 Step 2: Install UI Components (5 min)

### Install shadcn/ui

```bash
# Initialize shadcn/ui
npx shadcn-ui@latest init

# Select options:
# Style: Default
# Base color: Slate
# CSS variables: Yes
```

### Install Core Components

```bash
# Install essential components
npx shadcn-ui@latest add button
npx shadcn-ui@latest add input
npx shadcn-ui@latest add select
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add tabs
npx shadcn-ui@latest add card
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add progress
npx shadcn-ui@latest add checkbox
npx shadcn-ui@latest add toast
```

---

## 📦 Step 3: Install Dependencies (5 min)

### State Management & Data Fetching

```bash
npm install zustand @tanstack/react-query
```

### WebSocket & Real-time

```bash
npm install socket.io-client
```

### Charts & Visualization

```bash
npm install lightweight-charts recharts
npm install @tanstack/react-table
```

### Forms & Validation

```bash
npm install react-hook-form zod @hookform/resolvers/zod
```

### Utilities

```bash
npm install axios date-fns clsx tailwind-merge class-variance-authority
```

### Dev Dependencies

```bash
npm install -D @types/node @types/react @types/react-dom
npm install -D vitest @testing-library/react @testing-library/jest-dom
npm install -D @playwright/test
npm install -D prettier prettier-plugin-tailwindcss
```

---

## 🗂️ Step 4: Setup Project Structure (5 min)

### Create Folder Structure

```bash
cd src

# Create directories
mkdir -p app/\(dashboard\)/{analysis,portfolio,history}
mkdir -p components/{ui,dashboard,charts,shared}
mkdir -p lib/{api,hooks,utils,constants}
mkdir -p stores
mkdir -p types
mkdir -p styles

# Go back to root
cd ..
```

### Create Essential Files

```bash
# Create type definitions
touch src/types/analysis.ts
touch src/types/portfolio.ts
touch src/types/api.ts

# Create API clients
touch src/lib/api/client.ts
touch src/lib/api/trading-agents.ts
touch src/lib/api/portfolio.ts

# Create WebSocket client
touch src/lib/websocket.ts

# Create hooks
touch src/lib/hooks/useAnalysis.ts
touch src/lib/hooks/useWebSocket.ts
touch src/lib/hooks/usePortfolio.ts

# Create stores
touch src/stores/analysis-store.ts
touch src/stores/portfolio-store.ts
touch src/stores/ui-store.ts
```

---

## ⚙️ Step 5: Configure Environment (3 min)

### Create Environment Files

```bash
# Create .env.local
cat > .env.local << 'EOF'
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000

# Optional: Enable debug mode
NEXT_PUBLIC_DEBUG=true
EOF

# Create .env.example
cat > .env.example << 'EOF'
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000

# Optional: Enable debug mode
NEXT_PUBLIC_DEBUG=false
EOF
```

---

## 🎨 Step 6: Setup Tailwind Config (2 min)

### Update tailwind.config.js

```bash
cat > tailwind.config.js << 'EOF'
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
        buy: 'hsl(142 76% 36%)',      // Green
        sell: 'hsl(0 84% 60%)',        // Red
        hold: 'hsl(43 100% 50%)',      // Yellow
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
};
EOF
```

---

## 🔧 Step 7: Create First Components (5 min)

### 1. Layout Component

**Create**: `src/app/(dashboard)/layout.tsx`

```typescript
import { Inter } from 'next/font/google';
import '@/styles/globals.css';

const inter = Inter({ subsets: ['latin'] });

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-background">
          <header className="border-b">
            <div className="container mx-auto px-4 py-4">
              <h1 className="text-2xl font-bold">TradingAgents Dashboard</h1>
            </div>
          </header>
          <main className="container mx-auto px-4 py-6">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
```

### 2. Home Page

**Create**: `src/app/(dashboard)/page.tsx`

```typescript
export default function DashboardHome() {
  return (
    <div>
      <h2 className="text-3xl font-bold mb-6">Welcome to TradingAgents</h2>
      <p className="text-muted-foreground">
        Launch AI-powered trading analyses and manage your portfolio.
      </p>
    </div>
  );
}
```

### 3. API Client

**Create**: `src/lib/api/client.ts`

```typescript
import axios, { AxiosInstance } from 'axios';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  async get<T>(url: string): Promise<T> {
    const response = await this.client.get(url);
    return response.data;
  }

  async post<T>(url: string, data?: unknown): Promise<T> {
    const response = await this.client.post(url, data);
    return response.data;
  }
}

export const apiClient = new ApiClient();
```

---

## ✅ Step 8: Verify Setup

### Run Development Server

```bash
npm run dev
```

Open browser: http://localhost:3000

**You should see**: "Welcome to TradingAgents" page

---

## 📊 Step 9: Create Your First Feature (Bonus)

### Build AnalysisLauncher Component

**Create**: `src/components/dashboard/AnalysisLauncher.tsx`

```typescript
'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export function AnalysisLauncher() {
  const [symbol, setSymbol] = useState('');

  const handleLaunch = async () => {
    console.log('Launching analysis for:', symbol);
    // TODO: API call
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>New Analysis</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <Input
            placeholder="Enter symbol (e.g., NVDA)"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
          />
          <Button onClick={handleLaunch} className="w-full">
            🚀 Run Analysis
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
```

### Use in Home Page

**Update**: `src/app/(dashboard)/page.tsx`

```typescript
import { AnalysisLauncher } from '@/components/dashboard/AnalysisLauncher';

export default function DashboardHome() {
  return (
    <div className="max-w-2xl">
      <h2 className="text-3xl font-bold mb-6">Welcome to TradingAgents</h2>
      <AnalysisLauncher />
    </div>
  );
}
```

**Refresh browser** - You should see the analysis launcher!

---

## 🎯 Next Steps

Now that your foundation is ready, continue with:

1. **Sprint 1-2**: Complete remaining UI components
2. **Sprint 3-4**: Implement analysis features
3. **Sprint 5-6**: Add portfolio management
4. **Sprint 7-8**: Testing & polish

Refer to:
- `FRONTEND_PROJECT_PLAN.md` - Overall project plan
- `TECHNICAL_SPEC.md` - Detailed technical specs
- `DEVELOPMENT_ROADMAP.md` - Sprint-by-sprint tasks
- `API_BACKEND_SPEC.md` - Backend API reference

---

## 🆘 Troubleshooting

### Issue: Module not found errors

**Solution**:
```bash
npm install
# or
rm -rf node_modules package-lock.json
npm install
```

### Issue: TypeScript errors

**Solution**: Check `tsconfig.json` has correct paths:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### Issue: Tailwind styles not loading

**Solution**: Ensure `globals.css` imports Tailwind:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Issue: API connection failed

**Solution**: Check backend is running:
```bash
# In TradingAgents directory
python -m uvicorn main:app --reload
```

---

## 📚 Resources

### Documentation
- [Next.js Docs](https://nextjs.org/docs)
- [shadcn/ui](https://ui.shadcn.com/)
- [TanStack Query](https://tanstack.com/query/latest)
- [Zustand](https://docs.pmnd.rs/zustand/getting-started/introduction)

### Community
- GitHub: [TradingAgents Issues](https://github.com/your-repo/issues)
- Slack: `#tradingagents-frontend`

---

## ✅ Checklist

Before moving to Sprint 1:

- [ ] Next.js app running on localhost:3000
- [ ] shadcn/ui components installed
- [ ] Tailwind CSS configured
- [ ] Project structure created
- [ ] Environment variables set
- [ ] API client created
- [ ] First component working

**Congratulations!** 🎉 You're ready to build the TradingAgents Dashboard!

---

**Questions?** Refer to `TECHNICAL_SPEC.md` or ask in Slack `#tradingagents-frontend`
