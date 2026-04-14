.PHONY: smoke regression all clean site

REPORT_DIR = reports

all:
	behave

smoke:
	behave -t smoke

regression:
	behave -t regression

site:
	behave -D site=$(SITE)
	# Usage: 'make site SITE=services'

report:
	# mkdir -p $(REPORT_DIR)
	# behave -f plain -o $(REPORT_DIR)/report.txt
	behave -f plain -o report.txt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
