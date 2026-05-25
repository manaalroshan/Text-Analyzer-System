import os, json

class ReportGenerator:
    """
    Responsible for transforming raw analysis dictionaries into a structured 
    and human-readable string format.
    """

    def generate_report(self, word_data, char_data, sentence_data, para_data, lexical_data, freq_data):
        """Constructs a formatted string containing all analysis statistics."""
        if not all([word_data, char_data, sentence_data, para_data, lexical_data, freq_data]):
            return
     
        # Format frequency statistics into aligned, readable strings.
        word, count = freq_data['most_frequent_word']
        show_top_words = "\n".join([f"{i+1}. {w:<15} → {c:>2} times" for i, (w, c) in enumerate(freq_data['top_words'])])
        show_top_keywords = "\n".join([f"{i+1}. {w:<15} → {c:>2} times" for i, (w, c) in enumerate(freq_data['top_keywords'])])
            
        # Construct the final string using an f-string for clarity and performance.
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
                f"Vocabulary Richness Score: {lexical_data['vocabulary_score']:.2f}% ({lexical_data['vocabulary_remarks']})\n"
                "-------------------------------------------------------------------------\n" 
                "Frequency Based Stats:\n"
                f"Most Frequent Word: '{word}' ({count} times)\n"
                "\nTop 5 Frequent Words:\n"
                f"{show_top_words}\n"
                "\nTop 5 Keywords (Stopwords Excluded):\n"
                f"{show_top_keywords}"   
            )
    
    def build_report(self, results):
        """High-level method to generate and save the report from analysis results."""
        report = self.generate_report(
            results.get('WordAnalyzer'),
            results.get('CharacterAnalyzer'),
            results.get('SentenceAnalyzer'),
            results.get('ParagraphAnalyzer'),
            results.get('LexicalAnalyzer'),
            results.get('FrequencyAnalyzer')    
        )
        return report
        
class ReportExporter:
    """Handles the generation and file export of text analysis reports."""
    
    def __init__(self):
        """Initializes the exporter and ensures the output directory exists."""
        os.makedirs("results", exist_ok=True)
        
    def save_report(self, report, output_path):
        """Writes a string report to a physical text file."""
        if report is None:
            return
            
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(report)
            
    def save_json(self, results, json_output_path):
        """Exports the raw results dictionary to a JSON file for machine readability."""
        with open(json_output_path, "w", encoding="utf-8") as file:
            json.dump(results, file, indent=4)