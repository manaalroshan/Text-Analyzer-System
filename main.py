from text_analyzer import AnalyzerApp
from ui import TextAnalysisReport
from report_generator import ReportGenerator, ReportExporter
from config import input_path, json_output_path, output_path
import sys
from pathlib import Path

# Initialize the main application logic for text analysis.
app = AnalyzerApp()

# Create or check if there is a folder to load inputs.
Path("inputs").mkdir(exist_ok=True)

# Attempt to load text from the configured input file path.
try:
    user_input = input_path.read_text(encoding="utf-8")

except FileNotFoundError:
    # Fallback to manual console input if the file is missing.
    print("Error: 'raw_text.txt' was not found inside the inputs folder.")
    user_input = input("Please Enter text manually: ")

except Exception as e:
    # Catch-all for unexpected I/O or system errors.
    print(f"Unexpected Error: {e}")
    sys.exit(1)

# Check if the user input is empty or contains only whitespace.
if not user_input.strip():
    print("Invalid Input: Enter Some Words for Analysis Stats.")
else:
    # Perform the multi-layered text analysis.
    results = app.analyze(user_input)

    # If analysis returns None, it means no valid words were found.
    if results is None:
        print("Invalid Input: No Valid Words Found to Analyze. Please try to enter atleast a letter or number.")
    else:
        # 1. Console Output: Display the report immediately to the user.
        visualizer = TextAnalysisReport(divider_char="-", divider_length=50)
        visualizer.display_report(results)

        # 2. Report Construction: Build a formatted string for file export.
        generator = ReportGenerator()
        report = generator.build_report(results)

        # 3. Persistence: Export the raw analysis data (JSON) and the formatted report (TXT).
        exporter = ReportExporter()
        exporter.save_json(results, json_output_path)
        exporter.save_report(report, output_path)