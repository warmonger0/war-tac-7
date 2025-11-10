# E2E Test: Webbuilder Request Flow

## User Story
As a user, I want to submit a natural language request through the web UI, preview the generated issue, confirm it, and see it successfully posted to GitHub.

## Prerequisites
- Backend server running on http://localhost:8002
- Frontend running on http://localhost:5174
- Backend API endpoints functional (/api/request, /api/preview, /api/confirm)

## Test Steps

### 1. Navigate to Application
- Open http://localhost:5174
- Verify page loads successfully
- Verify page title contains "tac-webbuilder"
- Verify three tabs are visible: "New Request", "Workflows", "History"
- Verify "New Request" tab is active by default

### 2. Fill Out Request Form
- Verify textarea with placeholder "Describe what you want to build..." is visible
- Enter test NL input: "Build a simple REST API for managing tasks with CRUD operations"
- Verify project path input is visible (optional field)
- Enter project path: "/Users/test/projects/task-api"
- Verify auto-post checkbox is visible and unchecked by default
- Take screenshot: `webbuilder_request_form_filled.png`

### 3. Submit Request
- Click "Generate Issue" button
- Verify button shows "Processing..." state during submission
- Wait for API response (may take several seconds)
- Verify button returns to "Generate Issue" state

### 4. Verify Issue Preview
- Verify issue preview section appears with title
- Verify markdown content is rendered properly in preview
- Verify labels are displayed as badges
- Verify metadata section shows classification, workflow, and model_set
- Take screenshot: `webbuilder_issue_preview.png`

### 5. Open Confirmation Dialog
- Verify confirmation dialog modal appears (since auto-post was not checked)
- Verify modal overlay darkens background
- Verify modal title is "Confirm GitHub Issue"
- Verify issue preview is displayed in modal
- Verify two buttons: "Post to GitHub" and "Cancel"
- Take screenshot: `webbuilder_confirm_dialog.png`

### 6. Confirm and Post to GitHub
- Click "Post to GitHub" button
- Verify modal closes
- Wait for API response
- Verify success message appears with format "Issue #X created successfully! [URL]"
- Verify success message is styled with green background
- Verify form is reset (textarea and inputs cleared)
- Take screenshot: `webbuilder_post_success.png`

### 7. Verify Issue on GitHub (Optional)
- Extract GitHub URL from success message
- Open URL in browser
- Verify issue exists on GitHub with correct title and body
- Verify issue has expected labels

## Success Criteria
- Form submission works without errors
- Issue preview displays with proper markdown rendering
- Confirmation dialog appears when auto-post is disabled
- Issue is successfully posted to GitHub
- Success message displays with issue number and URL
- Form resets after successful submission
- All screenshots are captured successfully

## Error Handling Test Cases

### Test Case 1: Empty NL Input
- Clear textarea
- Click "Generate Issue" button
- Verify error message appears: "Please enter a description"
- Verify error message has red styling

### Test Case 2: Backend Unavailable
- Stop backend server
- Fill form and submit
- Verify error message displays connection error
- Restart backend server

### Test Case 3: Cancel Confirmation
- Submit request
- When confirmation dialog appears, click "Cancel"
- Verify modal closes
- Verify form retains entered values
- Verify no issue is posted

## Screenshots to Capture
1. `webbuilder_request_form_filled.png` - Form with NL input filled
2. `webbuilder_issue_preview.png` - Issue preview displayed
3. `webbuilder_confirm_dialog.png` - Confirmation dialog modal
4. `webbuilder_post_success.png` - Success message after posting
5. `webbuilder_error_empty_input.png` - Error state with empty input

## Notes
- This test validates the complete request submission workflow
- The backend must have functional /api/request, /api/preview, and /api/confirm endpoints
- GitHub token must be configured in backend for actual posting
- Test can be run with mock backend for preview testing
