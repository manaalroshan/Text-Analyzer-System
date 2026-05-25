# This class is responsible for formatting and printing the text analysis report.
class TextAnalysisReport:
    def __init__(self, divider_char="-", divider_length=50):
        self.divider = divider_char * divider_length
    
    # Prints the report header.
    def print_header(self):
        print("\nText Analysis Report")
        print(self.divider)
        
    # Prints statistics related to words.
    def print_word_stats(self, word_data):
        if not word_data: return
        print("Word Based Stats:")
        print(f"Total Words: {word_data['word_count']}")
        print(f"Unique Words: {word_data['unique_word_count']}")
        print(f"Longest Word: '{word_data['longest_word']}' ({word_data['length_longest_word']} letters long)")
        print(self.divider)
      
    # Prints statistics related to characters.
    def print_character_stats(self, char_data):
        if not char_data: return
        print("Character Stats:")
        print(f"Total Characters (with spaces): {char_data['char_count_with_spaces']}")
        print(f"Total Characters (without spaces): {char_data['char_count_without_spaces']}")
        print(self.divider)  
        
    # Prints statistics related to sentences.
    def print_sentence_stats(self, sentence_data):
        if not sentence_data: return
        print("Sentence Based Stats:")
        print(f"Total Sentences: {sentence_data['sentence_count']}")
        print(f"Longest Sentence: {sentence_data['max_words_sentence']} Words")
        print(f"Shortest Sentence: {sentence_data['min_words_sentence']} Words")
        print(f"Avg. Sentence Length: {sentence_data['avg_words_sentence']:.1f} Words")
        print(f"Avg. Sentence Characters: {sentence_data['avg_chars_sentence']:.1f} Characters")
        print(self.divider)
        
    # Prints statistics related to paragraphs.
    def print_paragraph_stats(self, para_data):
        if not para_data: return
        print("Paragraph Stats:")
        print(f"Total Paragraphs: {para_data['paragraph_count']}")
        print(f"Avg. Sentences per Paragraph: {para_data['avg_sentence_para']:.1f}")
        print(self.divider)
        
    # Prints lexical statistics including reading/speaking time and vocabulary richness.
    def print_lexical_stats(self, lexical_data):
        if not lexical_data: return
        print("Lexical Stats:")
        print(f"Estimated Reading Time: {lexical_data['reading_time']:.1f} Seconds")
        print(f"Estimated Speaking Time: {lexical_data['speaking_time']:.1f} Seconds")
        print(f"Vocabulary Richness Score: {lexical_data['vocabulary_score']:.2f}% ({lexical_data['vocabulary_remarks']})")
        print(self.divider)
        
    # Prints frequency-based statistics like most frequent words and keywords.
    def print_frequency_stats(self, freq_data):
        if not freq_data: return
        print("Frequency Based Stats:")
        word, count = freq_data['most_frequent_word']
        if word:
            print(f"Most Frequent Word: '{word}' ({count} times)")
            
        if freq_data['top_words']:
            print("\nTop 5 Frequent Words:")
            for index, (w, c) in enumerate(freq_data['top_words']):
                print(f"{index+1}. {w:<15} → {c:>2} times")
        
        if freq_data['top_keywords']:
            print("\nTop 5 Keywords (Stop words Excluded):")
            for index, (w, c) in enumerate(freq_data['top_keywords']):
                print(f"{index+1}. {w:<15} → {c:>2} times")
        
    # Prints the report footer.
    def print_footer(self):
        print(self.divider)
        print("REPORT ENDED")
        
    # Orchestrates the display of the entire report by calling individual print methods.
    def display_report(self, results):
        self.print_header()
        self.print_word_stats(results.get('WordAnalyzer'))
        self.print_character_stats(results.get('CharacterAnalyzer'))
        self.print_sentence_stats(results.get('SentenceAnalyzer'))
        self.print_paragraph_stats(results.get('ParagraphAnalyzer'))
        self.print_lexical_stats(results.get('LexicalAnalyzer'))
        self.print_frequency_stats(results.get('FrequencyAnalyzer'))
        self.print_footer()