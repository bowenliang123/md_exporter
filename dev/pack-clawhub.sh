#!/bin/bash

# Script to package the current directory into ./clawhub-skill folder
# while ignoring certain files and folders

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

# Collect all exclude patterns
ALL_PATTERNS=()

# Add patterns from .gitignore if it exists
if [ -f ".gitignore" ]; then
    echo "Adding patterns from .gitignore..."
    while IFS= read -r line || [ -n "$line" ]; do
        # Skip empty lines and comments
        [[ $line =~ ^\s*$ ]] && continue
        [[ $line =~ ^\s*# ]] && continue
        
        # Remove trailing spaces
        line=$(echo "$line" | sed 's/[[:space:]]*$//')
        
        # Skip if line is empty after processing
        [[ -z "$line" ]] && continue
        
        # Add to patterns
        ALL_PATTERNS+=($line)
    done < ".gitignore"
fi

# Add additional patterns
ADDITIONAL_PATTERNS=(
    ".difyignore"
    ".ruff.toml"
    "*.docx"
    "*.pdf"
    "*.png"
    "*.pptx"
    "*.xlsx"
    "_assets"
    "assets"
    "dev"
    "MANIFEST.in"
    "main.py"
    "manifest.yaml"
    "md-exporter"
    "PRIVACY.md"
    "provider"
    "README.md"
    "test"
    "tools"
    "uv.lock"
)
ALL_PATTERNS+=(${ADDITIONAL_PATTERNS[@]})

# Remove duplicates
UNIQUE_PATTERNS=$(printf "%s\n" "${ALL_PATTERNS[@]}" | awk '!seen[$0]++')

# Build rsync command with all exclude patterns
echo "Copying files with rsync..."
RSYNC_COMMAND="rsync -av --delete"

# Add each unique pattern as an exclude option
while IFS= read -r pattern; do
    RSYNC_COMMAND="$RSYNC_COMMAND --exclude=\"$pattern\""
done <<< "$UNIQUE_PATTERNS"

# Add special patterns that need explicit exclusion
RSYNC_COMMAND="$RSYNC_COMMAND --exclude=.git --exclude=.gitignore --exclude=.env.example --exclude=clawhub-skill"

# Execute the rsync command
eval $RSYNC_COMMAND ./ "$DEST_FOLDER/"

# Make the script executable
chmod +x "$DEST_FOLDER/dev/pack-clawhub.sh" 2>/dev/null

# Simplified verification
echo "\n=== Verification Results ==="

# Check representative excluded items
EXCLUDED_ITEMS=(".env.example" ".DS_Store" ".idea" ".venv" "__pycache__" ".pytest_cache")
ALL_PASSED=true

for item in "${EXCLUDED_ITEMS[@]}"; do
    if [ -e "$DEST_FOLDER/$item" ]; then
        echo "❌ ERROR: $item was not excluded!"
        ALL_PASSED=false
    else
        echo "✅ SUCCESS: $item was excluded"
    fi
done

# Check for any .iml files
IML_FILES=$(find "$DEST_FOLDER" -name "*.iml" 2>/dev/null)
if [ -n "$IML_FILES" ]; then
    echo "❌ ERROR: .iml files were not excluded!"
    ALL_PASSED=false
else
    echo "✅ SUCCESS: .iml files were excluded"
fi

# Check for any Python cache files
PYC_FILES=$(find "$DEST_FOLDER" -name "*.pyc" 2>/dev/null)
if [ -n "$PYC_FILES" ]; then
    echo "❌ ERROR: .pyc files were not excluded!"
    ALL_PASSED=false
else
    echo "✅ SUCCESS: .pyc files were excluded"
fi

# Check if the copy was successful
echo "\n=== Final Result ==="
if [ $? -eq 0 ] && $ALL_PASSED; then
    echo "✅ Successfully packaged the project into $DEST_FOLDER"
    echo "\nExcluded patterns were consolidated from .gitignore and additional patterns."
else
    echo "❌ Error packaging the project"
    exit 1
fi
