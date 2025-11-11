#!/bin/bash

# TAC WebBuilder - New Project Setup Script
# Creates a new web application from templates

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TEMPLATES_DIR="$PROJECT_ROOT/templates/new_webapp"

# Default values
PROJECT_NAME=""
PROJECT_TYPE=""
TARGET_DIR="."
INIT_GIT=true
INSTALL_DEPS=true

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
TAC WebBuilder - New Project Setup

Usage: $0 [OPTIONS]

Options:
    -n, --name NAME         Project name (required)
    -t, --type TYPE         Template type: react-vite, nextjs, vanilla (required)
    -d, --dir DIRECTORY     Target directory (default: current directory)
    --no-git                Skip git initialization
    --no-install            Skip dependency installation
    -h, --help              Show this help message

Examples:
    $0 --name my-app --type react-vite
    $0 -n todo-app -t nextjs -d ~/projects
    $0 --name landing-page --type vanilla --no-git

Available Templates:
    react-vite    React + Vite with TypeScript
    nextjs        Next.js with App Router
    vanilla       Plain HTML/CSS/JavaScript

EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -n|--name)
                PROJECT_NAME="$2"
                shift 2
                ;;
            -t|--type)
                PROJECT_TYPE="$2"
                shift 2
                ;;
            -d|--dir)
                TARGET_DIR="$2"
                shift 2
                ;;
            --no-git)
                INIT_GIT=false
                shift
                ;;
            --no-install)
                INSTALL_DEPS=false
                shift
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done

    # Validate required arguments
    if [[ -z "$PROJECT_NAME" ]]; then
        print_error "Project name is required"
        show_usage
        exit 1
    fi

    if [[ -z "$PROJECT_TYPE" ]]; then
        print_error "Project type is required"
        show_usage
        exit 1
    fi

    # Validate project type
    if [[ ! "$PROJECT_TYPE" =~ ^(react-vite|nextjs|vanilla)$ ]]; then
        print_error "Invalid project type: $PROJECT_TYPE"
        print_info "Valid types: react-vite, nextjs, vanilla"
        exit 1
    fi
}

# Interactive mode if no arguments provided
interactive_mode() {
    print_info "Interactive Project Setup"
    echo ""

    # Get project name
    read -p "Project name: " PROJECT_NAME
    if [[ -z "$PROJECT_NAME" ]]; then
        print_error "Project name cannot be empty"
        exit 1
    fi

    # Get project type
    echo ""
    echo "Select template type:"
    echo "  1) react-vite  - React + Vite with TypeScript"
    echo "  2) nextjs      - Next.js with App Router"
    echo "  3) vanilla     - Plain HTML/CSS/JavaScript"
    read -p "Choice (1-3): " choice

    case $choice in
        1) PROJECT_TYPE="react-vite" ;;
        2) PROJECT_TYPE="nextjs" ;;
        3) PROJECT_TYPE="vanilla" ;;
        *)
            print_error "Invalid choice"
            exit 1
            ;;
    esac

    # Get target directory
    echo ""
    read -p "Target directory (default: current): " TARGET_DIR
    if [[ -z "$TARGET_DIR" ]]; then
        TARGET_DIR="."
    fi

    # Git initialization
    echo ""
    read -p "Initialize git repository? (Y/n): " git_choice
    if [[ "$git_choice" =~ ^[Nn]$ ]]; then
        INIT_GIT=false
    fi

    # Dependency installation
    echo ""
    read -p "Install dependencies? (Y/n): " deps_choice
    if [[ "$deps_choice" =~ ^[Nn]$ ]]; then
        INSTALL_DEPS=false
    fi
}

# Create project from template
create_project() {
    local template_path="$TEMPLATES_DIR/$PROJECT_TYPE"
    local project_path="$TARGET_DIR/$PROJECT_NAME"

    print_info "Creating project: $PROJECT_NAME"
    print_info "Template: $PROJECT_TYPE"
    print_info "Location: $project_path"

    # Check if template exists
    if [[ ! -d "$template_path" ]]; then
        print_error "Template not found: $template_path"
        exit 1
    fi

    # Check if project directory already exists
    if [[ -d "$project_path" ]]; then
        print_error "Directory already exists: $project_path"
        exit 1
    fi

    # Create project directory
    mkdir -p "$project_path"

    # Copy template files
    print_info "Copying template files..."
    cp -r "$template_path/"* "$project_path/"
    cp -r "$template_path/".* "$project_path/" 2>/dev/null || true

    # Update project name in files
    print_info "Configuring project..."

    # Update package.json if exists
    if [[ -f "$project_path/package.json" ]]; then
        if command -v jq &> /dev/null; then
            jq ".name = \"$PROJECT_NAME\"" "$project_path/package.json" > "$project_path/package.json.tmp"
            mv "$project_path/package.json.tmp" "$project_path/package.json"
        else
            # Fallback to sed if jq not available
            sed -i.bak "s/\"name\": \".*\"/\"name\": \"$PROJECT_NAME\"/" "$project_path/package.json"
            rm "$project_path/package.json.bak"
        fi
    fi

    # Initialize git if requested
    if [[ "$INIT_GIT" == true ]]; then
        print_info "Initializing git repository..."
        cd "$project_path"
        git init
        git add .
        git commit -m "Initial commit: $PROJECT_NAME"
        cd - > /dev/null
    fi

    # Install dependencies if requested
    if [[ "$INSTALL_DEPS" == true ]]; then
        install_dependencies "$project_path"
    fi

    print_success
}

# Install project dependencies
install_dependencies() {
    local project_path="$1"

    if [[ ! -f "$project_path/package.json" ]]; then
        print_warn "No package.json found, skipping dependency installation"
        return
    fi

    print_info "Installing dependencies..."

    cd "$project_path"

    # Detect package manager
    if command -v bun &> /dev/null; then
        print_info "Using bun..."
        bun install
    elif command -v npm &> /dev/null; then
        print_info "Using npm..."
        npm install
    else
        print_warn "No package manager found (npm, bun)"
        print_warn "Please install dependencies manually"
    fi

    cd - > /dev/null
}

# Print success message
print_success() {
    local project_path="$TARGET_DIR/$PROJECT_NAME"

    echo ""
    echo -e "${GREEN}✓ Project created successfully!${NC}"
    echo ""
    echo "Next steps:"
    echo "  cd $project_path"

    case $PROJECT_TYPE in
        react-vite|nextjs)
            echo "  npm run dev"
            ;;
        vanilla)
            echo "  # Open index.html in your browser"
            echo "  # Or run: python -m http.server 8000"
            ;;
    esac

    echo ""
    echo "Additional setup:"
    echo "  - Copy .mcp.json.sample to .mcp.json for MCP integration"
    echo "  - Configure .env if needed"
    echo "  - Review README.md for more information"
    echo ""
}

# Main execution
main() {
    # Parse arguments or run interactive mode
    if [[ $# -eq 0 ]]; then
        interactive_mode
    else
        parse_args "$@"
    fi

    # Create the project
    create_project
}

main "$@"
