#!/bin/bash

# Stop all FAQ Bot applications

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Stopping FAQ Bot - All Applications"
echo "===================================="

# Check if PID file exists
if [ ! -f "$PROJECT_ROOT/pids.txt" ]; then
    echo "⚠️  No PID file found. Trying to find processes manually..."

    # Find and kill Python processes running the apps
    pkill -f "run_app.py" && echo "✅ Stopped Gradio app"
    pkill -f "run_streamlit.py" && echo "✅ Stopped Streamlit app"
    pkill -f "run_config.py" && echo "✅ Stopped Config app"

    echo ""
    echo "Done!"
    exit 0
fi

# Read PIDs from file
read GRADIO_PID STREAMLIT_PID CONFIG_PID < "$PROJECT_ROOT/pids.txt"

# Kill each process
echo "Stopping processes..."

if [ -n "$GRADIO_PID" ]; then
    kill $GRADIO_PID 2>/dev/null && echo "✅ Stopped Gradio app (PID: $GRADIO_PID)" || echo "⚠️  Gradio app already stopped"
fi

if [ -n "$STREAMLIT_PID" ]; then
    kill $STREAMLIT_PID 2>/dev/null && echo "✅ Stopped Streamlit app (PID: $STREAMLIT_PID)" || echo "⚠️  Streamlit app already stopped"
fi

if [ -n "$CONFIG_PID" ]; then
    kill $CONFIG_PID 2>/dev/null && echo "✅ Stopped Config app (PID: $CONFIG_PID)" || echo "⚠️  Config app already stopped"
fi

# Remove PID file
rm "$PROJECT_ROOT/pids.txt"

echo ""
echo "All applications stopped!"
