# E2E Test: Web Backend API

## User Story
As a tac-webbuilder developer
I want to verify that the web backend API is fully functional
So that I can confidently integrate it with the frontend

## Test Objective
Verify all web backend API endpoints are working correctly with real HTTP requests and the server can handle concurrent connections including WebSocket.

## Prerequisites
- All dependencies installed (`uv sync --group dev`)
- Port 8002 available
- No existing server running on port 8002

## Test Steps

### 1. Start the Server
```bash
cd /Users/Warmonger0/tac/tac-7/projects/tac-webbuilder
./scripts/start_web.sh &
SERVER_PID=$!
sleep 5
```

**Expected**: Server starts successfully and listens on port 8002

### 2. Health Check
```bash
curl -s http://localhost:8002/api/health | python3 -m json.tool
```

**Expected**:
```json
{
  "status": "ok",
  "version": "1.0.0",
  "timestamp": "2025-11-09T..."
}
```

**Validation**:
- HTTP status 200
- `status` field is "ok"
- `version` field is "1.0.0"

### 3. API Root
```bash
curl -s http://localhost:8002/ | python3 -m json.tool
```

**Expected**:
```json
{
  "name": "tac-webbuilder API",
  "version": "1.0.0",
  "description": "Web backend API for tac-webbuilder",
  "docs": "/docs",
  "redoc": "/redoc",
  "health": "/api/health",
  "websocket": "/ws"
}
```

**Validation**:
- HTTP status 200
- Contains API information and documentation links

### 4. API Documentation
```bash
curl -s http://localhost:8002/docs -I
```

**Expected**: HTTP 200 and HTML content

```bash
curl -s http://localhost:8002/redoc -I
```

**Expected**: HTTP 200 and HTML content

**Validation**:
- Both documentation endpoints are accessible
- Return HTML content type

### 5. List Workflows (Empty)
```bash
curl -s http://localhost:8002/api/workflows | python3 -m json.tool
```

**Expected**:
```json
{
  "workflows": [],
  "total_count": 0
}
```

**Validation**:
- HTTP status 200
- Empty workflows list (no active workflows yet)

### 6. List Projects (Empty)
```bash
curl -s http://localhost:8002/api/projects | python3 -m json.tool
```

**Expected**:
```json
{
  "projects": [],
  "total_count": 0
}
```

**Validation**:
- HTTP status 200
- Empty projects list initially

### 7. Add Project
```bash
curl -s -X POST http://localhost:8002/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "project_path": "/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder"
  }' | python3 -m json.tool
```

**Expected**:
```json
{
  "project_path": "/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder",
  "project_name": "tac-webbuilder",
  "framework": null,
  "language": "Python",
  "tech_stack": ["Python"],
  "build_tools": ["uv"],
  "test_frameworks": ["pytest"],
  "has_git": true,
  "repo_url": "..."
}
```

**Validation**:
- HTTP status 201
- Project context detected correctly
- Language detected as Python
- Build tool detected as uv

### 8. List Projects (With Added Project)
```bash
curl -s http://localhost:8002/api/projects | python3 -m json.tool
```

**Expected**:
```json
{
  "projects": [
    {
      "project_id": "tac-webbuilder",
      "project_name": "tac-webbuilder",
      "project_path": "/Users/Warmonger0/tac/tac-7/projects/tac-webbuilder",
      "framework": null,
      "language": "Python",
      "last_used": null
    }
  ],
  "total_count": 1
}
```

**Validation**:
- HTTP status 200
- Project appears in list

### 9. Get Request History (Empty)
```bash
curl -s http://localhost:8002/api/history | python3 -m json.tool
```

**Expected**:
```json
{
  "history": [],
  "total_count": 0,
  "has_more": false
}
```

**Validation**:
- HTTP status 200
- Empty history initially

### 10. Test CORS Headers
```bash
curl -s -X OPTIONS http://localhost:8002/api/health \
  -H "Origin: http://localhost:5174" \
  -H "Access-Control-Request-Method: GET" \
  -I
```

**Expected**:
- HTTP status 200 or 204
- CORS headers present (in actual browser, not TestClient)

**Validation**:
- Server accepts OPTIONS requests
- CORS is configured (headers may not show in curl)

### 11. Test Error Handling (Invalid Endpoint)
```bash
curl -s http://localhost:8002/api/nonexistent | python3 -m json.tool
```

**Expected**:
```json
{
  "detail": "Not Found"
}
```

**Validation**:
- HTTP status 404
- Returns proper error response

### 12. Test Invalid Request (Missing Required Fields)
```bash
curl -s -X POST http://localhost:8002/api/projects \
  -H "Content-Type: application/json" \
  -d '{}' | python3 -m json.tool
```

**Expected**:
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "project_path"],
      "msg": "Field required",
      "input": {}
    }
  ]
}
```

**Validation**:
- HTTP status 422 (Unprocessable Entity)
- Validation error for missing field

### 13. Test WebSocket Connection
```bash
# Install websocat if not present: brew install websocat
echo '{"test": "hello"}' | websocat -n1 ws://localhost:8002/ws 2>&1
```

**Expected**:
- Connection established
- Receives welcome message
- Connection closes gracefully

**Validation**:
- WebSocket endpoint is accessible
- Server accepts WebSocket connections

### 14. Cleanup - Stop the Server
```bash
pkill -f "uvicorn interfaces.web.server:app" || kill $SERVER_PID 2>/dev/null || true
sleep 2
```

**Expected**: Server stops cleanly

## Success Criteria
-  All API endpoints return expected HTTP status codes
-  Health check returns OK status
-  API documentation is accessible at /docs and /redoc
-  Project addition and listing works correctly
-  Project context detection identifies language and tools
-  Workflow listing works (returns empty list)
-  History endpoint works (returns empty list)
-  Error handling returns proper HTTP status codes
-  Validation errors return 422 with details
-  WebSocket endpoint accepts connections
-  Server starts and stops cleanly

## Notes
- This test uses the actual HTTP endpoints, not mocked APIs
- Test requires the server to be running
- Some tests expect empty responses (no workflows/history initially)
- Request submission test omitted as it requires GitHub CLI and API key
- WebSocket test is basic connectivity check only
- Project context detection may vary based on actual project structure

## Troubleshooting
- If port 8002 is in use: `lsof -ti:8002 | xargs kill -9`
- If server doesn't start: Check logs for errors, ensure dependencies installed
- If CORS test fails: This is expected with curl, test in browser or with proper client
- If WebSocket test fails: Install websocat or use another WebSocket client
