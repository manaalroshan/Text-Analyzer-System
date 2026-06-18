import pytest
from text_analyzer import AnalysisContext, SentenceAnalyzer, TextCleaner
from config import abbreviations_list

def test_sentence_analyzer_whole_pipeline():
    context = AnalysisContext("dummy")
    context.raw_text = "Dr. Smith arrived at 9'o clock. He met Mr. Jones there. The U.S.A. team won today. We reviewed the FAQ quickly. Prof. Brown gave updates. The CEO shared news. Mrs. Davis joined later. The meeting ended at 5 pm."
    context.words = TextCleaner.words_extractor(context.raw_text)
    context.normalized_abbreviations = TextCleaner.normalize_abbreviations(context.raw_text, abbreviations_list)
    context.sentence_wordcount = TextCleaner.get_sentence_wordcount(context.normalized_abbreviations)
    analyzer = SentenceAnalyzer()
    result = analyzer.analyze(context)
    assert result['sentence_count'] == 8
    assert result['max_words_sentence'] == 6
    assert result['min_words_sentence'] == 4
    assert result['avg_chars_sentence'] == 26.25
    assert result['avg_words_sentence'] == 5.125
    
@pytest.mark.parametrize("raw_text, words, sentence_wordcount, sentence_count, max_words_sentence, min_words_sentence, avg_chars_sentence, avg_words_sentence", [
    ("One two three four.", ["one", "two", "three", "four"], [4], 1, 4, 4, 19.0, 4.0),
    ("One two three. Four five six seven.", ["one", "two", "three", "four", "five", "six", "seven"], [3, 4], 2, 4, 3, 17.5, 3.5),
    ("", [], [], 0, 0, 0, 0, 0)
])
def test_sentence_analyzer_stats(raw_text, words, sentence_wordcount, sentence_count, max_words_sentence, min_words_sentence, avg_chars_sentence, avg_words_sentence):
    context = AnalysisContext("dummy")
    context.raw_text = raw_text
    context.words = words
    context.sentence_wordcount = sentence_wordcount
    analyzer = SentenceAnalyzer()
    result = analyzer.analyze(context)
    assert result['sentence_count'] == sentence_count
    assert result['max_words_sentence'] == max_words_sentence
    assert result['min_words_sentence'] == min_words_sentence
    assert result['avg_chars_sentence'] == pytest.approx(avg_chars_sentence)
    assert result['avg_words_sentence'] == pytest.approx(avg_words_sentence)