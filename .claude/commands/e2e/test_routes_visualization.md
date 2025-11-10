# E2E Test: Routes Visualization

Test the routes visualization tab functionality in the tac-webbuilder web interface.

## User Story

As a developer
I want to view all API routes with their methods, paths, handlers, and descriptions
So that I can discover and reference endpoints easily without searching through code

## Prerequisites

- Backend server running on `http://localhost:8000`
- tac-webbuilder frontend running on `http://localhost:5174`
- Routes API endpoint `/api/routes` returning route data

## Test Steps

### Initial Navigation

1. Navigate to the tac-webbuilder Application URL: `http://localhost:5174`
2. Take a screenshot of the initial tac-webbuilder page
3. **Verify** the page title contains "tac-webbuilder"
4. **Verify** tab navigation is visible with tabs: New Request, Workflows, History, API Routes

### Routes Tab Access

5. Click the "API Routes" tab
6. Take a screenshot after clicking the tab
7. **Verify** the page heading shows "API Routes"
8. **Verify** the filter controls are visible:
   - Search input with placeholder text
   - Method filter dropdown
9. **Verify** the summary text shows route count (e.g., "Showing X of Y routes")

### Routes Table Display

10. **Verify** the routes table displays with columns:
    - Method (with colored badges)
    - Path
    - Handler
    - Description
11. **Verify** at least one route is displayed in the table
12. **Verify** method badges are color-coded:
    - GET = blue
    - POST = green
    - DELETE = red
13. Take a screenshot of the routes table with all routes visible

### Method Filtering

14. Click the method filter dropdown
15. Select "GET" from the dropdown
16. **Verify** only GET routes are shown in the table
17. **Verify** the summary text updates (e.g., "Showing 5 of 10 routes")
18. Take a screenshot of the filtered GET routes
19. Select "POST" from the dropdown
20. **Verify** only POST routes are shown
21. Take a screenshot of the filtered POST routes

### Search Functionality

22. Select "All Methods" from the method filter dropdown to reset
23. Enter "api" in the search input box
24. **Verify** only routes containing "api" in path, handler, or description are shown
25. **Verify** the summary text updates to reflect filtered count
26. Take a screenshot of the search results
27. Clear the search input
28. **Verify** all routes are shown again

### Combined Filters

29. Select "GET" from the method filter
30. Enter "health" in the search box
31. **Verify** only GET routes matching "health" are shown
32. **Verify** if `/api/health` exists, it should be displayed
33. Take a screenshot of the combined filter results

### Route Details Verification

34. **Verify** at least one route shows all required fields:
    - Method badge is visible and color-coded
    - Path is displayed in monospace font
    - Handler function name is shown
    - Description is not empty or "N/A"
35. Take a screenshot focusing on a single route row

### Empty State (if applicable)

36. Enter "nonexistentroute12345" in the search box
37. **Verify** a "No routes match your filters" message is displayed
38. Take a screenshot of the empty state

## Success Criteria

- ✅ API Routes tab is accessible and loads successfully
- ✅ Routes table displays with all four columns
- ✅ At least 5 routes are displayed (server should have multiple endpoints)
- ✅ Method badges are color-coded correctly
- ✅ Method filter dropdown works and filters routes
- ✅ Search input filters routes by path, handler, or description
- ✅ Combined filters (method + search) work correctly
- ✅ Summary text accurately reflects filtered count
- ✅ Empty state message displays when no routes match
- ✅ All 8 required screenshots are captured

## Expected Routes

The test should find at least these routes:
- `GET /api/health`
- `GET /api/routes`
- `GET /api/schema`
- `POST /api/upload`
- `POST /api/query`
- `DELETE /api/table/{table_name}`

## Notes

- If the routes table is empty, verify the backend server is running
- If filtering doesn't work, check browser console for JavaScript errors
- Screenshots should clearly show UI state at each verification point
- Test should be idempotent and not modify any data
