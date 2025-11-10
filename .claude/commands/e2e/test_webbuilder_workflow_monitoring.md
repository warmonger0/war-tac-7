# E2E Test: Webbuilder Workflow Monitoring

## User Story
As a user, I want to monitor active ADW workflows in real-time through the web dashboard, see their progress across different phases, and navigate to GitHub to view issues.

## Prerequisites
- Backend server running on http://localhost:8002
- Frontend running on http://localhost:5174
- Backend API endpoint functional (/api/workflows)
- WebSocket endpoint functional (ws://localhost:8002/ws)
- At least one active workflow in the system (or ability to create one via API)

## Test Steps

### 1. Navigate to Workflows Tab
- Open http://localhost:5174
- Verify page loads successfully
- Click on "Workflows" tab in navigation bar
- Verify tab becomes active (highlighted with blue color)
- Verify tab content area updates to show workflow dashboard
- Take screenshot: `webbuilder_workflows_tab.png`

### 2. Verify Workflow Dashboard Display
- Verify heading "Active Workflows (N)" is displayed with correct count
- Verify workflow cards are displayed in a grid layout
- Verify each card shows:
  - Issue number (e.g., "Issue #24")
  - ADW ID
  - Status badge with phase name
  - Progress bar with all phases
  - "View on GitHub →" link
- Take screenshot: `webbuilder_workflow_dashboard.png`

### 3. Verify Workflow Card Details
- Select first workflow card
- Verify issue number is displayed prominently
- Verify ADW ID is shown
- Verify status badge color matches phase:
  - Plan: blue
  - Build: purple
  - Test: yellow
  - Review: orange
  - Document: indigo
  - Ship: green
- Verify progress bar shows:
  - Completed phases with green checkmarks
  - Current phase highlighted in blue
  - Pending phases in gray
- Take screenshot: `webbuilder_workflow_card_detail.png`

### 4. Test GitHub Link
- Click "View on GitHub →" link on a workflow card
- Verify link opens in new tab (target="_blank")
- Verify link points to correct GitHub issue URL
- Verify issue exists on GitHub
- Close GitHub tab and return to dashboard

### 5. Test Empty State
- If no workflows exist:
  - Verify empty state message is displayed
  - Verify message says "No active workflows"
  - Verify helpful text: "Submit a request to start a new workflow"
  - Take screenshot: `webbuilder_workflows_empty.png`

### 6. Test Real-Time Updates (WebSocket)
- Establish WebSocket connection (automatic on page load)
- Verify connection status in browser console
- Trigger workflow phase update via backend or simulation
- Verify workflow card updates automatically without page refresh:
  - Status badge changes to new phase
  - Progress bar updates to show new position
  - Animation or transition occurs smoothly
- Take screenshot before and after update:
  - `webbuilder_workflow_before_update.png`
  - `webbuilder_workflow_after_update.png`

### 7. Test Polling Fallback
- Verify dashboard polls /api/workflows every 5 seconds
- Observe network tab to confirm periodic API calls
- Verify dashboard updates even if WebSocket is unavailable

### 8. Test Multiple Workflows
- If multiple workflows exist:
  - Verify all workflows are displayed in grid
  - Verify each card is independent
  - Verify cards display different phases correctly
  - Verify grid is responsive (3 columns on desktop, 2 on tablet, 1 on mobile)
- Take screenshot: `webbuilder_multiple_workflows.png`

### 9. Test Loading State
- Refresh page
- Verify loading message appears: "Loading workflows..."
- Verify loading message disappears when data loads
- Verify smooth transition from loading to content

### 10. Test Error State
- Stop backend server
- Refresh workflows tab
- Verify error message displays with red styling
- Verify error message shows: "Error loading workflows: [error details]"
- Take screenshot: `webbuilder_workflows_error.png`
- Restart backend server

## Success Criteria
- Workflows tab displays correctly
- Workflow cards show all required information
- Status badges use correct colors for each phase
- Progress bars accurately represent workflow phase
- GitHub links work and open in new tabs
- Empty state displays when no workflows exist
- Real-time updates work via WebSocket
- Polling fallback functions when WebSocket unavailable
- Loading and error states display appropriately
- Dashboard is responsive across different screen sizes
- All screenshots are captured successfully

## Real-Time Update Test Details

### Simulating Workflow Updates
Option 1: Use backend API to update workflow phase
```bash
curl -X POST http://localhost:8002/api/workflows/[adw_id]/update \
  -H "Content-Type: application/json" \
  -d '{"phase": "test"}'
```

Option 2: Trigger workflow progression naturally by letting ADW run

### Expected WebSocket Message Format
```json
{
  "type": "workflow_progress",
  "adw_id": "abc123",
  "phase": "test"
}
```

## Screenshots to Capture
1. `webbuilder_workflows_tab.png` - Workflows tab selected
2. `webbuilder_workflow_dashboard.png` - Dashboard with workflow cards
3. `webbuilder_workflow_card_detail.png` - Close-up of single workflow card
4. `webbuilder_workflows_empty.png` - Empty state with no workflows
5. `webbuilder_workflow_before_update.png` - Card before real-time update
6. `webbuilder_workflow_after_update.png` - Card after real-time update
7. `webbuilder_multiple_workflows.png` - Multiple workflows in grid
8. `webbuilder_workflows_error.png` - Error state display

## Notes
- This test validates the workflow monitoring dashboard functionality
- Real-time updates are critical for user experience
- The backend must have functional /api/workflows endpoint
- WebSocket server must be running on ws://localhost:8002/ws
- Test can be run with mock workflows for development
- Progress bar should animate smoothly between phase transitions
