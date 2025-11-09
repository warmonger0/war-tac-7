# E2E Test: Environment Setup Workflow

Test the complete environment configuration setup and validation workflow for tac-webbuilder.

## User Story

As a new developer joining the project
I want to easily configure my development environment
So that I can start working on tac-webbuilder without configuration errors

## Pre-Test Setup

1. **Backup existing configuration** (if any):
   ```bash
   [ -f .env ] && cp .env .env.backup
   ```

2. **Clean state** - Remove .env file to simulate fresh setup:
   ```bash
   rm -f .env
   ```

3. **Verify prerequisites**:
   - Claude Code is installed: `which claude`
   - GitHub CLI is installed: `gh --version`
   - GitHub CLI is authenticated: `gh auth status`

## Test Steps

### Part 1: Interactive Setup Script

1. Run the setup script:
   ```bash
   ./scripts/setup_env.sh
   ```

2. **Verify** the script displays:
   - Welcome banner with "tac-webbuilder Environment Configuration Setup"
   - Checks for .env.sample file
   - Creates .env from template
   - Shows "Required Configuration" section

3. When prompted for "Anthropic API key", enter a test value:
   - Input: `sk-ant-test-api-key-12345`
   - **Verify** success message: "✓ Set ANTHROPIC_API_KEY"

4. **Verify** Claude Code auto-detection:
   - Should show: "✓ Claude Code found at: [path]"
   - Path should match output of `which claude`

5. When prompted "Configure GitHub Personal Access Token?":
   - Input: `N` (skip)
   - **Verify** script continues to next section

6. When prompted "Configure OpenAI API Key?":
   - Input: `N` (skip)

7. When prompted "Configure E2B Cloud Sandbox?":
   - Input: `N` (skip)

8. When prompted "Configure Cloudflare Tunnel?":
   - Input: `N` (skip)

9. When prompted "Configure Cloudflare R2?":
   - Input: `N` (skip)

10. **Verify** completion message displays:
    - "✓ Environment Configuration Complete!"
    - Path to .env file
    - Next steps with validation command
    - Security reminder

11. **Verify** .env file was created:
    ```bash
    [ -f .env ] && echo "✓ .env file exists" || echo "✗ .env file missing"
    ```

12. **Verify** ANTHROPIC_API_KEY was set in .env:
    ```bash
    grep "ANTHROPIC_API_KEY=sk-ant-test" .env && echo "✓ API key set correctly" || echo "✗ API key not set"
    ```

### Part 2: Configuration Validation

13. Run the validation script:
    ```bash
    ./scripts/test_config.sh
    ```

14. **Verify** validation output shows:
    - "tac-webbuilder Configuration Validation" header
    - "✓ .env file found"
    - "REQUIRED CONFIGURATION" section
    - "✓ Anthropic API Key is set"

15. **Verify** tool availability checks:
    - "✓ Claude Code is available at: [path]"
    - "✓ GitHub CLI is installed"
    - "✓ GitHub CLI is authenticated"

16. **Verify** optional configuration shows:
    - "○ GitHub Personal Access Token is not set (optional)"
    - "○ OpenAI API Key is not set (optional)"
    - "○ E2B API Key is not set (optional)"
    - "○ Cloudflare Tunnel Token is not set (optional)"

17. **Verify** R2 configuration shows:
    - "○ Cloudflare R2 not configured (all variables empty)"
    - "Screenshots will use local file paths instead"

18. **Verify** Playwright MCP section shows:
    - "✓ Playwright MCP configuration file found"

19. **Verify** validation summary:
    - Shows "✓ All checks passed!" or "⚠ Configuration valid with X warning(s)"
    - Exit code is 0 (success)
    - Shows "Errors: 0"
    - Lists "Next Steps"

20. Check the script exit code:
    ```bash
    echo $?
    ```
    - **Verify** exit code is 0

### Part 3: Handling Missing Required Fields

21. Edit .env to remove the API key:
    ```bash
    sed -i.bak 's/^ANTHROPIC_API_KEY=.*/ANTHROPIC_API_KEY=/' .env
    ```

22. Run validation again:
    ```bash
    ./scripts/test_config.sh
    ```

23. **Verify** validation now shows error:
    - "✗ Anthropic API Key (ANTHROPIC_API_KEY) is not set"
    - "✗ Configuration incomplete: 1 error(s)"
    - Exit code is 1 (failure)

24. Check the script exit code:
    ```bash
    echo $?
    ```
    - **Verify** exit code is 1

### Part 4: Re-running Setup with Existing .env

25. Run setup script again:
    ```bash
    ./scripts/setup_env.sh
    ```

26. **Verify** overwrite protection:
    - Shows warning: "Warning: .env file already exists"
    - Prompts: "Do you want to overwrite it? (y/N)"

27. Answer "N" to decline overwrite:
    - **Verify** script shows: "Setup cancelled. Your existing .env file was not modified."
    - **Verify** script exits without modifying .env

28. Run setup script again and accept overwrite:
    ```bash
    ./scripts/setup_env.sh
    ```
    - Answer "y" to overwrite prompt
    - Provide API key: `sk-ant-test-restored-key`
    - Skip optional configuration (answer N to all)
    - **Verify** .env is recreated with new API key

29. Validate the restored configuration:
    ```bash
    ./scripts/test_config.sh
    ```
    - **Verify** validation passes with exit code 0

## Post-Test Cleanup

1. **Restore original configuration** (if backup exists):
   ```bash
   [ -f .env.backup ] && mv .env.backup .env || rm -f .env
   ```

2. **Verify cleanup**:
   ```bash
   ls -la .env* | grep -E '\.env$|\.env\.backup'
   ```

## Success Criteria

- ✅ Setup script creates .env file from .env.sample
- ✅ Setup script prompts for required configuration (ANTHROPIC_API_KEY)
- ✅ Setup script auto-detects Claude Code path
- ✅ Setup script handles optional configuration sections
- ✅ Setup script protects against accidental overwrite
- ✅ Setup script saves configuration correctly to .env
- ✅ Validation script detects missing .env file
- ✅ Validation script checks required variables
- ✅ Validation script validates tool availability
- ✅ Validation script reports errors for missing required fields
- ✅ Validation script shows warnings for optional fields
- ✅ Validation script returns correct exit codes (0 for success, 1 for errors)
- ✅ Complete workflow from setup to validation works smoothly
- ✅ All error messages are clear and actionable
- ✅ Scripts are idempotent (safe to run multiple times)

## Edge Cases Tested

- ✅ Missing .env file (fresh setup)
- ✅ Existing .env file (overwrite protection)
- ✅ Missing required variables (validation failure)
- ✅ Partial optional configuration (warnings only)
- ✅ Re-running setup script multiple times
- ✅ Platform compatibility (macOS sed vs Linux sed)

## Screenshots Captured

1. Initial setup script welcome screen
2. Required configuration prompts
3. Optional configuration prompts
4. Setup completion message
5. Validation script running with all checks passed
6. Validation script showing errors for missing API key
7. Overwrite protection prompt
8. Final successful validation

## Notes

- This test uses dummy API keys for testing purposes
- Actual API keys should never be committed or shared
- Test validates the workflow but doesn't test actual API connectivity
- Scripts should work on both macOS and Linux platforms
