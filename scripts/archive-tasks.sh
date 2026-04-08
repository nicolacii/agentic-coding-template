#!/bin/bash
# Archive completed tasks to quarterly archive folder
# Usage: ./scripts/archive-tasks.sh [quarter]
# Example: ./scripts/archive-tasks.sh 2026-Q1

set -e

QUARTER="${1:-$(date +%Y)-Q$((($(date +%-m)-1)/3+1))}"
ARCHIVE_DIR="tasks/archive/$QUARTER"

mkdir -p "$ARCHIVE_DIR"

echo "Archiving completed tasks to $ARCHIVE_DIR..."

# Find directories in tasks/ that have reflection.md (= completed)
# but skip already archived
for dir in tasks/*/; do
    name=$(basename "$dir")

    # Skip special dirs
    [[ "$name" == "archive" || "$name" == "checklists" ]] && continue

    # Skip if no reflection.md (not completed)
    [[ ! -f "$dir/reflection.md" ]] && continue

    echo "  → $name"
    mv "$dir" "$ARCHIVE_DIR/"
done

echo ""
echo "Done. Update BACKLOG.md to reflect archived tasks."
echo "Archived to: $ARCHIVE_DIR"
