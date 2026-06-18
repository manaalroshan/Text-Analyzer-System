import pytest
from text_analyzer import LexicalAnalyzer, AnalysisContext, WordAnalyzer
from config import reading_wpm, speaking_wpm, buffer_time, vocab_statements

# Lexical Analyzer Tests
@pytest.mark.parametrize("word_count, unique_word_count, reading_time, speaking_time, vocab_score, expected_remark ", [
    (10, 10, 2.4, 4.125, 100.0, "Small text sample - interpret cautiously"),
    (20, 4, 4.8, 8.25, 20.0, "Very repetitive vocabulary"),
    ( 20, 12, 4.8, 8.25, 60.0, "Balanced vocabulary"),
    ( 20, 16, 4.8, 8.25, 80.0, "Diverse vocabulary"),
    ( 20, 20, 4.8, 8.25, 100.0, "Highly varied vocabulary"),
    ( 50, 25, 12.0, 20.625, 50.0, "Balanced vocabulary"),
])
def test_lexical_analyzer(word_count, unique_word_count, reading_time, speaking_time, vocab_score, expected_remark):
    context = AnalysisContext("dummy")
    context.results['WordAnalyzer'] = {'word_count': word_count, 'unique_word_count': unique_word_count}
    analyzer = LexicalAnalyzer(reading_wpm, speaking_wpm, buffer_time, vocab_statements)
    result = analyzer.analyze(context)
    assert result['reading_time'] == pytest.approx(reading_time, abs=0.01)
    assert result['speaking_time'] == pytest.approx(speaking_time, abs=0.01)
    assert result['vocabulary_score'] == pytest.approx(vocab_score, abs=0.01)
    assert result['vocabulary_remarks'] == expected_remark

# WordAnalyzer - Lexical Analyzer Pipeline Test
@pytest.mark.parametrize("words, reading_time, speaking_time, vocab_score, expected_remark", [
    (["hello", "we", "are", "testing", "lexical", "analyzer"], 1.44, 2.475, 100.0, "Small text sample - interpret cautiously"),
    (["hello", "hello", "world", "world", "python"], 1.2, 2.062, 60.0, "Small text sample - interpret cautiously"),
    (["w1", "w2", "w3", "w4", "w5", "w6", "w7", "w8", "w9", "w10", "w1", "w2", "w3", "w4", "w5","w6", "w7", "w8", "w9", "w10"], 4.8, 8.25, 50.0, "Balanced vocabulary"),

])
def test_word_to_lexical_analyzers(words, reading_time, speaking_time, vocab_score, expected_remark):
    context = AnalysisContext("dummy")
    context.words = words
    analyzers = [WordAnalyzer(), LexicalAnalyzer(reading_wpm, speaking_wpm, buffer_time, vocab_statements)]
    for analyzer in analyzers:
        context.results[type(analyzer).__name__] = analyzer.analyze(context)
    lexical_result = context.results["LexicalAnalyzer"]
    assert lexical_result['reading_time'] == pytest.approx(reading_time, abs=0.01)
    assert lexical_result['speaking_time'] == pytest.approx(speaking_time, abs=0.01)
    assert lexical_result['vocabulary_score'] == vocab_score
    assert lexical_result['vocabulary_remarks'] == expected_remark
    
# WordAnalyzer - LexicalAnalyzer Dependacy Test
def test_lexical_analyzer_requires_word_analyzer():
    context = AnalysisContext("dummy")
    context.words = ["hello", "world"]

    analyzer = LexicalAnalyzer(reading_wpm, speaking_wpm, buffer_time, vocab_statements)
    with pytest.raises(RuntimeError, match="LexicalAnalyzer requires WordAnalyzer to run first."):
        analyzer.analyze(context)
    
    