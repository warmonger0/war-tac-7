# Frontend Application Relocation

**ADW ID:** 9fb089a7
**Date:** 2025-11-10
**Specification:** specs/issue-38-adw-9fb089a7-sdlc_planner-move-frontend-application.md

## Overview

Relocated the tac-webbuilder frontend application from `/app/webbuilder/client/` to `/projects/tac-webbuilder/app/client/` to align with the new project structure. This reorganization improves the codebase layout by consolidating the frontend alongside its related backend services and making the project structure more maintainable.

## What Was Built

- Complete frontend application migration to new directory structure
- Updated startup script with environment-aware port configuration
- Updated validation scripts to reflect new paths
- Updated MCP configuration for tree-specific paths
- Comprehensive React + TypeScript + Vite frontend application with:
  - Workflow dashboard with real-time updates
  - Request form for workflow submissions
  - History view for tracking workflow executions
  - Routes visualization for API endpoint monitoring
  - WebSocket integration for live status updates

## Technical Implementation

### Files Modified

- `scripts/start_webbuilder_ui.sh`: Updated to navigate to new path at `projects/tac-webbuilder/app/client/`, added `.ports.env` support for configurable frontend port
- `scripts/validate_implementation.py`: Updated all path references from `app/webbuilder/client/` to `app/client/` in validation checks
- `.mcp.json`: Updated tree-specific path reference for Playwright MCP configuration

### Files Created

The entire frontend application was moved to `projects/tac-webbuilder/app/client/` including:

- `index.html`: Main HTML entry point
- `package.json`: Frontend dependencies (React, Vite, TypeScript, TailwindCSS)
- `vite.config.ts`: Vite bundler configuration with port 5174
- `tsconfig.json` & `tsconfig.node.json`: TypeScript configurations
- `tailwind.config.js` & `postcss.config.js`: Styling configuration
- `src/App.tsx`: Main React application component with tab-based navigation
- `src/main.tsx`: Application entry point
- `src/style.css`: Global styles and Tailwind imports
- `src/types.ts`: TypeScript type definitions for workflows, routes, and history

### Frontend Components

- `src/components/WorkflowDashboard.tsx`: Main dashboard displaying available workflows
- `src/components/WorkflowCard.tsx`: Individual workflow card component
- `src/components/RequestForm.tsx`: Form for submitting workflow requests with dynamic input fields
- `src/components/HistoryView.tsx`: Displays workflow execution history with status and details
- `src/components/RoutesView.tsx`: Visualizes API routes and endpoints
- `src/components/ProgressBar.tsx`: Animated progress indicator for workflow execution
- `src/components/StatusBadge.tsx`: Status indicator with color-coded badges
- `src/components/TabBar.tsx`: Navigation tabs for switching between views
- `src/components/ConfirmDialog.tsx`: Confirmation dialog for workflow actions
- `src/components/IssuePreview.tsx`: Preview component for issue details

### API Integration

- `src/api/client.ts`: API client with methods for:
  - Fetching available workflows
  - Triggering workflow executions
  - Retrieving workflow history
  - Fetching API routes
- `src/hooks/useWebSocket.ts`: WebSocket hook for real-time workflow status updates

### Key Changes

- Frontend path changed from `/app/webbuilder/client/` to `/projects/tac-webbuilder/app/client/`
- Startup script enhanced with `.ports.env` integration for configurable port (defaults to 5174)
- Validation scripts updated to check correct directory structure
- MCP configuration updated for proper tree isolation
- All frontend files properly organized under new projects structure

## How to Use

### Starting the Frontend

1. Ensure you're in the project root directory
2. Run the startup script:
   ```bash
   ./scripts/start_webbuilder_ui.sh
   ```
3. The frontend will start on port 5174 (or the port specified in `.ports.env`)
4. Access the UI at `http://localhost:5174`

### Using the Frontend UI

1. **Dashboard Tab**: View available workflows and trigger new executions
2. **Request Tab**: Submit workflow requests with custom inputs
3. **History Tab**: View past workflow executions and their status
4. **Routes Tab**: Explore available API endpoints

### Development

1. Navigate to the frontend directory:
   ```bash
   cd projects/tac-webbuilder/app/client
   ```
2. Install dependencies (if needed):
   ```bash
   npm install
   ```
3. Start development server:
   ```bash
   npm run dev
   ```

## Configuration

### Port Configuration

The frontend port can be configured via `.ports.env` file:

```bash
FRONTEND_PORT=5174
```

If `.ports.env` is not found, the script defaults to port 5174.

### Backend Connection

The frontend is configured to connect to the backend API on port 8002. The backend URL is set in the API client (`src/api/client.ts`).

## Testing

### Validation Commands

Run these commands to verify the migration:

```bash
# Verify frontend files exist in new location
ls -la projects/tac-webbuilder/app/client/
ls -la projects/tac-webbuilder/app/client/src/

# Count files (should be 18+)
find projects/tac-webbuilder/app/client -type f | wc -l

# Verify no old path references in scripts
grep -r "app/webbuilder/client" scripts/

# Test startup
./scripts/start_webbuilder_ui.sh &
sleep 5
curl -s http://localhost:5174 | grep -q "<!doctype html"
pkill -f "vite"

# Run validation script
cd app/server && uv run pytest
```

## Notes

- All import paths in the frontend code are relative, so no code changes were required
- The old `/app/webbuilder/client/` directory structure was removed
- Frontend dependencies (4,468 lines in package-lock.json) were preserved
- Backend API remains at `/app/server/` and continues to work without changes
- The validation script now correctly checks the new path structure
- MCP configuration is tree-specific and updates automatically per tree
