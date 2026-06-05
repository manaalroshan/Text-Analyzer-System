![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge&logo=opensourceinitiative&logoColor=white)

# 🧠 Text Analyzer System
A modular Python-based text analysis system built using layered architecture and object-oriented design principles. The project analyzes raw text, extracts structured insights, and generates both human-readable reports and machine-readable JSON output through an extensible analysis pipeline.

---

## 🎯 About This Project

This project began as a simple text analysis script and gradually evolved into a structured software system through **continuous refactoring** and **architectural improvements**.

The system now follows a modular architecture built around reusable analyzers, a shared execution context, dedicated presentation and reporting layers, and a persistence layer for exporting analysis results.

More importantly, the project serves as an ongoing engineering playground where new concepts are applied through real implementation rather than isolated exercises.

---

## ✨ Features

### 📊 Core Analysis
* Total word count and unique word count
* Longest word detection
* Character statistics (with and without spaces)
* Sentence analysis and readability metrics
* Paragraph analysis

### 📈 Lexical Insights
* Vocabulary richness scoring (Type-Token Ratio)
* Vocabulary quality remarks
* Estimated reading time
* Estimated speaking time

### 🔍 Frequency Analysis
* Most frequent word detection
* Top 5 frequent words
* Top 5 keywords (excluding stopwords)

### 💾 Persistence & Export
* File-based text input
* Formatted report export (.txt)
* Structured JSON export
* UTF-8 encoding support

---

## 🏗️ Architecture

The system follows a layered pipeline architecture where text flows through multiple stages of processing, analysis, presentation, and persistence.
```
                 Input Text
                      │
                      ▼
             ┌─────────────────┐
             │ AnalysisContext │
             └─────────────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ AnalyzerEngine  │
             └─────────────────┘
                      │
                      ▼
┌───────────────────────────────────────────────┐
│               Analyzer Pipeline               │
├───────────────────────────────────────────────┤
│ Word │ Character │ Lexical │ Frequency │      │
│ Sentence │ Paragraph │                        │
└───────────────────────────────────────────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Analysis Results│
             └─────────────────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
 ┌─────────────────┐    ┌─────────────────┐
 │ Console Display │    │ Report Generator│
 └─────────────────┘    └─────────────────┘
                                  │
                                  ▼
                        ┌─────────────────┐
                        │ Report Exporter │
                        └─────────────────┘
                                  │
                     ┌────────────┴────────────┐
                     ▼                         ▼
                TXT Report               JSON Export
```

### Key Components
#### AnalysisContext

Acts as a shared execution context for the entire analysis pipeline. Preprocessed data such as cleaned words, sentence statistics, paragraph counts, and frequency maps are computed once and shared across analyzers to avoid redundant work.

#### AnalyzerEngine

Responsible for orchestrating the analysis pipeline. Each analyzer is executed sequentially and its results are stored within the shared context.

#### Modular Analyzers

Each analyzer focuses on a single responsibility:

- WordAnalyzer
- CharacterAnalyzer
- LexicalAnalyzer
- FrequencyAnalyzer
- SentenceAnalyzer
- ParagraphAnalyzer

This design keeps the system modular and makes it easy to add new analyzers in the future.

#### Report Layer

The reporting system is separated into two responsibilities:

- ReportGenerator → Creates formatted human-readable reports.

- ReportExporter → Handles persistence and export operations.

This separation improves maintainability and keeps formatting logic independent from file operations.

---

## 📂 Project Structure

```bash
Text-Analyzer-System/
│
├── main.py
│   └── Application entry point and orchestration
│
├── text_analyzer.py
│   └── Core analysis engine, analyzers, context, and pipeline logic
│
├── ui.py
│   └── Console presentation and report visualization
│
├── report_generator.py
│   ├── ReportGenerator (report construction)
│   └── ReportExporter (TXT & JSON export)
│
├── config.py
│   └── Application configuration, stopwords, abbreviations, and file paths
│
├── inputs/
│   └── raw_text.txt
│
├── results/
│   ├── text_analysis.txt
│   └── analysis.json
│
├── README.md
├── LICENSE
└── .gitignore
```

---

## 🔧 Technologies & Concepts Used

### Technologies

* Python 3
* JSON
* Pathlib
* Git & GitHub

### Core Concepts

* Object-Oriented Programming (OOP)
* Abstraction & Polymorphism
* Layered Architecture
* Separation of Concerns
* Modular Design
* Shared Execution Context
* Refactoring

### File Handling & Persistence

* Text File Processing
* JSON Serialization
* UTF-8 Encoding
* Filesystem Path Management

---

## 🛠️ How to Run

Clone the repository:
```bash
git clone https://github.com/manaalroshan/Text-Analyzer-System.git

cd Text-Analyzer-System
```

Add the text you want to analyze to:
```
inputs/raw_text.txt
```

Run the analyzer:
```bash
python main.py
```

If the input file is missing, the program will automatically prompt for manual text input.
Enter your text and press Enter.

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
Longest Word: 'hello' (5 letters long)
--------------------------------------------------
Character Stats:
Total Characters (with spaces): 41
Total Characters (without spaces): 34
--------------------------------------------------
Sentence Based Stats:
Total Sentences: 3
Longest Sentence: 4 Words
Shortest Sentence: 2 Words
Avg. Sentence Length: 2.7 Words
Avg. Sentence Characters: 13.7 Characters
--------------------------------------------------
Paragraph Stats:
Total Paragraphs: 1
Avg. Sentences per Paragraph: 3.0
--------------------------------------------------
Lexical Stats:
Estimated Reading Time: 1.9 Seconds
Estimated Speaking Time: 3.3 Seconds
Vocabulary Richness Score: 87.50% (Small text sample - interpret cautiously)
--------------------------------------------------
Frequency Based Stats:
Most Frequent Word: 'hello' (2 times)

Top 5 Frequent Words:
1. hello           →  2 times
2. world           →  1 times
3. this            →  1 times
4. is              →  1 times
5. a               →  1 times

Top 5 Keywords (Stop words Excluded):
1. hello           →  2 times
2. world           →  1 times
3. test            →  1 times
--------------------------------------------------
REPORT ENDED
```

---

## 🧠 What I Learned

Building this project taught me that writing working code and designing maintainable software are very different challenges.

Through multiple iterations and refactors, I gained practical experience with:

- Object-Oriented Programming (OOP)
- Layered software architecture
- Separation of concerns
- Shared execution contexts
- File handling and persistence
- JSON serialization and deserialization
- Pathlib-based filesystem management

More importantly, this project helped me develop a stronger understanding of how software evolves over time through incremental improvements rather than perfect upfront design.

---

## 🗺️ Roadmap

### ✅ Completed

* Modular OOP Architecture
* Shared Analysis Context
* Layered Analyzer Pipeline
* TXT Report Export
* JSON Export
* Pathlib Integration
* Configuration Management

### 🚧 In Progress

* Regex-Based Text Parsing

### 🔮 Planned

* Unit Testing
* Pandas Integration
* SQL Fundamentals Integration
* PostgreSQL-Based Persistence
* Enhanced Text Processing & Analytics
* GUI or Web Interface

---

## 📜 License
This project is licensed under the MIT License. See the LICENSE file for details.
