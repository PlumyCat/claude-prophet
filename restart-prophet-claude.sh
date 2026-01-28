#!/bin/bash
# Restart Prophet Claude with proper context
# Usage: ./restart-prophet-claude.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Prophet Claude Bootstrap ==="
echo ""

# Generate settings.json from context-cli
echo "Generating settings.json for prophet-claude role..."
cd context-cli
uv run python main.py settings prophet-claude -o ../settings.json
cd ..
echo "  ✓ settings.json created"

# Kill existing prophet-claude session if any
if tmux has-session -t prophet-claude 2>/dev/null; then
    echo "Killing existing prophet-claude session..."
    tmux kill-session -t prophet-claude
    echo "  ✓ Old session terminated"
fi

# Start new session with claude (skip permissions for autonomy)
echo "Starting Prophet Claude..."
tmux new-session -d -s prophet-claude "claude --dangerously-skip-permissions"

# Wait for Claude to start
sleep 2

# Send initial context
INIT_PROMPT="You are now Prophet Claude. Your context has been loaded from context-cli.

Available commands:
- ./claude spawn --name <name> \"task\" - Spawn a worker
- ./claude spawn --role worker \"task\" - Spawn with role context
- ./claude capture <session> - See worker output
- ./claude list - List active workers
- ./claude kill <session> - Kill a worker

Ready to receive tasks. What would you like me to help with?"

tmux send-keys -t prophet-claude "$INIT_PROMPT" Enter

echo ""
echo "=== Prophet Claude Started ==="
echo ""
echo "Attach with:"
echo "  tmux attach -t prophet-claude"
echo ""
echo "Or run commands directly:"
echo "  ./claude list"
echo "  ./claude spawn --role worker \"your task\""
