import pytest
from text_analyzer import TextCleaner
from config import abbreviations_list, email_pattern, url_pattern, date_pattern, phone_pattern

# words_extractor should turn raw text into lowercase words while preserving
# useful in-word punctuation such as apostrophes and hyphens.
@pytest.mark.parametrize("text, expected", [
    # Extra spaces and sentence punctuation should be ignored.
    ("  This is      an automated test.   ", ["this", "is", "an", "automated", "test"]),
    # Hyphenated compound words should stay as one token.
    ("state-of-the-art, mother-in-law, On-duty", ["state-of-the-art", "mother-in-law", "on-duty"]),
    # Contractions should keep their apostrophes.
    ("don't can't shouldn't.", ["don't", "can't", "shouldn't"]),
    # Blank input should return an empty list.
    (" ", []),
    # Mixed punctuation, capitalization, contractions, and hyphenated words.
    ("  Hello, WORLD! state-of-the-art mother-in-law On-duty don't can't shouldn't Python's rock'n'roll test-case end-to-end foo-bar-baz --- !!! ??? ", ["hello", "world", "state-of-the-art", "mother-in-law", "on-duty", "don't", "can't", "shouldn't", "python's", "rock'n'roll", "test-case", "end-to-end", "foo-bar-baz"])
])
def test_words_extractor(text, expected):
    assert TextCleaner.words_extractor(text) == expected

# None is not valid text input, so calling string methods on it should fail.
def test_extract_words_result_is_none_raises_attribute_error():
    with pytest.raises(AttributeError):
        TextCleaner.words_extractor(None)

# normalize_abbreviations should remove periods from known abbreviations only
# when they appear as standalone abbreviations.
@pytest.mark.parametrize("text, abbr_list, expected", [
    # Removes the period after a listed abbreviation, but keeps normal sentence punctuation.
    ("This is Mr. John he is our guest tonight.", ["Mr.", "night."], "This is Mr John he is our guest tonight."),
    ("Mr. and Mrs. Smith met Dr. Brown.", ["Mr.", "Mrs.", "Dr."], "Mr and Mrs Smith met Dr Brown."),
    # Multi-period abbreviations should collapse all internal periods.
    ("U.S.A. is a country.", ["U.S.A."], "USA is a country."),
    # Abbreviations at the end of the text should also be normalized.
    ("Dr. Smith spoke to Mr.", ["Dr.", "Mr."], "Dr Smith spoke to Mr"),
    ("Mr. Mrs. Ms. Dr.", ["Mr.", "Mrs.", "Ms.", "Dr."], "Mr Mrs Ms Dr"),
    # Abbreviations attached to commas or parentheses are left unchanged.
    ("Hello Mr., how are you?", ["Mr."], "Hello Mr., how are you?"),
    # Extra whitespace is normalized while abbreviations are cleaned.
    ("  Mr.   Smith   met   Mrs.   Brown.  ", ["Mr.", "Mrs."], "Mr Smith met Mrs Brown."),
    ("Mr. Mr. Mr.", ["Mr."], "Mr Mr Mr"),
    ("(Mr.) Smith arrived.", ["Mr."], "(Mr.) Smith arrived."),
    ("Hello Mr.,John how are you?", ["Mr."], "Hello Mr.,John how are you?"),
    # Only abbreviations included in the provided list should be changed.
    ("U.K is not in abbr. list.", ["abbr."], "U.K is not in abbr list."),
    # Matching is case-insensitive for listed abbreviations.
    ("mr. Smith met Mr. Brown.", ["Mr."], "mr Smith met Mr Brown."),
    ("", [], ""),  
])
def test_normallized_abbreviations(text, abbr_list, expected):
    assert TextCleaner.normalize_abbreviations(text, abbr_list) == expected

# get_sentence_wordcount should count words in each sentence after abbreviation
# cleanup prevents titles like "Mr." and "Dr." from splitting sentences.
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
    # Normalize first so abbreviation periods are not mistaken for sentence ends.
    normalized = TextCleaner.normalize_abbreviations(text, abbreviations_list)
    assert TextCleaner.get_sentence_wordcount(normalized) == expected

# paragraph_count should count blocks separated by blank lines, while treating
# normal single newlines as part of the same paragraph.
@pytest.mark.parametrize("text, expected", [
    ("This is one paragraph.", 1),
    ("This is a test.\n\nFor Paragraph Detection.", 2),
    ("Paragraph one.\n\nParagraph two.\n\nParagraph three.", 3),
    # Multiple blank lines still create one paragraph break.
    ("Paragraph one.\n\n\n\nParagraph two.", 2),
    # Blank lines containing spaces or tabs should still count as separators.
    ("Paragraph one.\n   \n\t\nParagraph two.", 2),
    # Windows-style newlines should work too.
    ("Paragraph one.\r\n\r\nParagraph two.", 2),
    ("", 0),
    ("   \n\t\n   ", 0),
    ("\n\nParagraph one.\n\nParagraph two.\n\n", 2),
    ("Line one.\nLine two.", 1),
])
def test_paragraph_count(text, expected):
    assert TextCleaner.paragraph_count(text) == expected

# build_word_frequency should count how often each extracted word appears.
@pytest.mark.parametrize("text, expected", [
    ("", {}),
    ("hello", {"hello": 1}),
    ("hello hello hello apple banana apple orange banana apple", {"hello": 3, "apple": 3, "banana": 2, "orange": 1}),
    ("hello world python", {"hello": 1, "world": 1, "python": 1}),
    ("Hello hello HELLO", {"hello": 3}),
    ("state-of-the-art don't state-of-the-art don't test", {"state-of-the-art": 2, "don't": 2, "test": 1}),
])
def test_build_word_frequency(text, expected):
    # Use the real extractor so frequency tests cover lowercase normalization too.
    words = TextCleaner.words_extractor(text)
    assert TextCleaner.build_word_frequency(words) == expected

# sort_word_frequency should return word-count pairs from most common to least common.
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

# keywords_extractor should remove stop words after cleaning and lowercasing text.
@pytest.mark.parametrize("text, stop_words, expected", [
    ("This is a simple test case", ["is", "a"], ["this", "simple", "test", "case"]),
    ("THIS is JAVA, IS this Java?", ["this", "is"], ["java", "java"]),
    # Important word shapes should survive keyword extraction.
    ("state-of-the-art system is modern don't stop believing it's working", ["is", "stop"], ["state-of-the-art", "system", "modern", "don't", "believing", "it's", "working"]),
    # Digits inside words are allowed.
    ("version2 is better than version1 test3", ["is", "than"], ["version2", "better", "version1", "test3"]),
    ("the and is a the", ["the", "and", "is", "a"], []),
    ("", ["anything"], []),
    # Standalone numbers and punctuation should not become keywords.
    ("Hello!!! 1234 world??? This--is fun.", ["this"], ["hello", "world", "is", "fun"]),
    ("I have 2 apples and 10 oranges", ["and", "have", "i"], ["apples", "oranges"]
    ),
])
def test_keywords_extractor(text, stop_words, expected):
    assert TextCleaner.keywords_extractor(text, stop_words) == expected

# email_extractor should return valid email-like matches and reject malformed ones.
@pytest.mark.parametrize("text, expected", [
    ("Contact me at john.doe@example.com", ["john.doe@example.com"]),
    ("Emails: alice@test.com and bob.smith@company.org", ["alice@test.com", "bob.smith@company.org"]),
    # Plus aliases and subdomains are valid.
    ("Send to user+tag@mail.example.co.uk", ["user+tag@mail.example.co.uk"]),
    ("There is no email here", []),
    # Consecutive dots should not be accepted.
    ("john..doe@example.com john@exam..ple.com", []),
    ("Valid: jane@test.com Invalid: bad..email@test.com", ["jane@test.com"]),
    # Underscores, hyphenated domains, digits, and uppercase letters are allowed.
    ("user_name@example.com user@my-domain.com", ["user_name@example.com", "user@my-domain.com"]),
    ("abc123@test123.com", ["abc123@test123.com"]),
    # Top-level domains must be long enough.
    ("user@example.c", []),
    ("Email me at test@example.com.", ["test@example.com"]),
    ("USER.NAME@EXAMPLE.COM", ["USER.NAME@EXAMPLE.COM"]),
])
def test_email_extractor(text, expected):
    assert TextCleaner.email_extractor(text, email_pattern) == expected

# url_extractor should detect URLs with or without protocol and avoid emails.
@pytest.mark.parametrize("text, expected", [
    # Simple URL
    ("Visit https://example.com", ["https://example.com"]),
    # URL without protocol
    ("Visit example.com", ["example.com"]),
    # Multiple URLs
    ("Check example.com and https://google.com", ["example.com", "https://google.com"]),
    # Subdomain
    ("Go to docs.python.org", ["docs.python.org"]),
    # Path
    ("https://example.com/path/to/page", ["https://example.com/path/to/page"]),
    # Query string
    ("https://example.com/search?q=test&page=1 example.com/search?q=test", ["https://example.com/search?q=test&page=1", "example.com/search?q=test"]),
    # No URLs
    ("Just some plain text", []),
    # Email should be filtered out
    ("Email me at test@example.com", []),
     # Mixed URL and email
    ("Email test..@example.com and visit example.com", ["example.com"]),
    # Multiple emails and URLs
    ("a@test.com b@test.org example.com github.com", ["example.com", "github.com"]),
    # URL with hyphens
    ("https://my-site.example.com", ["https://my-site.example.com"]),
    # URL with trailing slash
    ("https://example.com/", ["https://example.com/"]),
    # URL surrounded by punctuation
    ("Visit (https://example.com) today", ["https://example.com"]),
     # TLD too short
    ("example.c", []),
])
def test_url_extractor(text, expected):
    assert TextCleaner.url_extractor(text, url_pattern, email_pattern) == expected

# phone_extractor should match common international phone formats while avoiding
# short or unrelated digit groups.
@pytest.mark.parametrize("text, expected", [
    # Plain international format
    ("Call me at 911234567890", ["911234567890"]),
    # Leading plus
    ("Call me at +911234567890", ["+911234567890"]),
     # Country code + local number
    ("Phone: +91 1234567890", ["+91 1234567890"]),
    # US-style with parentheses
    ("Office: +1 (555) 123-4567", ["+1 (555) 123-4567"]),
    # Without plus
    ("Office: 1 (555) 123-4567", ["1 (555) 123-4567"]),
    # Spaces instead of hyphens
    ("Office: 1 555 123 4567", ["1 555 123 4567"]),
    # Alternative pattern
    ("Reach me at 91 12345 67890", ["91 12345 67890"]),
    # Multiple numbers
    ("Numbers: +91 1234567890 and +1 (555) 123-4567", ["+91 1234567890", "+1 (555) 123-4567"]),
    # No phone numbers
    ("There are no phone numbers here", []),
    # Too short
    ("12345", []),
    # Random digits that shouldn't match
    ("ID 123456 and zip 90210", []),
    # Embedded in text
    ("Contact:+91 1234567890 immediately", ["+91 1234567890"]),
])
def test_phone_number_extractor(text, expected):
    assert TextCleaner.phone_extractor(text, phone_pattern) == expected

# date_extractor should match supported long-form and numeric date formats.
@pytest.mark.parametrize("text, expected", [
    ("Meeting on 25 December, 2024", ["25 December, 2024"]),
    ("Meeting on December 25, 2024", ["December 25, 2024"]),
    ("Date: 2024-12-25", ["2024-12-25"]),
    ("Date: 25-12-2024", ["25-12-2024"]),
    ("Date: 25/12/2024", ["25/12/2024"]),
    ("Date: 2024/12/25", ["2024/12/25"]),
    ("Start 2024-12-25 End 2025-01-01", ["2024-12-25", "2025-01-01"]),
    ("25 December, 2024 and December 26, 2024", ["25 December, 2024", "December 26, 2024"]),
    ("No dates here", []),
    ("20241225", []),
    ("25-12-24", []),
    ("25/12/24", []),
    ("2024/12", []),
    # Dates can be found even when directly next to surrounding text.
    ("2024-12-25abc", ["2024-12-25"]),
    ("abc2024-12-25", ["2024-12-25"]),
    ("2024-12-25, 25/12/2024, December 25, 2024", ["2024-12-25", "25/12/2024", "December 25, 2024"]),
])
def test_dates_extractor(text, expected):
    assert TextCleaner.date_extractor(text, date_pattern) == expected