import string
import sys
from config import stop_words, abbreviations_list, vocab_statements, reading_wpm, speaking_wpm, buffer_time

# This Function Cleans the text and returns punctuation free text.
def remove_punctuation(text):
    modified_punctuation = string.punctuation.replace("'", "").replace("-", "")
    no_punctuation_text = text.translate(str.maketrans("","", modified_punctuation)).lower()
    return no_punctuation_text

# This Funtions retuns a words list
def split_text_into_words(text):
    return text.split()

# This Function Analyzes word metric and return them into a dictionary
def compute_word_statistics(text_words):
    # Unique Words
    unique_word_set = set(text_words)
    
    # Longest Word
    longest_word = max(text_words, key=len)

    return {
        "word_count": len(text_words),
        "unique_words": len(unique_word_set),
        "longest_word": longest_word,
        "longest_word_length": len(longest_word),
    }
    
def compute_lexical_metrics(word_count, unique_words):
    return {
        "reading_time": 60 * (word_count/reading_wpm),
        "speaking_time": (word_count / speaking_wpm) * buffer_time * 60,
        "vocab_score": (unique_words / word_count) * 100,
    }
    
# Calculate total Characters 
def count_characters(text):
    char_count_nospace = len("".join(text.split())) # Removes all type of whitespaces.
    char_count_withspace = len(text)
    
    return char_count_nospace, char_count_withspace

def normalize_abbreviations(text):
    words_list = text.strip().split()
    new_word_list = [word.replace(".", "") if word in abbreviations_list else word for word in words_list]
    return " ".join(new_word_list)

def compute_sentence_count(text):
    sentence_count = 0
    punctuation_list = ["?", ".", "!"]
    """I am gonna Use a heuristic to get the sentence count that is [Full stop + Space + Capital Letter = End of the sentence]
    We will increase the count if that happens.
    So for First sentence we gonna manually check if user entered valid letters and names or punctuations only.
    If we find atleast one valid character we gonna increase the count to 1."""
    
    valid_letter = any(i.isalnum() for i in text)
    if valid_letter:
        sentence_count = 1
        
    # Now our heuristic part 
    for i in range(len(text)-2):
        if text[i] in punctuation_list:
            if text[i+1] == " " and text[i+2].isupper():
                sentence_count += 1
    
    return sentence_count
    
def get_sentence_wordcount_list(text):
    # Now will Calculate Min and Mix words sentences.
    # First we gonna split the paragraph into sentences and store the numbers of words per sentence in a list.
    text = text.replace("?", ".").replace("!", ".").split(".")
    text = [i.strip() for i in text if i.strip()]
    return [len(i.split()) for i in text]
    
# Calculates sentence stats  
def get_sentence_statistics(chunks_list, sentence_count, char_count, word_count):
    # Max Words in a sentence
    max_words_sentence = max(chunks_list, default=0) 
    
    # Min Words in a sentence
    min_words_sentence = min(chunks_list, default=0) 
    
    # Average characters, Words in a sentence
    if sentence_count > 0:
        avg_chars_sentence = char_count // sentence_count
        avg_words_sentence = word_count // sentence_count
    else:
        avg_chars_sentence = 0
        avg_words_sentence = 0
    
    return {
        "max_words_sentence": max_words_sentence,
        "min_words_sentence": min_words_sentence,
        "avg_chars_sentence": avg_chars_sentence,
        "avg_words_sentence": avg_words_sentence,
    }

# Calculates Paragraph stats 
def get_paragraph_statistics(text, sentence_count):
    # Usually the parahgraph start when we press enter two times means a blank line in between so we gonna build
    # on that heuristic or logic.
    
    # Text Processing Stage
    text = text.strip().splitlines()
    
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
         
    avg_sentence_para = sentence_count / len(paragraphs) if len(paragraphs) > 0 else 0
    return {
        "paragraph_count": len(paragraphs),
        "avg_sentence_para": avg_sentence_para,
    }

def build_word_frequency(text):
    word_frequency_dict = {}
    for word in text:
        word_frequency_dict[word] = word_frequency_dict.get(word, 0) + 1
    return word_frequency_dict

def sort_word_frequency(freq_dict):
    word_freq_list = list(freq_dict.items())
    word_freq_list.sort(reverse=True, key=lambda x:x[1])
    return word_freq_list
    
def get_frequent_words(freq_list):
    show_words = min(5, len(freq_list))
    return [((freq_list[i][0], freq_list[i][1])) for i in range(show_words)]
        
def get_most_frequent_word(freq_list):
    return ((freq_list[0][0], freq_list[0][1]))

def extract_top_keywords(freq_list, stop_words):
    top_keywords_list = [(word, count) for word, count in freq_list if word not in stop_words]      
    return top_keywords_list[:5]

# Syster Layering --------------------------------------------------------------------------------------------
def analyze_frequency_layer(words, stop_words):
    word_frequency = build_word_frequency(words)
    sorted_word_frequency = sort_word_frequency(word_frequency)

    return {
        "top_words": get_frequent_words(sorted_word_frequency), # Top 5 Most Frequent Words
        "top_keywords": extract_top_keywords(sorted_word_frequency, stop_words), # Top 5 Keywords(No stop Words)
        "most_freq_word": get_most_frequent_word(sorted_word_frequency) # Most Frequent Word
    }   

def prepare_text_data(text):
    clean_text = remove_punctuation(text)
    words = split_text_into_words(clean_text)
    return words
    
def analyze_word_layer(words):
    word_stats = compute_word_statistics(words)
    
    return {
    "word_count": word_stats['word_count'],
    "unique_words": word_stats['unique_words'],
    "longest_word": word_stats['longest_word'],
    "longest_word_length": word_stats['longest_word_length'],
    }
    
def analyze_lexical_layer(word_count, unique_words, vocab_statements):
    text_stats = compute_lexical_metrics(word_count, unique_words)
    return {
        "reading_time": text_stats['reading_time'], # Reading Time
        "speaking_time": text_stats['speaking_time'], # Speaking Time
        "vocab_rich_score": text_stats['vocab_score'], # Vocabulary Richness (Type Token Ratio)
        "vocab_statements": vocab_statements,
    }
    
def analyze_character_layer(text):
    char_count_no_spaces, char_count_with_spaces = count_characters(text)
    return {
        "char_count_no_spaces": char_count_no_spaces,
        "char_count_with_spaces": char_count_with_spaces,
    }
    
def analyze_sentence_layer(text, char_count_with_spaces, word_count):
    normalized_text = normalize_abbreviations(text)
    sentence_count = compute_sentence_count(normalized_text) # Sentence count
    sentence_chunks_list = get_sentence_wordcount_list(normalized_text)
    sentence_stats = get_sentence_statistics(sentence_chunks_list, sentence_count, char_count_with_spaces, word_count)
    
    return {
        "sentence_count": sentence_count, # Sentence count
        **sentence_stats
    }
    
def analyze_paragraph_layer(text, sentence_count):
    return get_paragraph_statistics(text, sentence_count) # Returns a dict
    

# Manager Function--------------------------------------------------------------------------
def analyze_text(text):
    # Getting Punctuation Free Text and Words
    words = prepare_text_data(text)
    if not words:
        return None
    
    # Word Layer
    word_layer = analyze_word_layer(words)

    # Character count
    character_layer = analyze_character_layer(text)
        
    # Word Frequency Based Metrics
    frequency_layer = analyze_frequency_layer(words, stop_words)
    
    # Lexical Later
    lexical_layer = analyze_lexical_layer(word_layer['word_count'], word_layer['unique_words'], vocab_statements)
    
    # Sentence Layer
    sentence_layer = analyze_sentence_layer(text, character_layer['char_count_with_spaces'], word_layer["word_count"])
    
    # Paragraph Layer
    paragraph_layer = analyze_paragraph_layer(text, sentence_layer['sentence_count'])
    
    return{
        **word_layer,
        **character_layer,
        **lexical_layer,
        **frequency_layer,
        **sentence_layer,
        **paragraph_layer,
    }