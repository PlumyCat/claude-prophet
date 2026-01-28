#!/bin/bash
# Install MCBS skills to global Claude Code skills directory
# Usage: ./install-skills.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_SRC="$SCRIPT_DIR/skills/mcbs"
SKILLS_DST="$HOME/.claude/skills/mcbs"

echo "=== MCBS Skills Installation ==="
echo ""

# Check source exists
if [ ! -d "$SKILLS_SRC" ]; then
    echo "Error: Skills source not found: $SKILLS_SRC"
    exit 1
fi

# Create destination if needed
mkdir -p "$SKILLS_DST"

# Copy skills
echo "Installing skills to $SKILLS_DST..."
cp -r "$SKILLS_SRC"/* "$SKILLS_DST/"

echo ""
echo "=== Installed Skills ==="
ls -1 "$SKILLS_DST" | while read skill; do
    echo "  /mcbs:$skill"
done

echo ""
echo "Done! Skills are now available globally."
echo ""
echo "Usage examples:"
echo "  /mcbs:status   - System status"
echo "  /mcbs:spawn    - Spawn a worker"
echo "  /mcbs:workers  - List workers"
