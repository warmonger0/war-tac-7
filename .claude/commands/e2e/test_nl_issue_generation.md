# E2E Test: Natural Language to GitHub Issue Generation

## User Story
As a developer, I want to describe my feature requirements in natural language and have the system automatically generate a properly formatted GitHub issue with appropriate ADW workflows.

## Prerequisites
- Backend server running on port 8000
- Frontend running on port 5173
- ANTHROPIC_API_KEY environment variable set
- GitHub CLI (`gh`) installed (optional for full flow)

## Test Steps

### 1. Start Services
```bash
# Terminal 1: Start backend
cd app/server
uv run uvicorn server:app --reload --port 8000

# Terminal 2: Start frontend
cd app/client
bun run dev
```

### 2. Navigate to Application
- Open browser to http://localhost:5173
- Verify the application loads successfully
- Screenshot: Main application interface

### 3. Locate Issue Builder Section
- Scroll down to find "WebBuilder - GitHub Issue Generator" section
- Verify GitHub CLI status is displayed (installed/authenticated status)
- Verify project context is detected and displayed
- Screenshot: Issue Builder section with status indicators

### 4. Test Natural Language Input - Feature Request
- In the text area, enter: "Add a dark mode toggle to the settings page that remembers user preference and applies the theme across all components"
- Verify character count updates (should show ~120/5000)
- Click "Generate Issue" button
- Verify button shows loading state
- Screenshot: Input with natural language request

### 5. Verify Issue Preview
- Wait for processing to complete (should take 2-5 seconds)
- Verify issue preview appears with:
  - Issue type badge showing "FEATURE"
  - Workflow badge (e.g., "adw_plan_build_test_iso (base)")
  - Confidence score percentage
  - Formatted issue content in preview box
  - Extracted requirements list
  - Time estimation based on complexity
- Screenshot: Complete issue preview

### 6. Test Issue Preview Content
- Verify the preview contains:
  - Clear title derived from the input
  - Description section with user request
  - Requirements section with bullet points
  - Technical approach section
  - Workflow specification
  - Type classification (/feature)
- Screenshot: Scrolled preview showing all sections

### 7. Test Natural Language Input - Bug Report
- Click "Edit" to return to input
- Clear the input and enter: "The login button on the homepage is not working when clicked. It should redirect to the authentication page but nothing happens."
- Click "Generate Issue"
- Verify issue type changes to "BUG"
- Verify workflow is "adw_plan_build_test_iso"
- Verify bug-specific sections appear (Steps to Reproduce, Expected vs Actual)
- Screenshot: Bug issue preview

### 8. Test Error Handling - Short Input
- Click "Edit" to return to input
- Enter only: "Fix it"
- Click "Generate Issue"
- Verify error message appears: "Input is too short. Please provide more details."
- Screenshot: Error message for short input

### 9. Test Error Handling - Empty Input
- Clear the input completely
- Click "Generate Issue"
- Verify error message appears: "Input cannot be empty"
- Verify button remains enabled after error
- Screenshot: Error message for empty input

### 10. Test Project Context Detection
- Verify the Project Context section shows:
  - Type: Existing Codebase
  - Framework: (if detected)
  - Backend: FastAPI (should be detected)
  - Complexity level with appropriate color coding
- Screenshot: Project context display

### 11. Test GitHub CLI Status (if available)
- If GitHub CLI is installed:
  - Verify green checkmark for "Installed"
  - If authenticated, verify username display
- If not authenticated:
  - Verify warning message about running `gh auth login`
- Screenshot: GitHub CLI status

### 12. Test Issue Posting (if GitHub CLI authenticated)
- Generate a test issue
- Click "Post to GitHub" button
- Verify button shows loading state
- If successful:
  - Verify success message with issue number
  - Verify link to view issue on GitHub
- If not authenticated:
  - Verify appropriate error message
- Screenshot: Success or error state

### 13. Test Clear Functionality
- After generating an issue, click "Clear" button
- Verify:
  - Input field is cleared
  - Character count resets to 0/5000
  - Preview section is hidden
  - Any error messages are cleared
- Screenshot: Cleared state

### 14. Test Keyboard Shortcut
- Enter a natural language request
- Press Cmd+Enter (Mac) or Ctrl+Enter (Windows/Linux)
- Verify this triggers the "Generate Issue" action
- Screenshot: Generated issue from keyboard shortcut

## Expected Results

### Success Criteria
- ✅ Natural language input successfully converts to structured GitHub issue
- ✅ Issue type classification is accurate (feature/bug/chore)
- ✅ Project context is correctly detected
- ✅ ADW workflow suggestion matches complexity
- ✅ Issue preview displays all required sections
- ✅ Requirements are extracted from natural language
- ✅ Time estimation reflects project complexity
- ✅ Error handling works for invalid inputs
- ✅ GitHub CLI status is accurately displayed
- ✅ UI remains responsive during processing
- ✅ Clear function resets all fields properly

### Performance Criteria
- Issue generation completes in < 5 seconds
- UI updates immediately on user actions
- No console errors during normal operation
- Character count updates in real-time

## Validation Points

1. **API Integration**
   - Check Network tab for `/api/webbuilder/process` POST request
   - Verify request payload contains nl_input
   - Verify response contains issue object with all fields

2. **Error Handling**
   - API errors display user-friendly messages
   - Network failures are handled gracefully
   - Invalid responses don't break the UI

3. **State Management**
   - Component state updates correctly
   - Previous results clear when starting new generation
   - Loading states prevent duplicate submissions

## Troubleshooting

### Common Issues

1. **"ANTHROPIC_API_KEY not set" error**
   - Solution: Set the environment variable in backend .env file
   - Restart the backend server

2. **GitHub CLI not detected**
   - Solution: Install with `brew install gh` (Mac) or appropriate method
   - Run `gh auth login` to authenticate

3. **Project context not detected**
   - Verify you're running from project root
   - Check file permissions

4. **Slow response times**
   - Check network latency to Anthropic API
   - Verify no rate limiting is occurring

## Screenshots Required
1. Initial Issue Builder section view
2. Natural language input entered
3. Processing/loading state
4. Complete issue preview (feature)
5. Complete issue preview (bug)
6. Error message display
7. GitHub CLI status display
8. Success message after posting (if available)
9. Cleared/reset state

## Notes
- The Anthropic API key is required for this feature to work
- GitHub CLI authentication is optional but recommended for full functionality
- Processing time may vary based on API response times
- The feature gracefully degrades if GitHub CLI is not available