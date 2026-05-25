import string
from config import stop_words, abbreviations_list, reading_wpm, speaking_wpm, buffer_time, vocab_statements
from abc import ABC, abstractmethod

# Abstract base class for all analyzers, defining the interface for analysis.
class Analyzer(ABC):
    @abstractmethod
    def analyze(self, context):
        """
        Analyzes the given context and returns a dictionary of results.
        Each concrete analyzer must implement this method.
        """
        pass

# Helper class containing static methods for common text cleaning and preprocessing tasks.
class TextCleaner:
    @staticmethod
    def remove_punctuation(text):
        """Removes punctuation from the text, preserving apostrophes and hyphens."""
        modified_punctuation = string.punctuation.replace("'", "").replace("-", "")
        return text.translate(str.maketrans("","", modified_punctuation)).lower()
    
    @staticmethod
    def split_text_into_words(text):
        """Cleans text by removing punctuation and then splits it into a list of words."""
        return TextCleaner.remove_punctuation(text).split()
    
    @staticmethod
    def normalize_abbreviations(text, abbreviations_list):
        """Removes periods from recognized abbreviations to prevent false sentence breaks."""
        words_list = text.strip().split()
        new_word_list = [word.replace(".", "") if word in abbreviations_list else word for word in words_list]
        return " ".join(new_word_list)
    
    @staticmethod
    def get_sentence_wordcount(normalized_text):
        """Splits text into sentences and returns a list of word counts for each sentence."""
        # Now will Calculate Min and Mix words sentences.
        # First we gonna split the paragraph into sentences and store the numbers of words per sentence in a list.
        text = normalized_text.replace("?", ".").replace("!", ".").split(".")
        text = [i.strip() for i in text if i.strip()]
        return [len(i.split()) for i in text]
    
    @staticmethod
    def build_word_frequency(words):
        """Builds a dictionary mapping each word to its frequency."""
        word_frequency_dict = {}
        for word in words:
            word_frequency_dict[word] = word_frequency_dict.get(word, 0) + 1
        return word_frequency_dict
        
    @staticmethod
    def sort_word_frequency(freq_dict): # Renamed for clarity
        """Sorts a word frequency dictionary into a list of (word, count) tuples in descending order."""
        sorted_frequency_list = list(freq_dict.items())
        sorted_frequency_list.sort(reverse=True, key=lambda x:x[1])
        return sorted_frequency_list
    
    @staticmethod
    def sentence_count(normalized_abbreviations):
        sentence_count = 0
        punctuation_list = ["?", ".", "!"]
        # Heuristic for sentence counting:
        # 1. Initialize count to 1 if any alphanumeric character exists (assuming at least one sentence).
        # 2. Increment count for patterns like "[.!?] + space + uppercase letter".
    
        valid_letter = any(i.isalnum() for i in normalized_abbreviations)
        if valid_letter:
            sentence_count = 1
            
        # Apply heuristic for sentence boundaries
        for i in range(len(normalized_abbreviations)-2):
            if normalized_abbreviations[i] in punctuation_list:
                if normalized_abbreviations[i+1] == " " and normalized_abbreviations[i+2].isupper():
                    sentence_count += 1
        return sentence_count
    
    @staticmethod
    def paragraph_count(raw_text):
        # Paragraphs are typically separated by blank lines (two consecutive newlines).
        text = raw_text.strip().splitlines()
        
        # Logic to identify paragraphs based on blank lines.
        # A paragraph is a sequence of non-empty lines.
        # When a blank line is encountered, the current accumulated lines form a paragraph.
        # to the paragraph list and then reset the current paragraph buffer.
        # After processing all lines, if anything remains in the current buffer,
        # we add it as the last paragraph.
        paragraphs = []
        current_paragraph = []
        for line in text:
            if line.strip():
                current_paragraph.append(line)
            else:
                if current_paragraph:
                    paragraphs.append(current_paragraph)
                    current_paragraph = []
        if current_paragraph:
            paragraphs.append(current_paragraph)
        return len(paragraphs)
 
# AnalysisContext acts as a shared data store for all analyzers, holding raw text and preprocessed data.   
class AnalysisContext:
    def __init__(self, text):
        self.raw_text = text
        # Preprocessed words (punctuation removed, lowercased)
        self.words = TextCleaner.split_text_into_words(text)  
        # Frequency map of all words
        self.word_frequency = TextCleaner.build_word_frequency(self.words)
        # Sorted list of (word, count) tuples by frequency
        self.sorted_word_frequency = TextCleaner.sort_word_frequency(self.word_frequency)
        # Text with abbreviations normalized for better sentence detection
        self.normalized_abbreviations = TextCleaner.normalize_abbreviations(text, abbreviations_list)
        # Sentence count logic
        self.sentence_count = TextCleaner.sentence_count(self.normalized_abbreviations)
        # List of word counts for each sentence
        self.sentence_wordcount = TextCleaner.get_sentence_wordcount(self.normalized_abbreviations)
        # Paragraph count logic
        self.paragraph_count = TextCleaner.paragraph_count(self.raw_text)
        # Stores Analyzer's results for context
        self.results = {}
  
# Concrete Analyzer classes --------------------------   

# Analyzes word-based statistics such as total words, unique words, and the longest word.
class WordAnalyzer(Analyzer):
    def analyze(self, context):
        words = context.words
        if not words: # Handle case where no valid words are found
            raise ValueError("Input text contains no valid words")
        longest_word = max(words, key=len)
        
        return {
            "word_count": len(words),
            "unique_word_count": len(set(words)),
            "longest_word": longest_word,
            "length_longest_word": len(longest_word)
        }

# Analyzes character-based statistics, counting characters with and without spaces.
class CharacterAnalyzer(Analyzer):
    def analyze(self, context):
        raw_text = context.raw_text
        return {
            "char_count_with_spaces": len(raw_text),
            "char_count_without_spaces": len("".join(raw_text.split()))
        }
        
# Analyzes lexical metrics like reading time, speaking time, and vocabulary richness.
class LexicalAnalyzer(Analyzer):
    def __init__(self, reading_wpm, speaking_wpm, buffer_time, vocab_statements):
        self.reading_wpm = reading_wpm
        self.speaking_wpm = speaking_wpm
        self.buffer_time = buffer_time
        self.vocab_statements = vocab_statements
        
    def analyze(self, context):
        # Requires WordAnalyzer results to calculate lexical metrics.
        try:
            word_stats = context.results["WordAnalyzer"]
        except KeyError:
            raise RuntimeError("LexicalAnalyzer requires WordAnalyzer to run first.")
        
        vocab_score = (word_stats["unique_word_count"] / word_stats["word_count"]) * 100
        
        vocabulary_comments = "N/A"
        if word_stats['word_count'] < 20:
            vocabulary_comments= "Insufficient data for richness score"
        else:
            for limit, remark in self.vocab_statements:
                if vocab_score <= limit:
                    vocabulary_comments = remark
                    break           
        
        return {
            "reading_time": (word_stats["word_count"] / self.reading_wpm) * 60, # Convert to seconds
            "speaking_time": (word_stats["word_count"] / self.speaking_wpm) * self.buffer_time * 60, # Convert to seconds with buffer
            "vocabulary_score": vocab_score,
            "vocabulary_remarks": vocabulary_comments,
        }
        
# Analyzes word frequencies, identifying most frequent words and keywords (excluding stop words).
class FrequencyAnalyzer(Analyzer):
    def __init__(self, stop_words):
        self.stop_words = stop_words
        
    def analyze(self, context):
        sorted_word_frequency = context.sorted_word_frequency # Use the renamed attribute
        
        show_words = min(5, len(sorted_word_frequency)) # Determine how many top words to display
        top_keywords = [(word, count) for word, count in sorted_word_frequency if word not in self.stop_words]
        
        return {
            "most_frequent_word": sorted_word_frequency[0],
            "top_words": [(sorted_word_frequency[i][0], sorted_word_frequency[i][1]) for i in range(show_words)],
            "top_keywords": top_keywords[:5]
        }
  
# Analyzes sentence-based statistics, including total sentences, and min/max/average word/character counts per sentence.
class SentenceAnalyzer(Analyzer):
    def analyze(self, context):                    
        return {
            "sentence_count": context.sentence_count,
            "max_words_sentence": max(context.sentence_wordcount, default=0),
            "min_words_sentence": min(context.sentence_wordcount, default=0),
            "avg_chars_sentence": len(context.raw_text) / context.sentence_count if context.sentence_count > 0 else 0,
            "avg_words_sentence": len(context.words) / context.sentence_count if context.sentence_count > 0 else 0,
        }
    
# Analyzes paragraph-based statistics, counting paragraphs and average sentences per paragraph.
class ParagraphAnalyzer(Analyzer):
    def analyze(self, context):
        return {
            "paragraph_count": context.paragraph_count,
            "avg_sentence_para": context.sentence_count / context.paragraph_count if context.paragraph_count > 0 else 0,
        }  

# AnalyzerEngine orchestrates the execution of multiple Analyzer instances.
class AnalyzerEngine:
    def __init__(self):
        self.analyzers = []
        
    def add_analyzer(self, analyzer):
        self.analyzers.append(analyzer)
        
    def run(self, text):
        """Executes all added analyzers on the given text, storing results in the context."""
        context = AnalysisContext(text)

        for analyzer in self.analyzers:
            # Store results in the context, keyed by the analyzer's class name.
            context.results[type(analyzer).__name__] = analyzer.analyze(context)
        return context.results
        
# AnalyzerApp is the main entry point for the text analysis system.
class AnalyzerApp:
    def __init__(self):
        self.engine = AnalyzerEngine()
        self.engine.add_analyzer(WordAnalyzer())
        self.engine.add_analyzer(CharacterAnalyzer())
        self.engine.add_analyzer(LexicalAnalyzer(reading_wpm, speaking_wpm, buffer_time, vocab_statements))
        self.engine.add_analyzer(FrequencyAnalyzer(stop_words))
        self.engine.add_analyzer(SentenceAnalyzer())
        self.engine.add_analyzer(ParagraphAnalyzer())
        
    def analyze(self, text):
        """Initiates the analysis process and handles potential errors."""
        try:
            return self.engine.run(text)
        except ValueError:
            return None