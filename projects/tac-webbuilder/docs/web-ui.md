# TAC WebBuilder Web UI Documentation

## Overview

The TAC WebBuilder Web UI provides an intuitive interface for managing web projects, processing natural language requirements, and automating development workflows.

## Accessing the UI

Start the server and navigate to:
```
http://localhost:8000
```

## Dashboard

The dashboard provides an overview of:
- Active projects
- Recent issues
- Processing history
- System status

### Features
- Real-time status updates
- Quick action buttons
- Project statistics
- Recent activity feed

## Natural Language Processing Interface

### Processing Requests

1. Navigate to the NL Processing tab
2. Enter your requirement in natural language
3. Click "Process" to analyze the request
4. Review the extracted information:
   - Issue type (feature, bug, chore)
   - Requirements list
   - Technical approach
   - Suggested workflow

### Example Inputs

**Feature Request:**
```
Create a user authentication system with email/password login,
OAuth integration, and password reset functionality
```

**Bug Report:**
```
Users are getting 500 errors when uploading files larger than 10MB.
This happens on the /upload endpoint and affects all users.
```

**Chore:**
```
Update dependencies to latest versions and fix security vulnerabilities
found in the npm audit report
```

## File Processing

### CSV to SQLite Conversion

1. Navigate to File Processing tab
2. Select "CSV to SQLite"
3. Upload your CSV file
4. Review column mapping
5. Click "Convert"
6. Download the generated SQLite database

**Supported Features:**
- Automatic column name cleaning
- Type inference
- Handling inconsistent data
- Progress tracking

### JSON to SQLite Conversion

1. Select "JSON to SQLite"
2. Upload JSON file (array or JSONL)
3. Review detected schema
4. Adjust flattening options if needed
5. Convert and download

**Options:**
- Flatten nested objects
- Handle arrays
- Custom field separators
- Schema preview

## SQL Query Generator

### Generating Queries

1. Navigate to SQL Generator
2. Upload or connect to database
3. Enter question in natural language
4. Review generated SQL query
5. Execute or copy query

**Example Questions:**
```
Show me all users who registered in the last 30 days

Find the top 10 products by revenue

Get average order value by month for 2024
```

### Query Features

- Syntax highlighting
- Query explanation
- Execution preview
- Result export (CSV, JSON)
- Query history

## GitHub Integration

### Creating Issues

1. Navigate to GitHub tab
2. Select repository
3. Fill in issue details or use NL processing
4. Preview formatted issue
5. Post to GitHub

**Issue Templates:**
- Feature request
- Bug report
- Chore/maintenance

### Issue Management

- View existing issues
- Filter by label/status
- Bulk operations
- Link to GitHub directly

## Project Templates

### Creating New Projects

1. Click "New Project"
2. Select template:
   - React + Vite
   - Next.js
   - Vanilla JavaScript
3. Configure options:
   - Project name
   - Directory
   - Git initialization
   - MCP integration
4. Click "Create"

### Template Options

**React + Vite:**
- TypeScript configured
- Vite dev server
- Hot module replacement
- ESLint + Prettier

**Next.js:**
- App Router
- TypeScript
- API routes included
- Optimized for production

**Vanilla:**
- Pure HTML/CSS/JS
- No build tools
- Quick prototyping
- Minimal setup

## Project Detection

### Analyzing Existing Projects

1. Navigate to Project Analysis
2. Enter project path or upload project
3. View detected information:
   - Framework
   - Backend technology
   - Build tools
   - Package manager
   - Git status
   - Complexity score

### Workflow Suggestions

Based on analysis, receive suggestions for:
- Recommended ADW workflow
- Integration steps
- Configuration changes
- Best practices

## Settings

### Configuration

**General Settings:**
- Default LLM provider (OpenAI/Anthropic)
- Auto-save preferences
- Theme (light/dark)
- Language

**API Keys:**
- OpenAI API key
- Anthropic API key
- GitHub token

**GitHub Settings:**
- Default repository
- Auto-post issues
- Default labels
- Issue template preferences

**Processing Options:**
- Temperature setting
- Max tokens
- Workflow preferences
- Auto-detection settings

### Workspace Management

- Switch between projects
- Manage multiple repositories
- Workspace-specific settings
- Import/export configuration

## Keyboard Shortcuts

### Global
- `Ctrl/Cmd + K` - Command palette
- `Ctrl/Cmd + P` - Quick project switch
- `Ctrl/Cmd + S` - Save/submit
- `Esc` - Close modal/cancel

### Editor
- `Ctrl/Cmd + Enter` - Process/submit
- `Ctrl/Cmd + /` - Comment line
- `Alt + Up/Down` - Move line
- `Ctrl/Cmd + D` - Duplicate line

## Data Visualization

### Query Results

View SQL query results in multiple formats:
- Table view (sortable, filterable)
- Chart view (bar, line, pie)
- JSON view (raw data)
- Export options

### Project Insights

Visualize project metrics:
- Complexity score
- File count
- Dependencies graph
- Issue trends

## Collaboration Features

### Sharing

- Share processed requirements
- Export reports
- Generate shareable links
- Collaborate on issues

### History

- View processing history
- Replay previous requests
- Compare results
- Track changes

## Mobile Experience

The UI is responsive and works on mobile devices:
- Touch-optimized controls
- Mobile-friendly layouts
- Swipe gestures
- Offline capability (coming soon)

## Customization

### Themes

Choose from:
- Light mode
- Dark mode
- High contrast
- Custom themes (via CSS)

### Layout

Customize your workspace:
- Panel positions
- Show/hide sections
- Saved layouts
- Keyboard-first mode

## Performance

### Optimization Features

- Lazy loading of components
- Virtual scrolling for large datasets
- Request caching
- Background processing
- Progressive enhancement

### Monitoring

- Real-time performance metrics
- API response times
- Processing queue status
- Resource usage

## Accessibility

The UI follows WCAG 2.1 AA guidelines:
- Keyboard navigation
- Screen reader support
- High contrast mode
- Focus indicators
- ARIA labels

## Browser Support

Supported browsers:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Troubleshooting

### Common Issues

**UI not loading:**
- Check server is running
- Clear browser cache
- Check console for errors
- Verify network connection

**Slow performance:**
- Close unused tabs
- Reduce query result size
- Check system resources
- Use pagination

**Authentication errors:**
- Verify API keys
- Check GitHub token
- Refresh connection
- Clear session storage

## Best Practices

1. **Save frequently**: Use auto-save or manual save regularly
2. **Use templates**: Start with templates for consistency
3. **Review before posting**: Always preview GitHub issues
4. **Test queries**: Validate SQL before execution
5. **Monitor usage**: Check API usage limits

## Advanced Features

### Batch Operations

Process multiple files or requests:
- Bulk file conversion
- Multiple issue creation
- Batch SQL queries
- Parallel processing

### Automation

Set up automated workflows:
- Scheduled processing
- Webhook triggers
- CI/CD integration
- Auto-posting rules

### Extensions

Install extensions for:
- Custom templates
- Additional LLM providers
- Integration plugins
- Custom visualizations

## Additional Resources

- [CLI Documentation](cli.md)
- [API Documentation](api.md)
- [Architecture Overview](architecture.md)
- [Examples and Tutorials](examples.md)
- [Troubleshooting Guide](troubleshooting.md)
