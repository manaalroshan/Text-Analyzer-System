from text_analyzer import AnalyzerApp
from ui import TextAnalysisReport
from config import vocab_statements

# Initialize the main application logic for text analysis.
app = AnalyzerApp()

# Prompt the user to enter text for analysis.
user_input = input("Enter Text: ")

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