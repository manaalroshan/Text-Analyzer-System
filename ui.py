import os
from config import output_path
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
    def print_lexical_stats(self, lexical_data, vocab_statements, word_stats):
        if not lexical_data or not word_stats: return
        print("Lexical Stats:")
        print(f"Estimated Reading Time: {lexical_data['reading_time']:.1f} Seconds")
        print(f"Estimated Speaking Time: {lexical_data['speaking_time']:.1f} Seconds")
        
        vocab_comments = "N/A"
        if word_stats['word_count'] < 20:
            print(f"Vocabulary Richness: Insufficient data for richness score")
        else:
            for limit, remark in vocab_statements:
                if lexical_data['vocabulary_score'] <= limit:
                    vocab_comments = remark
                    break
            print(f"Vocabulary Richness Score: {lexical_data['vocabulary_score']:.2f}% ({vocab_comments})")
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
    def display_report(self, results, vocab_statements):
        self.print_header()
        self.print_word_stats(results.get('WordAnalyzer'))
        self.print_character_stats(results.get('CharacterAnalyzer'))
        self.print_sentence_stats(results.get('SentenceAnalyzer'))
        self.print_paragraph_stats(results.get('ParagraphAnalyzer'))
        self.print_lexical_stats(results.get('LexicalAnalyzer'), vocab_statements, results.get('WordAnalyzer'))
        self.print_frequency_stats(results.get('FrequencyAnalyzer'))
        self.print_footer()
        
class TextAnalysisExport:
    def __init__(self):
        os.makedirs("results", exist_ok=True)
    
    def generate_report(self, word_data, char_data, sentence_data, para_data, lexical_data, vocab_statements, freq_data):
        
        if not all([word_data, char_data, sentence_data, para_data, lexical_data, freq_data]):
            return

        # Vocab Score message logic
        vocab_comments = "N/A"
        if word_data['word_count'] < 20:
            vocab_comments= "Insufficient data for richness score"
        else:
            for limit, remark in vocab_statements:
                if lexical_data['vocabulary_score'] <= limit:
                    vocab_comments = remark
                    break
                
        # Freq Based stats logic - Fixed iteration bug using join
        word, count = freq_data['most_frequent_word']
        show_top_words = "\n".join([f"{i+1}. {w:<15} → {c:>2} times" for i, (w, c) in enumerate(freq_data['top_words'])])
        show_top_keywords = "\n".join([f"{i+1}. {w:<15} → {c:>2} times" for i, (w, c) in enumerate(freq_data['top_keywords'])])
            
        return (
                "Text Analysis Report\n"
                "-------------------------------------------------------------------------\n"
                "Word Based Stats:\n"
                f"Total Words: {word_data['word_count']}\n"
                f"Unique Words: {word_data['unique_word_count']}\n"
                f"Longest Word: '{word_data['longest_word']}' ({word_data['length_longest_word']} letters long)\n"
                "-------------------------------------------------------------------------\n"
                "Character Stats:\n"
                f"Total Characters (with spaces): {char_data['char_count_with_spaces']}\n"
                f"Total Characters (without spaces): {char_data['char_count_without_spaces']}\n"
                "-------------------------------------------------------------------------\n"
                "Sentence Based Stats:\n"
                f"Total Sentences: {sentence_data['sentence_count']}\n"
                f"Longest Sentence: {sentence_data['max_words_sentence']} Words\n"
                f"Shortest Sentence: {sentence_data['min_words_sentence']} Words\n"
                f"Avg. Sentence Length: {sentence_data['avg_words_sentence']:.1f} Words\n"
                f"Avg. Sentence Characters: {sentence_data['avg_chars_sentence']:.1f} Characters\n"
                "-------------------------------------------------------------------------\n"
                "Paragraph Stats:\n"
                f"Total Paragraphs: {para_data['paragraph_count']}\n"
                f"Avg. Sentences per Paragraph: {para_data['avg_sentence_para']:.1f}\n"
                "-------------------------------------------------------------------------\n"
                "Lexical Stats:\n"
                f"Estimated Reading Time: {lexical_data['reading_time']:.1f} Seconds\n"
                f"Estimated Speaking Time: {lexical_data['speaking_time']:.1f} Seconds\n"
                f"Vocabulary Richness Score: {lexical_data['vocabulary_score']:.2f}% ({vocab_comments})\n"
                "-------------------------------------------------------------------------\n" 
                "Frequency Based Stats:\n"
                f"Most Frequent Word: '{word}' ({count} times)\n"
                "\nTop 5 Frequent Words:\n"
                f"{show_top_words}\n"
                "\nTop 5 Keywords (Stopwords Excluded):\n"
                f"{show_top_keywords}"   
            )
    
    def save_report(self, report, output_path):
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(report)
    
    def export_report(self, results, vocab_statements):
        report = self.generate_report(
            results.get('WordAnalyzer'),
            results.get('CharacterAnalyzer'),
            results.get('SentenceAnalyzer'),
            results.get('ParagraphAnalyzer'),
            results.get('LexicalAnalyzer'), vocab_statements,
            results.get('FrequencyAnalyzer')    
        )
        self.save_report(output_path, report)
        
