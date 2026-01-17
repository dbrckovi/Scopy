#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Get user's home directory (full path)
HOME_DIR="$HOME"

echo "Installing Scopy..."
echo "Script directory: $SCRIPT_DIR"
echo "Home directory: $HOME_DIR"

# Copy run_scopy.sh.template to run_scopy.sh and replace {dir}
sed "s|{dir}|$SCRIPT_DIR|g" "$SCRIPT_DIR/run_scopy.sh.template" > "$SCRIPT_DIR/run_scopy.sh"
echo "Created run_scopy.sh"

# Make run_scopy.sh executable
chmod +x "$SCRIPT_DIR/run_scopy.sh"
echo "Made run_scopy.sh executable"

# Create autostart directory if it doesn't exist
mkdir -p "$HOME_DIR/.config/autostart"
echo "Created autostart directory"

# Copy start_scopy.desktop.template and replace {dir}
sed "s|{dir}|$SCRIPT_DIR|g" "$SCRIPT_DIR/start_scopy.desktop.template" > "$HOME_DIR/.config/autostart/start_scopy.desktop"
echo "Created start_scopy.desktop in autostart"

echo "Installation complete!"
echo "Scopy will start automatically on next boot."
echo "To run now: $SCRIPT_DIR/run_scopy.sh"
