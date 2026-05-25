from text_analyzer import AnalyzerApp
from ui import TextAnalysisReport
from report_generator import TextAnalysisExport
from config import vocab_statements, input_path
import os
import sys

# Initialize the main application logic for text analysis.
app = AnalyzerApp()

# Create or check if there is a folder to load inputs.
os.makedirs("inputs", exist_ok=True)

# Getting output from a file
try:
    with open(input_path, "r", encoding="utf-8") as file:
        user_input = file.read()
        
except FileNotFoundError:
    print("Error: 'raw_text.txt' was not found inside the inputs folder.")
    user_input = input("Please Enter text manually: ")

except Exception as e:
    print(f"Unexpected Error: {e}")
    sys.exit(1)
    
# Check if the user input is empty or contains only whitespace.
if not user_input.strip():
    print("Invalid Input: Enter Some Words for Analysis Stats.")
else:
    # Perform the text analysis.
    results = app.analyze(user_input)
    
    # If analysis returns None, it means no valid words were found.
    if results is None:
        print("Invalid Input: No Valid Words Found to Analyze. Please try to enter atleast a letter or number.")
    else:
        # Initialize the report visualizer and display the results.
        visualizer = TextAnalysisReport(divider_char="-", divider_length=50)
        visualizer.display_report(results, vocab_statements)
        exporter = TextAnalysisExport()
        exporter.export_report(results, vocab_statements)