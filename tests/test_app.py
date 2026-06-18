import pytest
from text_analyzer import AnalyzerApp
from report_generator import ReportGenerator, ReportExporter
from config import json_output_path, output_path

def test_app_pipeline():
    text = "This is a text."
    app = AnalyzerApp()
    result = app.analyze(text)
    assert result['WordAnalyzer']['word_count'] == 4
    assert result['CharacterAnalyzer']['char_count_with_spaces'] == 15
    assert result['SentenceAnalyzer']['sentence_count'] == 1

def test_app_pipeline_no_input():
    app = AnalyzerApp()
    result = app.analyze("")
    assert result is None
    
def test_report_generation_file_creation():
    text = "Lets Generate Report"
    app = AnalyzerApp()
    result = app.analyze(text)
    generator = ReportGenerator()
    generator.build_report(result)
    report = generator.generate_report(result)
    exporter = ReportExporter()
    exporter.save_json(result, json_output_path)
    exporter.save_report(report, output_path)
    assert json_output_path.exists()
    assert output_path.exists()
    
def test_report_generation_correctness():
    text = "Lets Generate Report. Email: test@example.com Phone: +1-555-123-4567 Date: 2026-06-19 URL: https://example.com"
    app = AnalyzerApp()
    result = app.analyze(text)
    generator = ReportGenerator()
    generator.build_report(result)
    report = generator.generate_report(result)
    assert "Total Words: 15" in report
    assert "Total Characters (with spaces): 110" in report
    assert "Total Sentences: 2" in report
    assert "Emails Found: 1" in report