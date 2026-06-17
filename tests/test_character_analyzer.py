import pytest
from text_analyzer import CharacterAnalyzer
from text_analyzer import AnalysisContext

@pytest.mark.parametrize("raw_text, char_count_WS, char_count_NS", [
    ("this is a test.", 15, 12),
    ("hello", 5, 5),
    ("", 0, 0),
    ("   ", 3, 0),
    (" hello ", 7, 5),
    ("hello   world", 13, 10),
    ("123 456", 7, 6),
    ("!@# $%^", 7, 6),
    ("Python 3.12", 11, 10),
])
def test_character_analyzer(raw_text, char_count_NS, char_count_WS):
    context = AnalysisContext("dummy")
    context.raw_text = raw_text
    analyzer = CharacterAnalyzer()
    result = analyzer.analyze(context)
    assert result['char_count_with_spaces'] == char_count_WS
    assert result['char_count_without_spaces'] == char_count_NS
    