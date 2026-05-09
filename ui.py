from text_analyzer import analyze_text

def print_header():
    print("\nText Analysis Report")
    print("-"*50)
    return

def print_word_statistics(result):
    print("Word Based Stats:")
    print(f"Total Words: {result['word_count']}")
    print(f"Unique Words: {result['unique_words']}")
    print(f"Longest Word: {result['longest_word']}, {result['longest_word_length']} letters long.")
    print("-"*50)
    
def print_character_statistics(result):
    print("Character Stats:")
    print(f"Total Characters (without spaces): {result['char_count_no_spaces']}")
    print(f"Total Characters (with spaces): {result['char_count_with_spaces']}")
    print("-"*50)

def print_sentence_statistics(result):
    print("Sentence Based Stats:")
    print(f"Total Sentences: {result['sentence_count']}")
    print(f"Longest Sentence (Words): {result['max_words_sentence']}")
    print(f"Shortest Sentence (Words): {result['min_words_sentence']}")
    print(f"Avg. Sentence Words: {result['avg_words_sentence']}")
    print(f"Avg. Sentence Chars: {result['avg_chars_sentence']}")
    print("-"*50)
    
def print_paragraph_statistics(result):
    print("Paragraph Stats:")
    print(f"Total Paragraphs: {result['paragraph_count']}")
    print(f"Average sentences (per Para.): {result['avg_sentence_para']:.1f}")
    print("-"*50)
    
def print_lexical_statistics(result):
    print("Lexical Stats:")
    print(f"Estimated Reading Time: {result['reading_time']:.1f} Seconds.")
    print(f"Estimated Speaking Time: {result['speaking_time']:.1f} Seconds.")
    # Vocabulary Richness
    if result['word_count'] < 20:
        print(f"Vocabulary Richness: Insufficient data for richness score")
    else:
        for limit, remark in result['vocab_statements']:
            if result['vocab_rich_score'] <= limit:
                vocab_comments = remark
                break
        print(f"Vocabulary Richness: {result['vocab_rich_score']:.2f} ({vocab_comments})")
    print("-"*50)
    
def print_frequency_statistics(result):
    print("Frequency Based Stats:")
    # Most Frequent Word
    word, count = result['most_freq_word']
    print(f"Most Frequent word: {word}, {count} Times.")
    
    # Top words frequency
    print("Top 5 Frequent Words")
    for index, (word, count) in enumerate(result["top_words"]):
        print(f"{index+1}. {word:<15}→{count:>2} times")
        
    # Top keywords(Stop Words Excluded)
    print("Top 5 keywords(Stopwords Excluded)")
    for index, (word, count) in enumerate(result['top_keywords']):
        print(f"{index+1}. {word:<15}→{count:>2} times")
        
def print_footer():
    print("-"*50)
    print("Created By MRX")
    
    
    
# Prints Output
def display_results(result):
    # Header
    print_header()
    
    # Word stats
    print_word_statistics(result)
    
    # Chracter stats
    print_character_statistics(result)
    
    # Sentence stats
    print_sentence_statistics(result)
    
    # Paragraph stats
    print_paragraph_statistics(result)
    
    # Lexical stats
    print_lexical_statistics(result)
    
    # Frequency stats
    print_frequency_statistics(result)
    
    # Footer
    print_footer()