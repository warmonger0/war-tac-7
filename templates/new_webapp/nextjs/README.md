# My App - Next.js Template

This project was created from the **tac-webbuilder Next.js template** and is pre-configured for ADW-powered development.

## Tech Stack

- **Next.js 14** - React framework with App Router
- **React 18** - Modern React with Server Components
- **TypeScript** - Type safety and better DX
- **Jest** - Unit testing framework
- **React Testing Library** - Component testing utilities
- **ESLint** - Code linting with Next.js config

## Getting Started

### Prerequisites

- Node.js 18+ or Bun
- npm, yarn, or bun package manager

### Installation

```bash
npm install
# or
bun install
```

### Development

Start the development server:

```bash
npm run dev
# or
bun run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Building

Build for production:

```bash
npm run build
# or
bun run build
```

Start production server:

```bash
npm run start
# or
bun run start
```

### Testing

Run tests:

```bash
npm run test
# or
bun run test
```

Run tests in watch mode:

```bash
npm run test:watch
# or
bun run test:watch
```

### Type Checking

```bash
npm run type-check
# or
bun run type-check
```

### Linting

```bash
npm run lint
# or
bun run lint
```

## Project Structure

```
app/
├── api/           # API routes
│   └── hello/     # Example API endpoint
├── layout.tsx     # Root layout
├── page.tsx       # Home page
└── globals.css    # Global styles

components/        # React components
lib/              # Utility functions and shared code
```

## App Router

This template uses Next.js App Router with:

- **Server Components** - Default for all components
- **Client Components** - Use `'use client'` directive when needed
- **API Routes** - In `app/api/` directory
- **Layouts** - Nested layouts for consistent UI
- **Loading & Error States** - Automatic with `loading.tsx` and `error.tsx`

## ADW Integration

This project is pre-configured for ADW (Autonomous Development Workflow):

- `.claude/` directory contains Claude Code configuration
- Use natural language to request features
- Tests are automatically generated for new features
- Code follows project-specific rules defined in `.claude/settings.json`

## Environment Variables

Copy `.env.sample` to `.env.local` and configure:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENABLE_DEBUG=false
API_SECRET_KEY=your-secret-key-here
```

Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser. Others are server-side only.

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [TypeScript Documentation](https://www.typescriptlang.org)
- [App Router Guide](https://nextjs.org/docs/app)
