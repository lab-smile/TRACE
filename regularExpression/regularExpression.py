import re
import nltk
from nltk.corpus import words as nltk_words

nltk.download('words', quiet=True)

from .nationalities import nationalities

def findSurroundingSentences(text: str, target_word: str, context_size: int = 100) -> list:
    """
    Find sentences surrounding a target word in a given text.

    Args:
        text (str): The text to search in.
        target_word (str): The word to search for.
        context_size (int, optional): The number of words to include in the context. Defaults to 100.

    Returns:
        list: A list of context strings containing the target word.
    """
    pattern = re.compile(r'\b{}\b'.format(re.escape(target_word)))
    words = text.split()
    results = []

    for match in pattern.finditer(text):
        start_index = match.start()
        end_index = match.end()
        
        start_word_index = len(text[:start_index].split())
        end_word_index = len(text[:end_index].split())
        
        start_context_index = max(0, start_word_index - context_size)
        end_context_index = min(len(words), end_word_index + context_size)
        
        context = words[start_context_index:start_word_index] + [target_word] + words[end_word_index:end_context_index]
        context_text = ' '.join(context)
        
        results.append(context_text)
    
    return results