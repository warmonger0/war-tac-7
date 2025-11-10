# My App - React + Vite Template

This project was created from the **tac-webbuilder React-Vite template** and is pre-configured for ADW-powered development.

## Tech Stack

- **React 18** - Modern React with hooks
- **Vite** - Fast build tool and dev server
- **TypeScript** - Type safety and better DX
- **Vitest** - Unit testing framework
- **React Testing Library** - Component testing utilities
- **ESLint** - Code linting

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

Open [http://localhost:5173](http://localhost:5173) in your browser.

### Building

Build for production:

```bash
npm run build
# or
bun run build
```

Preview production build:

```bash
npm run preview
# or
bun run preview
```

### Testing

Run tests:

```bash
npm run test
# or
bun run test
```

Run tests with UI:

```bash
npm run test:ui
# or
bun run test:ui
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
src/
├── components/     # React components
├── api/           # API client and endpoints
├── main.tsx       # Application entry point
├── App.tsx        # Main App component
├── types.d.ts     # Global TypeScript definitions
└── setupTests.ts  # Test configuration
```

## ADW Integration

This project is pre-configured for ADW (Autonomous Development Workflow):

- `.claude/` directory contains Claude Code configuration
- Use natural language to request features
- Tests are automatically generated for new features
- Code follows project-specific rules defined in `.claude/settings.json`

## Environment Variables

Copy `.env.sample` to `.env` and configure:

```env
VITE_API_URL=http://localhost:8000
VITE_ENABLE_DEBUG=false
```

## Learn More

- [React Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)
- [Vitest Documentation](https://vitest.dev)
- [TypeScript Documentation](https://www.typescriptlang.org)
