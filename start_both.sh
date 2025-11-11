#!/bin/bash
# Helper script to start both chat and config applications

echo "=========================================="
echo "FAQ Bot - Starting Applications"
echo "=========================================="
echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not activated!"
    echo "   Run: source venv/bin/activate"
    exit 1
fi

# Check for .env file
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "   Create .env with: OPENAI_API_KEY=your-key"
    exit 1
fi

echo "Starting applications..."
echo ""

# Start chat application
echo "📱 Starting Chat Application (port 8080)..."
python app.py > logs/chat.log 2>&1 &
CHAT_PID=$!
echo "   PID: $CHAT_PID"

# Wait a bit
sleep 2

# Start config application
echo "⚙️  Starting Config Application (port 8081)..."
python config_app.py > logs/config.log 2>&1 &
CONFIG_PID=$!
echo "   PID: $CONFIG_PID"

echo ""
echo "=========================================="
echo "✅ Both applications started!"
echo "=========================================="
echo ""
echo "📱 Chat (Users):   http://localhost:8080"
echo "⚙️  Config (Admin): http://localhost:8081"
echo ""
echo "Process IDs:"
echo "  Chat:   $CHAT_PID"
echo "  Config: $CONFIG_PID"
echo ""
echo "To stop both applications:"
echo "  kill $CHAT_PID $CONFIG_PID"
echo ""
echo "Or use: ./stop_both.sh"
echo ""
echo "Logs:"
echo "  Chat:   tail -f logs/chat.log"
echo "  Config: tail -f logs/config.log"
echo "=========================================="

# Create stop script
cat > stop_both.sh << EOF
#!/bin/bash
echo "Stopping applications..."
kill $CHAT_PID $CONFIG_PID 2>/dev/null
echo "Done!"
EOF
chmod +x stop_both.sh
