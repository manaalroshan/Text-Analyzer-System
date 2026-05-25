import os
from config import output_path
class TextAnalysisExport:
    def __init__(self):
        os.makedirs("results", exist_ok=True)
    
    def generate_report(self, word_data, char_data, sentence_data, para_data, lexical_data, vocab_statements, freq_data):
        if not all([word_data, char_data, sentence_data, para_data, lexical_data, freq_data]):
            return
        #----------------------------------------------
        # Lexical Preprocesing
        #----------------------------------------------
        vocab_comments = "N/A"
        if word_data['word_count'] < 20:
            vocab_comments= "Insufficient data for richness score"
        else:
            for limit, remark in vocab_statements:
                if lexical_data['vocabulary_score'] <= limit:
                    vocab_comments = remark
                    break
                
        #--------------------------------------------------------        
        # Freq Based stats logic - Fixed iteration bug using join
        #--------------------------------------------------------
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
        self.save_report(report, output_path)