import string
from config import stop_words, abbreviations_list, vocab_statements, reading_wpm, speaking_wpm, buffer_time

class Analyzer:
    def analyze(self, context):
        raise NotImplementedError

class TextCleaner:
    @staticmethod
    def remove_punctuation(text):
        modified_punctuation = string.punctuation.replace("'", "").replace("-", "")
        return text.translate(str.maketrans("","", modified_punctuation)).lower()
    
    @staticmethod
    def split_text_into_words(text):
        return TextCleaner.remove_punctuation(text).split()
    
class AnalysisContext:
    def __init__(self, text):
        self.raw_text = text
        self.words = TextCleaner.split_text_into_words(text)  
        self.word_frequency = FrequencyHelper.build_word_frequency(self.words)
        self.sorted_frequency = FrequencyHelper.sort_word_frequency(self.word_frequency)
        self.results = {}
  
    
class WordAnalyzer(Analyzer):
    def analyze(self, context):
        words = context.words
        if not words:
            raise ValueError("Input text contains no valid words")
        longest_word = max(words, key=len)
        
        return {
            "word_count": len(words),
            "unique_word_count": len(set(words)),
            "longest_word": longest_word,
            "length_longest_word": len(longest_word)
        }

class CharacterAnalyzer(Analyzer):
    def analyze(self, context):
        raw_text = context.raw_text
        return {
            "char_count_with_spaces": len(raw_text),
            "char_count_without_spaces": len("".join(raw_text.split()))
        }
        
class LexicalAnalyzer(Analyzer):
    def __init__(self, reading_wpm, speaking_wpm, buffer_time):
        self.reading_wpm = reading_wpm
        self.speaking_wpm = speaking_wpm
        self.buffer_time = buffer_time
        
    def analyze(self, context):
        word_stats = context.results["WordAnalyzer"]
        
        if not word_stats:
            raise RuntimeError("LexicalAnalyzer requires WordAnalyzer to run first.")
        
        return {
            "reading_time": 60 * (word_stats["word_count"] / self.reading_wpm),
            "speaking_time": (word_stats["word_count"] / self.speaking_wpm) * self.buffer_time * 60,
            "vocabulary_score": (word_stats["unique_word_count"] / word_stats["word_count"]) * 100,
        }
        
class FrequencyAnalyzer(Analyzer):
    def __init__(self, stop_words):
        self.stop_words = stop_words
        
    def analyze(self, context):
        sorted_frequency = context.sorted_frequency 
        
        show_words = min(5, len(sorted_frequency)) # for top words
        
        top_keywords_list = [(word, count) for word, count in sorted_frequency if word not in self.stop_words]
        
        return {
            "most_frequent_word": ((sorted_frequency[0][0], sorted_frequency[0][1])),
            "top_words": [((sorted_frequency[i][0], sorted_frequency[i][1])) for i in range(show_words)],
            "top_keywords": top_keywords_list[:5]
        }
        

class FrequencyHelper:
    @staticmethod
    def build_word_frequency(words):
        word_frequency_dict = {}
        for word in words:
            word_frequency_dict[word] = word_frequency_dict.get(word, 0) + 1
        return word_frequency_dict
        
    @staticmethod
    def sort_word_frequency(freq_dict):
        sorted_frequency_list = list(freq_dict.items())
        sorted_frequency_list.sort(reverse=True, key=lambda x:x[1])
        return sorted_frequency_list
 
class AnalyzerEngine:
    def __init__(self):
        self.analyzers = []
        
    def add_analyzer(self, analyzer):
        self.analyzers.append(analyzer)
        
    def run(self, text):
        context = AnalysisContext(text)

        for analyzer in self.analyzers:
            context.results[type(analyzer).__name__] = analyzer.analyze(context)
        return context.results
    
    

engine = AnalyzerEngine()

engine.add_analyzer(WordAnalyzer())
engine.add_analyzer(CharacterAnalyzer())
engine.add_analyzer(LexicalAnalyzer(reading_wpm, speaking_wpm, buffer_time))
engine.add_analyzer(FrequencyAnalyzer(stop_words))

results = engine.run("This is is is a a test.")

for n, v in results.items():
    print(n,":", v)
