#!/bin/bash

# TAC WebBuilder - Existing Project Integration Script
# Adds ADW capabilities to existing projects

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TEMPLATES_DIR="$PROJECT_ROOT/templates/existing_webapp"

# Default values
TARGET_PROJECT=""
DRY_RUN=false
SKIP_BACKUP=false

# Print colored message
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Show usage
show_usage() {
    cat << EOF
TAC WebBuilder - Existing Project Integration

Usage: $0 [OPTIONS] PROJECT_PATH

Arguments:
    PROJECT_PATH            Path to existing project directory

Options:
    --dry-run               Show what would be done without making changes
    --skip-backup           Skip creating backup of existing files
    -h, --help              Show this help message

Examples:
    $0 /path/to/my-project
    $0 . --dry-run
    $0 ~/projects/todo-app --skip-backup

This script will:
    1. Detect project framework and structure
    2. Add ADW core modules
    3. Install Python dependencies
    4. Configure environment files
    5. Add MCP configuration
    6. Update .gitignore

EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --skip-backup)
                SKIP_BACKUP=true
                shift
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            -*)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
            *)
                TARGET_PROJECT="$1"
                shift
                ;;
        esac
    done

    # Validate required argument
    if [[ -z "$TARGET_PROJECT" ]]; then
        print_error "Project path is required"
        show_usage
        exit 1
    fi

    # Resolve to absolute path
    TARGET_PROJECT="$(cd "$TARGET_PROJECT" && pwd)"
}

# Detect project framework
detect_framework() {
    print_info "Detecting project framework..."

    local framework="unknown"

    if [[ -f "$TARGET_PROJECT/package.json" ]]; then
        if grep -q "\"next\":" "$TARGET_PROJECT/package.json"; then
            framework="nextjs"
        elif grep -q "\"vite\":" "$TARGET_PROJECT/package.json"; then
            if grep -q "\"react\":" "$TARGET_PROJECT/package.json"; then
                framework="react-vite"
            else
                framework="vite"
            fi
        elif grep -q "\"react\":" "$TARGET_PROJECT/package.json"; then
            framework="react"
        elif grep -q "\"vue\":" "$TARGET_PROJECT/package.json"; then
            framework="vue"
        else
            framework="javascript"
        fi
    elif [[ -f "$TARGET_PROJECT/pyproject.toml" ]]; then
        framework="python"
    elif [[ -f "$TARGET_PROJECT/index.html" ]]; then
        framework="vanilla"
    fi

    print_info "Detected framework: $framework"
    echo "$framework"
}

# Create backup
create_backup() {
    if [[ "$SKIP_BACKUP" == true ]]; then
        print_warn "Skipping backup as requested"
        return
    fi

    local backup_dir="$TARGET_PROJECT/.adw-backup-$(date +%Y%m%d_%H%M%S)"

    print_info "Creating backup at: $backup_dir"

    mkdir -p "$backup_dir"

    # Backup files that might be modified
    local files_to_backup=(
        ".gitignore"
        ".env"
        "package.json"
        "pyproject.toml"
    )

    for file in "${files_to_backup[@]}"; do
        if [[ -f "$TARGET_PROJECT/$file" ]]; then
            cp "$TARGET_PROJECT/$file" "$backup_dir/"
        fi
    done
}

# Add core modules
add_core_modules() {
    print_info "Adding ADW core modules..."

    if [[ "$DRY_RUN" == true ]]; then
        print_info "[DRY RUN] Would copy core modules to $TARGET_PROJECT/adw_core/"
        return
    fi

    local core_dir="$TARGET_PROJECT/adw_core"
    mkdir -p "$core_dir"

    # Copy core modules
    local modules=(
        "file_processor.py"
        "llm_processor.py"
        "nl_processor.py"
        "sql_processor.py"
        "github_poster.py"
        "issue_formatter.py"
        "project_detector.py"
    )

    for module in "${modules[@]}"; do
        if [[ -f "$PROJECT_ROOT/app/server/core/$module" ]]; then
            cp "$PROJECT_ROOT/app/server/core/$module" "$core_dir/"
        fi
    done

    # Create __init__.py
    touch "$core_dir/__init__.py"
}

# Install Python dependencies
install_python_deps() {
    print_info "Installing Python dependencies..."

    if [[ "$DRY_RUN" == true ]]; then
        print_info "[DRY RUN] Would install: fastapi uvicorn python-dotenv anthropic openai"
        return
    fi

    cd "$TARGET_PROJECT"

    if command -v uv &> /dev/null; then
        print_info "Using uv..."
        uv add fastapi uvicorn python-dotenv anthropic openai
    elif command -v pip &> /dev/null; then
        print_info "Using pip..."
        pip install fastapi uvicorn python-dotenv anthropic openai
    else
        print_warn "No Python package manager found"
        print_warn "Please install manually: fastapi uvicorn python-dotenv anthropic openai"
    fi

    cd - > /dev/null
}

# Configure environment
configure_environment() {
    print_info "Configuring environment..."

    local env_sample="$TARGET_PROJECT/.env.sample"
    local env_file="$TARGET_PROJECT/.env"

    if [[ "$DRY_RUN" == true ]]; then
        print_info "[DRY RUN] Would create .env.sample with API key placeholders"
        return
    fi

    # Create .env.sample
    cat > "$env_sample" << 'EOF'
# LLM API Keys (at least one required)
OPENAI_API_KEY=sk-your_openai_key_here
ANTHROPIC_API_KEY=sk-ant-your_anthropic_key_here

# GitHub Configuration (optional)
GITHUB_TOKEN=ghp_your_github_token_here
GITHUB_REPO=owner/repository

# Server Configuration
SERVER_HOST=127.0.0.1
SERVER_PORT=8000
EOF

    if [[ ! -f "$env_file" ]]; then
        cp "$env_sample" "$env_file"
        print_info "Created .env file - please update with your API keys"
    else
        print_warn ".env already exists - check .env.sample for required variables"
    fi
}

# Add MCP configuration
add_mcp_config() {
    print_info "Adding MCP configuration..."

    if [[ "$DRY_RUN" == true ]]; then
        print_info "[DRY RUN] Would create .mcp.json.sample and playwright-mcp-config.json"
        return
    fi

    # Copy MCP config files
    if [[ -f "$PROJECT_ROOT/.mcp.json.sample" ]]; then
        cp "$PROJECT_ROOT/.mcp.json.sample" "$TARGET_PROJECT/"
    fi

    if [[ -f "$PROJECT_ROOT/playwright-mcp-config.json" ]]; then
        cp "$PROJECT_ROOT/playwright-mcp-config.json" "$TARGET_PROJECT/"
    fi

    print_info "Created MCP configuration files"
    print_info "Copy .mcp.json.sample to .mcp.json to activate"
}

# Update .gitignore
update_gitignore() {
    print_info "Updating .gitignore..."

    local gitignore="$TARGET_PROJECT/.gitignore"

    if [[ "$DRY_RUN" == true ]]; then
        print_info "[DRY RUN] Would add ADW patterns to .gitignore"
        return
    fi

    # Create .gitignore if it doesn't exist
    if [[ ! -f "$gitignore" ]]; then
        touch "$gitignore"
    fi

    # Add ADW patterns if not already present
    local patterns=(
        ".env"
        "*.db"
        "*.sqlite"
        ".mcp.json"
        "videos/"
        "adw_core/__pycache__/"
        ".adw-backup-*/"
    )

    for pattern in "${patterns[@]}"; do
        if ! grep -q "^$pattern$" "$gitignore"; then
            echo "$pattern" >> "$gitignore"
        fi
    done

    print_info "Updated .gitignore with ADW patterns"
}

# Create example server file
create_example_server() {
    print_info "Creating example server file..."

    local server_file="$TARGET_PROJECT/adw_server.py"

    if [[ "$DRY_RUN" == true ]]; then
        print_info "[DRY RUN] Would create adw_server.py"
        return
    fi

    if [[ -f "$server_file" ]]; then
        print_warn "adw_server.py already exists, skipping"
        return
    fi

    cat > "$server_file" << 'EOF'
"""
ADW Server - Example integration
Run with: uvicorn adw_server:app --reload
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from adw_core.nl_processor import NLProcessor
from adw_core.file_processor import FileProcessor

app = FastAPI(title="ADW Integration")

class NLRequest(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"message": "ADW Server Running"}

@app.post("/api/process")
async def process_nl(request: NLRequest):
    """Process natural language request"""
    try:
        processor = NLProcessor()
        result = await processor.process_request(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
EOF

    print_info "Created adw_server.py example"
}

# Print success message
print_success() {
    echo ""
    echo -e "${GREEN}✓ Integration complete!${NC}"
    echo ""
    echo "What was added:"
    echo "  - ADW core modules in adw_core/"
    echo "  - Environment configuration (.env.sample)"
    echo "  - MCP configuration files"
    echo "  - Example server (adw_server.py)"
    echo "  - Updated .gitignore"
    echo ""
    echo "Next steps:"
    echo "  1. Configure API keys in .env"
    echo "  2. Install dependencies (if not done automatically)"
    echo "  3. Test the integration:"
    echo "     uvicorn adw_server:app --reload"
    echo "  4. Visit http://localhost:8000/docs"
    echo ""
    echo "For more information, see:"
    echo "  $TEMPLATES_DIR/integration_guide.md"
    echo ""
}

# Main execution
main() {
    # Parse arguments
    parse_args "$@"

    # Validate project directory exists
    if [[ ! -d "$TARGET_PROJECT" ]]; then
        print_error "Project directory not found: $TARGET_PROJECT"
        exit 1
    fi

    print_info "Integrating ADW into: $TARGET_PROJECT"

    if [[ "$DRY_RUN" == true ]]; then
        print_warn "DRY RUN MODE - No changes will be made"
    fi

    # Detect framework
    FRAMEWORK=$(detect_framework)

    # Create backup
    if [[ "$DRY_RUN" == false ]]; then
        create_backup
    fi

    # Perform integration steps
    add_core_modules
    install_python_deps
    configure_environment
    add_mcp_config
    update_gitignore
    create_example_server

    # Print success
    if [[ "$DRY_RUN" == false ]]; then
        print_success
    else
        echo ""
        print_info "DRY RUN complete - run without --dry-run to apply changes"
    fi
}

main "$@"
