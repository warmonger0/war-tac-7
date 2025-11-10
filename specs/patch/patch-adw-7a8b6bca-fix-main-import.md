# Patch: Add Missing App Import to main.py

## Metadata
adw_id: `7a8b6bca`
review_change_request: `Issue #1: main.py is missing the import statement 'from server import app'. The file only contains the if __name__ == '__main__' block but doesn't expose the app object at module level, causing uvicorn to fail with 'ERROR: Error loading ASGI app. Attribute "app" not found in module "main"' when running 'uvicorn main:app'. Resolution: Add 'from server import app' at the top of main.py before the if __name__ == '__main__' block. The spec explicitly shows this pattern: 'from app.server.server import app' or simpler 'from server import app' when running from within app/server/ directory. Severity: blocker`

## Issue Summary
**Original Spec:** specs/issue-41-adw-7a8b6bca-sdlc_planner-reorganize-backend-structure.md
**Issue:** The `app/server/main.py` file is missing the import statement `from server import app`, causing uvicorn to fail with "ERROR: Error loading ASGI app. Attribute 'app' not found in module 'main'" when attempting to run `uvicorn main:app`.
**Solution:** Add `from server import app` at the top of main.py before the `if __name__ == '__main__'` block to expose the FastAPI app object at module level, enabling uvicorn to successfully load the application.

## Files to Modify
Use these files to implement the patch:

- `app/server/main.py` - Add the missing import statement at the top of the file

## Implementation Steps
IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Add import statement to main.py
- Add `from server import app` as the first line in `app/server/main.py`
- This exposes the FastAPI app object at module level so uvicorn can discover it
- Preserve the existing `if __name__ == '__main__'` block unchanged

## Validation
Execute every command to validate the patch is complete with zero regressions.

```bash
# Verify the import works from within app/server directory
cd app/server && python3 -c "from main import app; print('✅ main.py import successful')"

# Verify the app can be imported from server module
cd app/server && python3 -c "from server import app; print('✅ server.py import successful')"

# Run Python syntax check
cd app/server && uv run python -m py_compile main.py

# Run backend tests to ensure no regressions
cd app/server && uv run pytest tests/ -v --tb=short

# Start backend with uvicorn and verify it loads successfully
cd app/server && timeout 10 uv run uvicorn main:app --host 0.0.0.0 --port 8002 &
sleep 5
curl -f http://localhost:8002/health || echo "❌ Health check failed"
pkill -f "uvicorn main:app"
```

## Patch Scope
**Lines of code to change:** 1 line added (1 total change)
**Risk level:** low
**Testing required:** Import validation, syntax check, backend test suite, health endpoint verification
