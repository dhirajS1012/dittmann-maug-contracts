#!/bin/bash
# setup-dropbox-env.sh
# This script sets up the DM_DROPBOX_ROOT environment variable for the project

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Dittmann-Maug Dropbox Setup ===${NC}\n"

# Detect shell
if [[ $SHELL == *"zsh"* ]]; then
    SHELL_CONFIG="$HOME/.zshrc"
    SHELL_NAME="zsh"
elif [[ $SHELL == *"bash"* ]]; then
    SHELL_CONFIG="$HOME/.bashrc"
    SHELL_NAME="bash"
else
    echo -e "${YELLOW}Warning: Could not detect shell. Using ~/.zshrc${NC}"
    SHELL_CONFIG="$HOME/.zshrc"
    SHELL_NAME="zsh"
fi

echo -e "${BLUE}Detected shell: $SHELL_NAME ($SHELL_CONFIG)${NC}\n"

# Ask user for Dropbox path
echo -e "${YELLOW}Enter your Dropbox path to ExecuComp data:${NC}"
echo "Examples:"
echo "  $HOME/Dropbox/Research/ExecuComp"
echo "  $HOME/Dropbox/dittmann-maug-data"
echo ""
read -p "Enter path (or press Enter for default): " DROPBOX_PATH

# Use default if empty
if [ -z "$DROPBOX_PATH" ]; then
    DROPBOX_PATH="$HOME/Dropbox/dittmann-maug-execucomp"
    echo -e "${YELLOW}Using default: $DROPBOX_PATH${NC}"
fi

# Expand ~ if needed
DROPBOX_PATH="${DROPBOX_PATH/#\~/$HOME}"

# Check if path exists
if [ ! -d "$DROPBOX_PATH" ]; then
    echo -e "${YELLOW}Warning: Path does not exist yet: $DROPBOX_PATH${NC}"
    echo -e "${YELLOW}Make sure to create it and add parquet files:${NC}"
    echo "  $DROPBOX_PATH/execucomp/anncomp.parquet"
    echo "  $DROPBOX_PATH/execucomp/codirfin.parquet"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 1
    fi
fi

# Check if already configured
if grep -q "DM_DROPBOX_ROOT" "$SHELL_CONFIG"; then
    echo -e "${YELLOW}DM_DROPBOX_ROOT already configured in $SHELL_CONFIG${NC}"
    read -p "Replace existing configuration? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 1
    fi
    # Remove old line
    sed -i '' '/export DM_DROPBOX_ROOT=/d' "$SHELL_CONFIG"
fi

# Add to shell config
echo "export DM_DROPBOX_ROOT=\"$DROPBOX_PATH\"" >> "$SHELL_CONFIG"

echo -e "${GREEN}✓ Added to $SHELL_CONFIG:${NC}"
echo "  export DM_DROPBOX_ROOT=\"$DROPBOX_PATH\""
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. Reload your shell:"
echo "   source $SHELL_CONFIG"
echo ""
echo "2. Verify setup:"
echo "   echo \$DM_DROPBOX_ROOT"
echo ""
echo "3. Test the CLI:"
echo "   cd /Users/dhirajs/Desktop/project/Dev-dittmann-maug-contracts/dittmann-maug-contracts"
echo "   uv run python -m dittmann_maug.cli check-data"
echo ""
echo -e "${GREEN}Setup complete!${NC}"
