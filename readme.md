![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 About This Project

This project began as a simple text processing script and gradually evolved into a structured, layered system through **continuous refactoring**.

Rather than designing a perfect architecture from the start, I let the system emerge organically:
- Started with basic functionality
- Identified inefficiencies (like repeated computations)
- Improved data flow
- Separated concerns
- Modularized the codebase step by step

This project reflects my belief that **real systems are refined through iteration**, not created perfectly in one go. It served as a bridge between learning basic Python and moving toward more professional software development practices.

---

## ✨ Features

### 📊 Core Analysis
- Word count, unique words, and longest word detection
- Character statistics (with and without spaces)
- Sentence analysis (count, length, averages)
- Paragraph analysis

### 📈 Advanced Insights
- Estimated Reading Time & Speaking Time
- Vocabulary Richness Score (Type-Token Ratio)
- Most frequent words
- Top keywords (excluding stopwords)

---

## 🏗️ Architecture & Design Philosophy

The system follows a **layered pipeline architecture**:
Input Text
↓
Text Preparation
↓
[Word Layer] → [Character Layer] → [Sentence Layer] → [Paragraph Layer]
↓
Frequency Layer + Lexical Layer
↓
Merged Results
↓
Presentation Layer (CLI)
text**Key Design Principles:**
- Strong **Separation of Concerns** (Logic, Configuration, and UI are isolated)
- Single Responsibility Principle
- Avoiding recomputation through shared data
- Config-driven behavior (stopwords, abbreviations, etc.)
- Clean, readable, and maintainable code

---

## 📂 Project Structure

```bash
Text-Analyzer-System/
├── main.py              # Entry point
├── text_analyzer.py     # Core analysis logic (layered pipeline)
├── ui.py                # Presentation & formatting layer
├── config.py            # Constants, stopwords, abbreviations
├── .gitignore
├── LICENSE
└── README.md

🛠️ How to Run
Clone the repository:Bashgit clone https://github.com/manaalroshan/Text-Analyzer-System.git
cd Text-Analyzer-System
Run the analyzer:Bashpython main.py

Enter your text and press Enter twice (blank line) to finish input.

🧠 What I Learned
Difference between writing code vs structuring systems
Importance of data flow and avoiding redundant computations
Iterative refactoring and modular design
How to separate logic, configuration, and presentation layers
Practical use of Git & GitHub (version control, commits, and safe refactoring)
Building intuition for system design through real development


🔄 Development Journey
This project was developed using an evolutionary approach:
Build → Identify Problems → Refactor → Modularize → Stabilize
Instead of over-planning upfront, I focused on making steady improvements. This helped me develop better problem-solving instincts and real-world coding habits.

📌 Current Limitations
Sentence detection is heuristic-based (not full NLP)
Command-line interface only
No file input/output support yet


🚀 Future Improvements
Full OOP Refactoring (currently learning)
File Handling support (.txt input & report export)
Export reports as JSON / PDF
Simple GUI using Tkinter or Streamlit
Integration with Pandas for advanced analysis


⚔️ Project Philosophy
This project intentionally avoids heavy external libraries at this stage.
My goal is to build strong fundamentals first before relying on powerful tools and frameworks.