![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=opensourceinitiative&logoColor=white)

# 🧠 Text Analyzer System (Modular & Layered Design)
A modular Python-based text analysis system designed to extract structured insights from raw text using a layered pipeline architecture.

Built from scratch to strengthen understanding of core text processing, system design, and clean architecture principles.

---

## 🎯 About This Project

This project began as a simple text processing script and evolved into a structured, layered system through **continuous refactoring**.

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

```text
                   Input Text
                       ↓
                 Text Preparation
                       ↓
+---------------------------------------------------+
|                 Analysis Layers                   |
| [Word]  [Char]  [Lex]  [Freq]  [Sentence]  [Para] |
+---------------------------------------------------+
                       ↓
                  Output Report
```

**Key Design Principles:**
- Strong **Separation of Concerns**
- Avoiding redundant computations through shared data
- Single Responsibility Principle
- Config-driven behavior (stopwords, abbreviations, etc.)

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
```

## 🛠️ How to Run

Clone the repository:
```bash
git clone https://github.com/manaalroshan/Text-Analyzer-System.git
cd Text-Analyzer-System
```

Run the analyzer:
```bash
python main.py
```

Enter your text and press Enter.

---

## 🧠 What I Learned

- Difference between writing code vs structuring systems
- Importance of data flow and avoiding redundant computations
- Iterative refactoring and modular design
- How to separate logic, configuration, and presentation layers
- Practical use of Git & GitHub (version control, commits, and safe refactoring)
- Building intuition for system design through real development

---

## 🔄 Development Journey
This project was developed using an evolutionary approach:

**Build → Identify Problems → Refactor → Modularize → Stabilize**

Instead of over-planning upfront, I focused on making steady improvements. This helped me develop better problem-solving instincts and real-world coding habits.

---

## 📌 Current Limitations
- Sentence detection is heuristic-based (not full NLP)
- Command-line interface only
- No file input/output support yet

---

## 🚀 Future Improvements
- Full OOP Refactoring (currently learning)
- File Handling support (.txt input & report export)
- Export reports as JSON / PDF
- Simple GUI using Tkinter or Streamlit
- Integration with Pandas for advanced analysis

---

## ⚔️ Project Philosophy
This project intentionally avoids heavy external libraries at this stage.
My goal is to build strong fundamentals first before relying on powerful tools and frameworks.

---

## 📌 Example Output
Sample 1: "Hello world! This is a test. Hello again."
### Output:
```
Text Analysis Report
--------------------------------------------------
Word Based Stats:
Total Words: 8
Unique Words: 7
Longest Word: hello, 5 letters long.
--------------------------------------------------
Character Stats:
Total Characters (without spaces): 34
Total Characters (with spaces): 41
--------------------------------------------------
Sentence Based Stats:
Total Sentences: 3
Longest Sentence (Words): 4
Shortest Sentence (Words): 2
Avg. Sentence Words: 2
Avg. Sentence Chars: 13
--------------------------------------------------
Paragraph Stats:
Total Paragraphs: 1
Average sentences (per Para.): 3.0
--------------------------------------------------
Lexical Stats:
Estimated Reading Time: 1.9 Seconds.
Estimated Speaking Time: 3.3 Seconds.
Vocabulary Richness: Insufficient data for richness score
--------------------------------------------------
Frequency Based Stats:
Most Frequent word: hello, 2 Times.
Top 5 Frequent Words
1. hello          → 2 times
2. world          → 1 times
3. this           → 1 times
4. is             → 1 times
5. a              → 1 times
Top 5 keywords (Stopwords Excluded)
1. hello          → 2 times
2. world          → 1 times
3. test           → 1 times
--------------------------------------------------
Created By Manaal Roshan
```
