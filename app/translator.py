"""
Sardaukar Language Translator

Implements the linguistic rules for translating English to Sardaukar,
based on the language specification in sardaukar_language.md.
"""

import re
from typing import List, Dict, Tuple


class SardaukarTranslator:
    """
    Core translator for English to Sardaukar language conversion.
    
    Implements the following transformation rules:
    1. Extreme compression (~75% syllable reduction)
    2. Agglutinative morphology (suffixes: -e, -r, -de, -zi)
    3. Sound system simplification (vowels to eh/ah/ee/oo)
    4. Harsh consonant emphasis with geminates
    """
    
    def __init__(self):
        # Stop words to remove for compression
        self.stop_words = {
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'can', 'must', 'shall', 'to', 'of', 'in',
            'on', 'at', 'by', 'for', 'with', 'from', 'up', 'about', 'into',
            'through', 'during', 'before', 'after', 'above', 'below', 'between',
            'among', 'and', 'or', 'but', 'so', 'yet', 'nor'
        }
        
        # Vowel mapping for sound compression
        self.vowel_map = {
            'a': 'ah', 'e': 'eh', 'i': 'ee', 'o': 'oo', 'u': 'oo',
            'A': 'ah', 'E': 'eh', 'I': 'ee', 'O': 'oo', 'U': 'oo'
        }
        
        # Consonant clusters to emphasize (geminate)
        self.harsh_consonants = ['k', 'g', 't', 'd', 'p', 'b', 'r', 's', 'z']
        
        # Common word compressions based on examples
        self.word_compressions = {
            'no': 'nah',
            'we': '',  # Remove entirely
            'are': '',  # Remove entirely
            'sardaukar': 'sardaukar',  # Keep as is
            'those': 'suh',
            'who': 'oost',
            'stand': 'ageesta',
            'against': 'ageesta',
            'us': '',  # Remove
            'fall': 'fallah',
            'it': 'et',
            'done': 'duh',
            'hello': 'heh-loo',
            'world': 'woor-dah',
            'yes': 'yah',
            'good': 'guud',
            'bad': 'bahd',
            'fight': 'fee-ght',
            'battle': 'baht-tul',
            'victory': 'veek-tor',
            'death': 'dehth',
            'honor': 'ahn-oor',
            'emperor': 'ehm-per-oor',
            'enemy': 'ehn-mee',
            'warrior': 'wahr-ree-oor'
        }
    
    def preprocess_text(self, text: str) -> List[str]:
        """
        Strip down input text by removing stop words and non-essential elements.
        
        Args:
            text: Input English text
            
        Returns:
            List of essential words
        """
        # Convert to lowercase and split into words
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Remove stop words but keep at least one word
        essential_words = []
        for word in words:
            if word not in self.stop_words:
                essential_words.append(word)
        
        # If we removed everything, keep the first word
        if not essential_words and words:
            essential_words = [words[0]]
        
        return essential_words
    
    def compress_word(self, word: str) -> str:
        """
        Apply sound compression and modification to a single word.
        
        Args:
            word: English word to compress
            
        Returns:
            Compressed Sardaukar word
        """
        # Check for direct word mapping first
        if word.lower() in self.word_compressions:
            return self.word_compressions[word.lower()]
        
        # Apply vowel compression
        compressed = word
        for eng_vowel, sard_vowel in self.vowel_map.items():
            compressed = compressed.replace(eng_vowel, sard_vowel)
        
        # Simplify consonant clusters and add geminates
        compressed = self._process_consonants(compressed)
        
        # Remove excessive length (aim for ~25% of original)
        compressed = self._reduce_syllables(compressed)
        
        return compressed
    
    def _process_consonants(self, word: str) -> str:
        """Process consonants to add harsh, guttural emphasis."""
        result = word
        
        # Double harsh consonants for emphasis
        for consonant in self.harsh_consonants:
            # Add geminate if consonant appears at word boundaries or stressed positions
            if consonant in result:
                # Simple rule: double if it's in the middle of the word
                pattern = f'([aeiou]){consonant}([aeiou])'
                replacement = f'\\1{consonant}{consonant}\\2'
                result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        return result
    
    def _reduce_syllables(self, word: str) -> str:
        """Reduce syllable count by ~75% through aggressive compression."""
        # Count approximate syllables (vowel groups)
        syllable_count = len(re.findall(r'[aeiou]+', word, re.IGNORECASE))
        
        if syllable_count <= 1:
            return word
        
        # For longer words, apply aggressive compression
        if len(word) > 6:
            # Keep first 2-3 characters and last 2-3 characters
            compressed = word[:3] + word[-3:]
            return compressed
        elif len(word) > 4:
            # Keep first 2 and last 2
            compressed = word[:2] + word[-2:]
            return compressed
        
        return word
    
    def apply_grammar(self, words: List[str], original_text: str) -> List[str]:
        """
        Apply agglutinative suffixes based on grammatical context.
        
        Args:
            words: List of compressed words
            original_text: Original English text for context
            
        Returns:
            Words with appropriate suffixes
        """
        if not words:
            return words
        
        result = words.copy()
        
        # Detect plurals in original text and apply -e or -r suffix
        if any(word.endswith('s') and len(word) > 1 for word in re.findall(r'\b\w+\b', original_text.lower())):
            # Apply plural suffix to the main noun (usually last content word)
            for i in range(len(result) - 1, -1, -1):
                if result[i] and not result[i].endswith(('e', 'r', 'de', 'zi')):
                    if result[i][-1] in 'aeiou':
                        result[i] += 'r'  # Vowel stem gets -r
                    else:
                        result[i] += 'e'  # Consonant stem gets -e
                    break
        
        # Detect verbs and apply appropriate suffixes
        verb_indicators = ['will', 'shall', 'going to', 'must', 'should']
        if any(indicator in original_text.lower() for indicator in verb_indicators):
            # Apply infinitive suffix -de to main verb
            for i in range(len(result)):
                if result[i] and self._is_likely_verb(result[i], original_text):
                    if not result[i].endswith(('de', 'zi')):
                        result[i] += 'de'
                    break
        
        # Third person singular gets -zi (check for verb patterns)
        original_lower = original_text.lower()
        if any(pronoun in original_lower for pronoun in ['he', 'she', 'it']) or 'fights' in original_lower:
            for i in range(len(result)):
                if result[i] and (self._is_likely_verb(result[i], original_text) or 'fight' in result[i]):
                    if not result[i].endswith(('de', 'zi')):
                        result[i] += 'zi'
                    break
        
        return result
    
    def _is_likely_verb(self, word: str, context: str) -> bool:
        """Simple heuristic to identify if a word is likely a verb."""
        # This is a simplified approach - in a full implementation,
        # you'd want to use proper POS tagging
        verb_endings = ['ing', 'ed', 'es', 's']
        context_words = context.lower().split()
        
        # Check if word appears after common verb indicators
        for i, ctx_word in enumerate(context_words):
            if word.lower() in ctx_word and i > 0:
                prev_word = context_words[i-1]
                if prev_word in ['will', 'shall', 'must', 'should', 'can', 'could']:
                    return True
        
        return any(word.lower().endswith(ending) for ending in verb_endings)
    
    def translate(self, text: str) -> str:
        """
        Main translation method that converts English text to Sardaukar.
        
        Args:
            text: English text to translate
            
        Returns:
            Translated Sardaukar text
        """
        if not text.strip():
            return ""
        
        # Step 1: Preprocess - remove stop words and extract essential meaning
        essential_words = self.preprocess_text(text)
        
        # Step 2: Compress each word according to Sardaukar phonetic rules
        compressed_words = [self.compress_word(word) for word in essential_words]
        
        # Step 3: Apply grammatical suffixes
        final_words = self.apply_grammar(compressed_words, text)
        
        # Step 4: Join with appropriate spacing and punctuation
        result = ' '.join(word for word in final_words if word)
        
        # Preserve exclamation marks and periods for dramatic effect
        if text.strip().endswith('!'):
            result += '!'
        elif text.strip().endswith('.'):
            result += '.'
        
        return result
    
    def get_phonetic_guide(self, sardaukar_text: str) -> str:
        """
        Generate a phonetic pronunciation guide for TTS optimization.
        
        Args:
            sardaukar_text: Translated Sardaukar text
            
        Returns:
            Phonetic guide with emphasis markers
        """
        # Add pronunciation hints for TTS
        phonetic = sardaukar_text
        
        # Mark geminate consonants for emphasis
        for consonant in self.harsh_consonants:
            double_pattern = consonant + consonant
            if double_pattern in phonetic:
                phonetic = phonetic.replace(double_pattern, f"{consonant}-{consonant}")
        
        # Add stress markers for harsh delivery
        phonetic = phonetic.replace(' ', ' | ')  # Pause markers
        
        return f"[HARSH, CLIPPED] {phonetic}"


# Convenience function for simple translation
def translate_to_sardaukar(text: str) -> str:
    """
    Simple function to translate English text to Sardaukar.
    
    Args:
        text: English text to translate
        
    Returns:
        Translated Sardaukar text
    """
    translator = SardaukarTranslator()
    return translator.translate(text)


# Convenience function with phonetic guide
def translate_with_phonetics(text: str) -> Tuple[str, str]:
    """
    Translate text and return both translation and phonetic guide.
    
    Args:
        text: English text to translate
        
    Returns:
        Tuple of (sardaukar_text, phonetic_guide)
    """
    translator = SardaukarTranslator()
    sardaukar = translator.translate(text)
    phonetic = translator.get_phonetic_guide(sardaukar)
    return sardaukar, phonetic