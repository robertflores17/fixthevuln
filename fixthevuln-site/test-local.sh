#!/bin/bash

echo "🚀 FixTheVuln - Quick Test Script"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "🔍 Fetching latest security news..."
echo ""

# Run the news fetcher
python3 fetch_news.py

echo ""
echo "✅ Done! Check the 'posts/' directory for generated blog posts."
echo ""
echo "Next steps:"
echo "1. Review the generated posts in posts/"
echo "2. Upload this folder to GitHub"
echo "3. Deploy to Netlify"
echo "4. Your site will auto-update daily!"
