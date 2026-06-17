import pytest
from text_analyzer import WordAnalyzer
from text_analyzer import AnalysisContext
    
@pytest.mark.parametrize("words, word_count, unique_word_count, longest_word", [
    (["We", "are", "testing", "wordanalyzer"], 4, 4, "wordanalyzer"),
    (["hello", "hello", "world"], 3, 2, "hello"),
    (["test", "test", "test", "test"], 4, 1, "test"),
    (["apple", "banana", "apple", "cherry", "banana"], 5, 3, "banana"),
    (["extraordinary", "cat", "dog"], 3, 3, "extraordinary"),
    (["cat", "dog", "sun"], 3, 3, "cat"),
    (["Hello", "hello", "HELLO"], 3, 3, "Hello"),
    (["123", "4567", "89"], 3, 3, "4567"),
    (["abc123", "test", "longestword999"], 3, 3, "longestword999"),
])
def test_word_analyzer(words, word_count, unique_word_count, longest_word):
    context = AnalysisContext("dummy")
    context.words = words
    analyzer = WordAnalyzer()
    result = analyzer.analyze(context)
    assert result['word_count'] == word_count
    assert result['unique_word_count'] == unique_word_count
    assert result['longest_word'] == longest_word
    
def test_word_analyzer_if_no_valid_words():
    context = AnalysisContext("dummy")
    context.words = []
    analyzer = WordAnalyzer()
    with pytest.raises(ValueError):
        analyzer.analyze(context)