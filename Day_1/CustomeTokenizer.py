"""
    Create a customer tokenizer for english and hindi language
"""

class VocabularyTokenizer:
    def __init__(self, offset=1000):
        self.offset = offset

    def encode(self, text):
        """
            Encodes each character as its Unicode + offset
        """
        return [ord(char) + self.offset for char in text]

    def decode(self, token_ids):
        """
            Decodes token IDs back to characters using offset
        """
        return ''.join(chr(token_id - self.offset) for token_id in token_ids)

tokenizer = VocabularyTokenizer(offset=1000)
text = input("Enter the text: ")
encoded = tokenizer.encode(text)
print("Encoded tokens:", encoded)

decoded = tokenizer.decode(encoded)
print("Decoded text:", decoded)

class HindiUnicodeTokenizer:
    def __init__(self, offset=1000):
        self.offset = offset

    def encode(self, text):
        """
        Encodes each character in the Hindi text as Unicode + offset
        """
        return [ord(char) + self.offset for char in text]

    def decode(self, token_ids):
        """
        Decodes token IDs back to Hindi characters using offset
        """
        return ''.join(chr(token_id - self.offset) for token_id in token_ids)

# Usage
tokenizer = HindiUnicodeTokenizer(offset=1000)

text = input("हिंदी में कोई वाक्य लिखें: ")
encoded = tokenizer.encode(text)
print("Encoded tokens:", encoded)

decoded = tokenizer.decode(encoded)
print("Decoded text:", decoded)