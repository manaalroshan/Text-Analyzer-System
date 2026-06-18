from text_analyzer import AnalysisContext, ParagraphAnalyzer, TextCleaner
from config import abbreviations_list

def test_paragraph_analyzer_whole_pipeline():
    context = AnalysisContext("dummy")
    context.raw_text = ("This is paragraph one.\n" "It has two sentences.\n" "\n" "\n" "This is paragraph two.\n" "It is short.\n" "\n" "\n" "\n" "This is paragraph three.\n" "Another short sentence here.\n" "\n" "\n" "\n" "\n" "\n" "Final paragraph.\n" "Last sentence.")
    context.normalized_abbreviations = TextCleaner.normalize_abbreviations(context.raw_text, abbreviations_list)
    context.sentence_wordcount = TextCleaner.get_sentence_wordcount(context.normalized_abbreviations)
    context.paragraph_count = TextCleaner.paragraph_count(context.raw_text)
    analyzer = ParagraphAnalyzer()
    result = analyzer.analyze(context)
    assert result['paragraph_count'] == 4
    assert result['avg_sentence_para'] == 2