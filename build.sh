# Create build.sh
cat > build.sh << 'EOL'
#!/bin/bash
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Creating necessary directories..."
mkdir -p uploads outputs

echo "Build complete!"
EOL

chmod +x build.sh