import re

def read_essay(filename):
    """Reads a text file and returns a set of words."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read().lower()
            words = set(re.findall(r'\b\w+\b', text))  # Extract words using regex
            return words
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return set()

def find_common_words(essay1_words, essay2_words):
    """Finds words that appear in both essays."""
    return essay1_words.intersection(essay2_words)

def search_word(word, essay1_words, essay2_words):
    """Checks if a specific word is present in either essay."""
    return word.lower() in essay1_words or word.lower() in essay2_words

def calculate_plagiarism(essay1_words, essay2_words):
    """Calculates plagiarism percentage using set operations."""
    common_words = find_common_words(essay1_words, essay2_words)
    total_unique_words = essay1_words.union(essay2_words)
    plagiarism_percentage = (len(common_words) / len(total_unique_words)) * 100 if total_unique_words else 0
    return plagiarism_percentage

def main():
    essay1_words = read_essay('essay-1.txt')
    essay2_words = read_essay('essay-2.txt')
    
    if not essay1_words or not essay2_words:
        print("Error: One or both essays could not be processed.")
        return
    
    common_words = find_common_words(essay1_words, essay2_words)
    plagiarism_percentage = calculate_plagiarism(essay1_words, essay2_words)
    
    print("\n--- Plagiarism Detection Report ---")
    print(f"Common Words Found: {len(common_words)}")
    print(f"Plagiarism Percentage: {plagiarism_percentage:.2f}%")
    print("Plagiarism Status:", "Plagiarism Detected" if plagiarism_percentage >= 50 else "No Plagiarism")
    
    # Search for a word
    word = input("Enter a word to search in both essays: ").strip()
    found = search_word(word, essay1_words, essay2_words)
    print(f"Word '{word}' found in essays: {found}")
    
if __name__ == "__main__":
    main()
