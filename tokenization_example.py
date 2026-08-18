import re

def basic_word_tokenizer(text):
    """
    A very basic word-level tokenizer that splits text by whitespace 
    and removes basic punctuation.
    """
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation using a regular expression
    text = re.sub(r'[^\w\s]', '', text)
    # Split by whitespace
    tokens = text.split()
    return tokens

if __name__ == "__main__":
    sample_text = "Hello there! Welcome to Stanford CME295: Transformers & LLMs."
    
    print("Original Text:")
    print(sample_text)
    
    tokens = basic_word_tokenizer(sample_text)
    
    print("\nTokens:")
    print(tokens)
    
    # Vocabulary creation (assigning an ID to each unique token)
    vocab = {token: idx for idx, token in enumerate(set(tokens))}
    print("\nVocabulary (Token to ID mapping):")
    print(vocab)
    
    # Encoding the text into IDs
    encoded_text = [vocab[token] for token in tokens]
    print("\nEncoded Text (IDs):")
    print(encoded_text)
