# E2E Test: Landing Page Visual Design

Test the visual design enhancements of the tac-webbuilder landing page including centered content and visual separator.

## User Story

As a user of tac-webbuilder
I want to see a modern, clean, and centered landing page layout
So that I have a professional and visually appealing experience when accessing the application

## Test Steps

1. Navigate to the `Application URL`
2. Take a screenshot of the initial landing page state
3. **Verify** the page displays correctly with:
   - Header section with application name
   - Tagline text
   - Navigation bar with tabs
   - Visual separator between navigation and main content

4. **Verify** content alignment:
   - Check that "tac-webbuilder" heading is center-aligned
   - Check that "Build web apps with natural language" tagline is center-aligned
   - Check that navigation tabs are center-aligned in their container

5. **Verify** visual separator:
   - Use browser DevTools to inspect the visual separator element
   - Verify it has a green background color (#10b981)
   - Verify it has box-shadow applied (for depth effect)
   - Verify it spans the full width of the page
   - Verify it has a height of 3px

6. Take a screenshot showing the visual separator and centered content

7. Test responsive behavior:
   - Resize browser to tablet width (768px)
   - Take a screenshot of tablet view
   - **Verify** centered content remains properly aligned
   - **Verify** visual separator spans full width

8. Resize browser to mobile width (375px)
   - Take a screenshot of mobile view
   - **Verify** centered content is still readable and properly aligned
   - **Verify** visual separator spans full width

9. Restore browser to desktop size (1280px)
   - Take a screenshot of desktop view
   - **Verify** all elements are properly displayed

## Success Criteria
- Landing page loads without errors
- "tac-webbuilder" heading is center-aligned
- Tagline "Build web apps with natural language" is center-aligned
- Navigation tabs are center-aligned
- Visual separator is present between navigation and main content
- Visual separator has green color (#10b981)
- Visual separator has drop shadow effect (box-shadow)
- Visual separator spans full width
- Design is responsive at tablet (768px) and mobile (375px) widths
- At least 5 screenshots are captured (initial, separator detail, tablet, mobile, desktop)
