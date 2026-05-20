from oop_text_analyzer import AnalyzerApp
app = AnalyzerApp()
user_input = input("Enter Text: ")

if not user_input.strip():
    print("Invalid Input: Enter Some Words for Analysis Stats.")
else:
    results = app.analyze(user_input)
    
    if results is None:
        print("Invalid Input: No Valid Words Found to Analyze. Please try to enter atleast a letter or number.")
    else:
        for name, value in results.items():
            print(name, value)
    