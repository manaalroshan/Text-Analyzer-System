from text_analyzer import analyze_text
from ui import display_results

user_input = input("Enter Your Text: ")
if not user_input.strip():
    print("Please Enter Some Words for Analysis Stats.")
else:
    result = analyze_text(user_input)
    if result:
        display_results(result)
    else:
        print("No Valid Words Found to Analyze. Please try to enter atleast a letter or number.")