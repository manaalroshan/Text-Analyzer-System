import pytest
from text_analyzer import TextCleaner
from config import abbreviations_list

# Tests for words_extractor function.    
@pytest.mark.parametrize("text, expected", [
    ("  This is      an automated test.   ", ["this", "is", "an", "automated", "test"]),
    ("state-of-the-art, mother-in-law, On-duty", ["state-of-the-art", "mother-in-law", "on-duty"]),
    ("don't can't shouldn't.", ["don't", "can't", "shouldn't"]),
    (" ", []),
    ("  Hello, WORLD! state-of-the-art mother-in-law On-duty don't can't shouldn't Python's rock'n'roll test-case end-to-end foo-bar-baz --- !!! ??? ", ["hello", "world", "state-of-the-art", "mother-in-law", "on-duty", "don't", "can't", "shouldn't", "python's", "rock'n'roll", "test-case", "end-to-end", "foo-bar-baz"])
])
def test_words_extractor(text, expected):
    assert TextCleaner.words_extractor(text) == expected
    
def test_extract_words_result_is_none_raises_attribute_error():
    with pytest.raises(AttributeError):
        TextCleaner.words_extractor(None)
    
# Tests for normallized_abbreviations function.
@pytest.mark.parametrize("text, abbr_list, expected", [
    ("This is Mr. John he is our guest tonight.", ["Mr.", "night."], "This is Mr John he is our guest tonight."),
    ("Mr. and Mrs. Smith met Dr. Brown.", ["Mr.", "Mrs.", "Dr."], "Mr and Mrs Smith met Dr Brown."),
    ("U.S.A. is a country.", ["U.S.A."], "USA is a country."),
    ("Dr. Smith spoke to Mr.", ["Dr.", "Mr."], "Dr Smith spoke to Mr"),
    ("Mr. Mrs. Ms. Dr.", ["Mr.", "Mrs.", "Ms.", "Dr."], "Mr Mrs Ms Dr"),
    ("Hello Mr., how are you?", ["Mr."], "Hello Mr., how are you?"),
    ("  Mr.   Smith   met   Mrs.   Brown.  ", ["Mr.", "Mrs."], "Mr Smith met Mrs Brown."),
    ("Mr. Mr. Mr.", ["Mr."], "Mr Mr Mr"),
    ("(Mr.) Smith arrived.", ["Mr."], "(Mr.) Smith arrived."),
    ("Hello Mr.,John how are you?", ["Mr."], "Hello Mr.,John how are you?"),
    ("U.K is not in abbr. list.", ["abbr."], "U.K is not in abbr list."),
    ("mr. Smith met Mr. Brown.", ["Mr."], "mr Smith met Mr Brown."),
    ("", [], ""),  
])
def test_normallized_abbreviations(text, abbr_list, expected):
    assert TextCleaner.normalize_abbreviations(text, abbr_list) == expected

# Tests for get_sentence_wordcount function.
@pytest.mark.parametrize("text, expected", [
    ("This is a simple sentence.", [5]),
    ("Hello world! How are you? I am fine.", [2, 3, 3]),
    ("Go. Stop. Wait.", [1, 1, 1]),
    ("  This is one sentence.   This is another.  ", [4, 3]),
    ("This is a state-of-the-art solution.", [5]),
    ("Don't worry. It's going to be okay.", [2, 5]),
    ("This is Mr. John. He lives down the street. Is that okay?", [4, 5, 3]),
    ("Dr. Brown arrived. He sat down.", [3, 3]),
    ("Hello world. this is another sentence.", [6]),
    ("Version released. 2025 was a good year.", [2, 5]),
    ("Hello world.This is another sentence.", [5]),
])
def test_get_sentence_wordcount(text, expected):
    normalized = TextCleaner.normalize_abbreviations(text, abbreviations_list)
    assert TextCleaner.get_sentence_wordcount(normalized) == expected
    
# Tests for paragraph_count function.
@pytest.mark.parametrize("text, expected", [
    ("This is one paragraph.", 1),
    ("This is a test.\n\nFor Paragraph Detection.", 2),
    ("Paragraph one.\n\nParagraph two.\n\nParagraph three.", 3),
    ("Paragraph one.\n\n\n\nParagraph two.", 2),
    ("Paragraph one.\n   \n\t\nParagraph two.", 2),
    ("Paragraph one.\r\n\r\nParagraph two.", 2),
    ("", 0),
    ("   \n\t\n   ", 0),
    ("\n\nParagraph one.\n\nParagraph two.\n\n", 2),
    ("Line one.\nLine two.", 1),
])
def test_paragraph_count(text, expected):
    assert TextCleaner.paragraph_count(text) == expected
    
# Tests for build_word_frequency function.
@pytest.mark.parametrize("text, expected", [
    ("", {}),
    ("hello", {"hello": 1}),
    ("hello hello hello apple banana apple orange banana apple", {"hello": 3, "apple": 3, "banana": 2, "orange": 1}),
    ("hello world python", {"hello": 1, "world": 1, "python": 1}),
    ("Hello hello HELLO", {"hello": 3}),
    ("state-of-the-art don't state-of-the-art don't test", {"state-of-the-art": 2, "don't": 2, "test": 1}),
])
def test_build_word_frequency(text, expected):
    words = TextCleaner.words_extractor(text)
    assert TextCleaner.build_word_frequency(words) == expected
    
# Tests for sort_word_frequency function.
@pytest.mark.parametrize("text, expected", [
    ("", []),
    ("hello", [("hello", 1)]),
    ("a b c", [("a", 1), ("b", 1), ("c", 1)]),
    ("apple banana apple orange banana apple", [("apple", 3), ("banana", 2), ("orange", 1)]),
])
def test_sort_word_frequency(text, expected):
    words = TextCleaner.words_extractor(text)
    freq_data = TextCleaner.build_word_frequency(words)
    assert TextCleaner.sort_word_frequency(freq_data) == expected
    
# Tests for keywords_extractor function.
@pytest.mark.parametrize("text, stop_words, expected", [
    ("This is a simple test case", ["is", "a"], ["this", "simple", "test", "case"]),
    ("THIS is JAVA, IS this Java?", ["this", "is"], ["java", "java"]),
    ("state-of-the-art system is modern don't stop believing it's working", ["is", "stop"], ["state-of-the-art", "system", "modern", "don't", "believing", "it's", "working"]),
    ("version2 is better than version1 test3", ["is", "than"], ["version2", "better", "version1", "test3"]),
    ("the and is a the", ["the", "and", "is", "a"], []),
    ("", ["anything"], []),
    ("Hello!!! 1234 world??? This--is fun.", ["this"], ["hello", "world", "is", "fun"]),
    ("I have 2 apples and 10 oranges", ["and", "have", "i"], ["apples", "oranges"]
    ),
])
def test_keywords_extractor(text, stop_words, expected):
    assert TextCleaner.keywords_extractor(text, stop_words) == expected
    