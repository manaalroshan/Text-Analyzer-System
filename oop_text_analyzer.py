import string
from config import stop_words, abbreviations_list, reading_wpm, speaking_wpm, buffer_time

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
    
    @staticmethod
    def normalize_abbreviations(text, abbreviations_list):
        words_list = text.strip().split()
        new_word_list = [word.replace(".", "") if word in abbreviations_list else word for word in words_list]
        return " ".join(new_word_list)
    
    @staticmethod
    def get_sentence_wordcount_list(normalized_text):
        # Now will Calculate Min and Mix words sentences.
        # First we gonna split the paragraph into sentences and store the numbers of words per sentence in a list.
        text = normalized_text.replace("?", ".").replace("!", ".").split(".")
        text = [i.strip() for i in text if i.strip()]
        return [len(i.split()) for i in text]
    
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
    
class AnalysisContext:
    def __init__(self, text):
        self.raw_text = text
        self.words = TextCleaner.split_text_into_words(text)  
        self.word_frequency = TextCleaner.build_word_frequency(self.words)
        self.sorted_frequency = TextCleaner.sort_word_frequency(self.word_frequency)
        self.normalized_abbr = TextCleaner.normalize_abbreviations(text, abbreviations_list)
        self.sentence_wordcount = TextCleaner.get_sentence_wordcount_list(self.normalized_abbr)
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
        try:
            word_stats = context.results["WordAnalyzer"]
        except KeyError:
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
        if not sorted_frequency:
            return {
            "most_frequent_word": (None, 0),
            "top_words": [],
            "top_keywords": []
            }
        
        show_words = min(5, len(sorted_frequency)) # for top words
        top_keywords_list = [(word, count) for word, count in sorted_frequency if word not in self.stop_words]
        
        return {
            "most_frequent_word": ((sorted_frequency[0][0], sorted_frequency[0][1])),
            "top_words": [((sorted_frequency[i][0], sorted_frequency[i][1])) for i in range(show_words)],
            "top_keywords": top_keywords_list[:5]
        }
  
class SentenceAnalyzer(Analyzer):
    def analyze(self, context):
        
        sentence_count = 0
        punctuation_list = ["?", ".", "!"]
        """I am gonna Use a heuristic to get the sentence count that is [Full stop + Space + Capital Letter = End of the sentence]
        We will increase the count if that happens.
        So for First sentence we gonna manually check if user entered valid letters and names or punctuations only.
        If we find atleast one valid character we gonna increase the count to 1."""
    
        valid_letter = any(i.isalnum() for i in context.normalized_abbr)
        if valid_letter:
            sentence_count = 1
            
        # Now our heuristic part 
        for i in range(len(context.normalized_abbr)-2):
            if context.normalized_abbr[i] in punctuation_list:
                if context.normalized_abbr[i+1] == " " and context.normalized_abbr[i+2].isupper():
                    sentence_count += 1
                    
        # Max Words in a sentence
        max_words_sentence = max(context.sentence_wordcount, default=0) 
    
        # Min Words in a sentence
        min_words_sentence = min(context.sentence_wordcount, default=0) 
        
        # Average characters, Words in a sentence
        try:
            word_count = context.results['WordAnalyzer']['word_count']
            char_count = context.results['CharacterAnalyzer']['char_count_with_spaces']
        except KeyError:
            raise RuntimeError("SentenceAnalyzer requires both WordAnalyzer and CharacterAnalyzer to run first.")
        
        avg_chars_sentence = char_count / sentence_count if sentence_count > 0 else 0 
        avg_words_sentence = word_count / sentence_count if sentence_count > 0 else 0
        
        return {
            "sentence_count": sentence_count,
            "max_words_sentence": max_words_sentence,
            "min_words_sentence": min_words_sentence,
            "avg_chars_sentence": avg_chars_sentence,
            "avg_words_sentence": avg_words_sentence,
        }
        
class ParagraphAnalyzer(Analyzer):
    def analyze(self, context):
        # Usually the parahgraph start when we press enter two times means a blank line in between so we gonna build
        # on that heuristic or logic.
        
        # Text Processing Stage
        text = context.raw_text.strip().splitlines()
        
        # We are using blank lines to separate paragraphs.
        # Each time we encounter a blank line, we add the current paragraph
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
         
        try:   
            sentence_count = context.results['SentenceAnalyzer']['sentence_count']
        except KeyError:
            raise RuntimeError("ParagraphAnalyzer requires SentenceAnalyzer to run first.")
            
            
        avg_sentence_para = sentence_count / len(paragraphs) if len(paragraphs) > 0 else 0
        return {
            "paragraph_count": len(paragraphs),
            "avg_sentence_para": avg_sentence_para,
        }  
        
    
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
    
    
# Flow of Data should remain intact for this to work as some analyzers are coupled.
class AnalyzerApp:
    def __init__(self):
        self.engine = AnalyzerEngine()
        self.engine.add_analyzer(WordAnalyzer())
        self.engine.add_analyzer(CharacterAnalyzer())
        self.engine.add_analyzer(LexicalAnalyzer(reading_wpm, speaking_wpm, buffer_time))
        self.engine.add_analyzer(FrequencyAnalyzer(stop_words))
        self.engine.add_analyzer(SentenceAnalyzer())
        self.engine.add_analyzer(ParagraphAnalyzer())
        
    def analyze(self, text):
        try:
            return self.engine.run(text)
        except ValueError:
            return None