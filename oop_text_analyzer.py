import string

class Analyzer:
    def analyze(self, text):
        raise NotImplementedError

class TextCleaner:
    @staticmethod
    def raw_text(text):
        return text
    
    @staticmethod
    def remove_punctuation(text):
        modified_punctuation = string.punctuation.replace("'", "").replace("-", "")
        return text.translate(str.maketrans("","", modified_punctuation)).lower()
    
    @staticmethod
    def split_text_into_words(text):
        return TextCleaner.remove_punctuation(text).split()
    
    
class WordAnalyzer(Analyzer):
    def analyze(self, text):
        words = TextCleaner.split_text_into_words(text)
        if not words:
            raise ValueError("Input text contains no valid words")
        longestword = max(words, key=len)
        
        return {
            "word_count": len(words),
            "unique_words": len(set(words)),
            "longest_word": longestword,
            "length_longest_word": len(longestword)
        }
 
class AnalyzerEngine:
    def __init__(self):
        self.analyzers = []
        
    def add_analyzer(self, analyzer):
        self.analyzers.append(analyzer)
        
    def run_analyzers(self, text):
        results = {}
        for analyzer in self.analyzers:
            results[type(analyzer).__name__] = analyzer.analyze(text)
        return results


 
    
