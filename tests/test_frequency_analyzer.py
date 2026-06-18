from config import stop_words
from text_analyzer import AnalysisContext, FrequencyAnalyzer
from text_analyzer import TextCleaner


def test_frequency_analyzer_whole_pipeline():
    context = AnalysisContext("dummy")
    raw_text = "The quick brown fox jumps over the lazy dog. The fox is quick and the fox is clever."
    context.words = TextCleaner.words_extractor(raw_text)
    context.word_frequency = TextCleaner.build_word_frequency(context.words)
    context.sorted_word_frequency = TextCleaner.sort_word_frequency(context.word_frequency)
    
    context.keywords = TextCleaner.keywords_extractor(raw_text, stop_words)
    context.keyword_frequency = TextCleaner.build_word_frequency(context.keywords)
    context.sorted_keyword_frequency = TextCleaner.sort_word_frequency(context.keyword_frequency)
    
    analyzer = FrequencyAnalyzer()
    result = analyzer.analyze(context)
    assert result['most_frequent_word'] == ("the", 4)
    assert result['top_words'] == [('the', 4), ('fox', 3), ('quick', 2), ('is', 2), ('brown', 1)]
    assert result['top_keywords'] == [("fox", 3, 16.7), ("quick", 2, 11.1), ("brown", 1, 5.6), ("jumps", 1, 5.6), ("lazy", 1, 5.6)]


def test_frequency_analyzer_basic():
    context = AnalysisContext("dummy")
    context.words = ["hello", "world", "is", "python", "hello", "hello", "world"]
    context.sorted_word_frequency = [("hello", 3), ("world", 2), ("is", 1), ("python", 1)]
    context.sorted_keyword_frequency = [("hello", 3), ("world", 2), ("python", 1)]
    analyzer = FrequencyAnalyzer()
    result = analyzer.analyze(context)
    assert result['most_frequent_word'] == ("hello", 3)
    assert result['top_words'] == [("hello", 3), ("world", 2), ("is", 1), ("python", 1)]
    assert result['top_keywords'] == [("hello", 3, 42.9), ("world", 2, 28.6), ("python", 1, 14.3)]
    
def test_frequency_analyzer_even_distribution():
    context = AnalysisContext("dummy")
    context.words = ["apple", "banana", "cherry", "date"]
    context.sorted_word_frequency = [ ("apple", 1), ("banana", 1), ("cherry", 1), ("date", 1), ]
    context.sorted_keyword_frequency = [ ("apple", 1), ("banana", 1), ("cherry", 1), ("date", 1), ]

    analyzer = FrequencyAnalyzer()
    result = analyzer.analyze(context)

    assert result["most_frequent_word"] == ("apple", 1)
    assert result["top_words"] == [ ("apple", 1), ("banana", 1), ("cherry", 1), ("date", 1), ]
    assert result["top_keywords"] == [ ("apple", 1, 25.0), ("banana", 1, 25.0), ("cherry", 1, 25.0), ("date", 1, 25.0), ]
    
def test_frequency_analyzer_empty_input():
    context = AnalysisContext("dummy")
    context.words = []
    context.sorted_word_frequency = []
    context.sorted_keyword_frequency = []

    analyzer = FrequencyAnalyzer()
    result = analyzer.analyze(context)

    assert result["most_frequent_word"] is None
    assert result["top_words"] == []
    assert result["top_keywords"] == []