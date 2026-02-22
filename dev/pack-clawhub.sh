#!/bin/bash

# Script to package only specified files into ./clawhub-skill folder

# Define the destination folder
DEST_FOLDER="./clawhub-skill"

# Remove destination folder if it exists to start fresh
if [ -d "$DEST_FOLDER" ]; then
    rm -rf "$DEST_FOLDER"
    echo "Removed existing destination folder: $DEST_FOLDER"
fi

# Create fresh destination folder
mkdir -p "$DEST_FOLDER"
echo "Created fresh destination folder: $DEST_FOLDER"

# Define include patterns
INCLUDE_PATTERNS=(
    "SKILL.md"
)

# Build rsync command with include list restriction
echo "Copying files with rsync..."
RSYNC_COMMAND="rsync -av --delete"

# First include all parent directories to ensure traversal
for pattern in "${INCLUDE_PATTERNS[@]}"; do
    # Get directory part of the pattern
    dir=$(dirname "$pattern")
    if [ "$dir" != "." ]; then
        # Include all parent directories
        RSYNC_COMMAND="$RSYNC_COMMAND --include=\"$dir/\""
    fi
    # Include the file itself
    RSYNC_COMMAND="$RSYNC_COMMAND --include=\"$pattern\""
done

# Exclude everything else
RSYNC_COMMAND="$RSYNC_COMMAND --exclude=\"*\""

# Execute the rsync command
eval $RSYNC_COMMAND ./ "$DEST_FOLDER/"

# Check if the copy was successful
echo "=== Final Result ==="
if [ $? -eq 0 ]; then
    echo "✅ Successfully packaged the project into $DEST_FOLDER"
    echo "Included files: ${INCLUDE_PATTERNS[*]}"
    echo "Contents of $DEST_FOLDER:"
    ls -la "$DEST_FOLDER"
else
    echo "❌ Error packaging the project"
    exit 1
fi
