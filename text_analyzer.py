import re
from config import stop_words, abbreviations_list, reading_wpm, speaking_wpm, buffer_time, vocab_statements
from config import date_pattern, email_pattern, url_pattern, phone_pattern
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
    def words_extractor(text):
        clean_text = re.findall(r"[a-zA-Z0-9]+(?:[-'’—][a-zA-Z0-9]+)*", text.lower())
        return clean_text
    
    @staticmethod
    def normalize_abbreviations(text, abbreviations_list):
        """Removes periods from recognized abbreviations to prevent false sentence breaks."""
        words_list = text.strip().split()
        new_word_list = [word.replace(".", "") if word in abbreviations_list else word for word in words_list]
        return " ".join(new_word_list)
    
    @staticmethod
    def get_sentence_wordcount(normalized_text):
        """Splits text into sentences and returns a list of word counts for each sentence."""
        sentences = re.split(r"(?<=[!.?])\s+(?=[A-Z0-9])", normalized_text)
        return [len(sentence.split()) for sentence in sentences]
    
    @staticmethod
    def sentence_count(splitted_sentences):
        return len(splitted_sentences)
    
    @staticmethod
    def keywords_extractor(text, stop_words):
        extracted_words = re.findall(r"\d*[a-zA-Z]+\d*(?:[-'’—][a-zA-Z0-9]+)*", text.lower())
        final_result = [keyword for keyword in extracted_words if keyword not in stop_words]
        return final_result
    
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
    def paragraph_count(raw_text):
        paragraph_pattern = r"\r?\n[\t\r ]*\n+"
        paragraph_split = [paragraph.strip() for paragraph in re.split(paragraph_pattern, raw_text) if paragraph.strip()]
        return len(paragraph_split)
    
    @staticmethod
    def entity_extractor(text, date_pattern, email_pattern, url_pattern, phone_pattern):
        email_list = re.findall(email_pattern, text, re.X)
        clean_email = [email for email in email_list if ".." not in email]

        url_list = re.findall(url_pattern, text, re.X)
        clean_url = [url for url in url_list if "@" not in url and url not in clean_email]

        raw_phone_numbers = re.findall(phone_pattern, text, re.X)
        raw_dates = re.findall(date_pattern, text, re.X)
        
        return {
            "emails": clean_email,
            "urls": clean_url,
            "phones": raw_phone_numbers,
            "dates": raw_dates
        }
    
# AnalysisContext acts as a shared data store for all analyzers, holding raw text and preprocessed data.   
class AnalysisContext:
    def __init__(self, text):
        self.raw_text = text
        # Preprocessed words (punctuation removed, lowercased)
        self.words = TextCleaner.words_extractor(self.raw_text) 
        # Keywords extraction and frequency calculation
        self.keywords = TextCleaner.keywords_extractor(self.raw_text, stop_words) 
        self.keyword_frequency = TextCleaner.build_word_frequency(self.keywords)
        self.sorted_keyword_frequency = TextCleaner.sort_word_frequency(self.keyword_frequency)
        # Frequency map of all words
        self.word_frequency = TextCleaner.build_word_frequency(self.words)
        # Sorted list of (word, count) tuples by frequency
        self.sorted_word_frequency = TextCleaner.sort_word_frequency(self.word_frequency)
        # Text with abbreviations normalized for better sentence detection
        self.normalized_abbreviations = TextCleaner.normalize_abbreviations(text, abbreviations_list)
        # List of word counts for each sentence
        self.sentence_wordcount = TextCleaner.get_sentence_wordcount(self.normalized_abbreviations)
        # Sentence count logic
        self.sentence_count = TextCleaner.sentence_count(self.sentence_wordcount)
        # Paragraph count logic
        self.paragraph_count = TextCleaner.paragraph_count(self.raw_text)
        # Entity Logic
        self.entities = TextCleaner.entity_extractor(self.raw_text, date_pattern, email_pattern, url_pattern, phone_pattern)
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
            vocabulary_comments= "Small text sample - interpret cautiously"
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
    def analyze(self, context):
        sorted_word_frequency = context.sorted_word_frequency
        # Calculating Keyword Density
        top_keywords = []
        for keyword, count in context.sorted_keyword_frequency:
            density = round((count / len(context.words)) * 100, 1)
            top_keywords.append((keyword, count, density))
        return {
            "most_frequent_word": sorted_word_frequency[0],
            "top_words": sorted_word_frequency[:5],
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
        
# Entity Analyzer
class EntityAnalyzer(Analyzer):
    def analyze(self, context):
        entities = context.entities
        return {
            'Emails': entities['emails'],
            'Urls': entities['urls'],
            'Phone Numbers': entities['phones'],
            'Dates': entities['dates'] 
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
        self.engine.add_analyzer(FrequencyAnalyzer())
        self.engine.add_analyzer(SentenceAnalyzer())
        self.engine.add_analyzer(ParagraphAnalyzer())
        self.engine.add_analyzer(EntityAnalyzer())
        
    def analyze(self, text):
        """Initiates the analysis process and handles potential errors."""
        try:
            return self.engine.run(text)
        except ValueError:
            return None