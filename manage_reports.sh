#!/bin/bash
# Report management helper script

REPORTS_DIR="reports"

case "$1" in
    open)
        echo "Opening test report..."
        open "$REPORTS_DIR/report.html"
        ;;
    clean)
        echo "Cleaning reports..."
        rm -rf "$REPORTS_DIR"
        echo "Reports cleaned."
        ;;
    generate)
        echo "Generating test reports..."
        python -m pytest tests/ -v --html="$REPORTS_DIR/report.html" --self-contained-html
        echo "Reports generated at: $REPORTS_DIR/report.html"
        ;;
    *)
        echo "Report Management Helper"
        echo ""
        echo "Usage: $0 {open|clean|generate}"
        echo ""
        echo "Commands:"
        echo "  open     - Open the HTML report in the default browser"
        echo "  clean    - Remove all generated reports"
        echo "  generate - Run tests and generate fresh reports"
        ;;
esac

