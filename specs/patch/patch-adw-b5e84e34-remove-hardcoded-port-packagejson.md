# Patch: Remove hardcoded port from package.json dev script

## Metadata
adw_id: `b5e84e34`
review_change_request: `Issue #1: Package.json contains hardcoded port '--port 5174' in the dev script which overrides the vite.config.ts port configuration that reads from .ports.env (FRONTEND_PORT=9213). This breaks the worktree port isolation system where each worktree should use its own port from .ports.env. Resolution: Remove '--port 5174' from package.json dev script to allow vite.config.ts to control the port based on .ports.env. The dev script should be 'vite' not 'vite --port 5174'. Severity: blocker`

## Issue Summary
**Original Spec:** N/A (Review issue)
**Issue:** The `dev` script in `app/client/package.json` contains a hardcoded `--port 5174` flag that overrides the port configuration in `vite.config.ts`. The vite config correctly reads `FRONTEND_PORT=9213` from `.ports.env` for worktree port isolation, but the CLI flag takes precedence and breaks this system.
**Solution:** Remove the `--port 5174` flag from the dev script in package.json, changing it from `"dev": "vite --port 5174"` to `"dev": "vite"`. This allows vite.config.ts to control the port using the FRONTEND_PORT value from .ports.env.

## Files to Modify
Use these files to implement the patch:

- `app/client/package.json` - Remove `--port 5174` from the dev script

## Implementation Steps
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Update package.json dev script
- Open `app/client/package.json`
- Locate the `"dev"` script on line 7
- Change `"dev": "vite --port 5174"` to `"dev": "vite"`
- This allows vite.config.ts to control the port via FRONTEND_PORT from .ports.env

## Validation
Execute every command to validate the patch is complete with zero regressions.

1. **Verify port configuration**: Check that `vite.config.ts` correctly reads FRONTEND_PORT from `.ports.env`
   ```bash
   grep -A 2 "frontendPort" app/client/vite.config.ts
   ```

2. **TypeScript Type Check**: Ensure no type errors introduced
   ```bash
   cd app/client && bun tsc --noEmit
   ```

3. **Frontend Build**: Validate build process works correctly
   ```bash
   cd app/client && bun run build
   ```

4. **Manual verification**: Start the dev server and confirm it uses port 9213 (not 5174)
   ```bash
   cd app/client && bun run dev
   ```
   Expected: Server should start on http://localhost:9213

## Patch Scope
**Lines of code to change:** 1 line
**Risk level:** low
**Testing required:** Verify dev server starts on correct port (9213) from .ports.env instead of hardcoded 5174
