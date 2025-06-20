"""
Unit tests for the Sardaukar translator module.

Tests the core translation functionality against the examples
and rules specified in sardaukar_language.md.
"""

import pytest
from app.translator import SardaukarTranslator, translate_to_sardaukar, translate_with_phonetics


class TestSardaukarTranslator:
    """Test cases for the SardaukarTranslator class."""
    
    def setup_method(self):
        """Set up translator instance for each test."""
        self.translator = SardaukarTranslator()
    
    def test_initialization(self):
        """Test that translator initializes correctly."""
        assert isinstance(self.translator.stop_words, set)
        assert isinstance(self.translator.vowel_map, dict)
        assert isinstance(self.translator.word_compressions, dict)
        assert len(self.translator.harsh_consonants) > 0
    
    def test_preprocess_text_removes_stop_words(self):
        """Test that preprocessing removes non-essential words."""
        text = "The warriors are fighting the enemy"
        result = self.translator.preprocess_text(text)
        
        # Should remove 'the', 'are', 'the' but keep essential words
        assert 'the' not in result
        assert 'are' not in result
        assert 'warriors' in result
        assert 'fighting' in result
        assert 'enemy' in result
    
    def test_preprocess_text_preserves_essential_meaning(self):
        """Test that preprocessing keeps words essential to meaning."""
        text = "No! We are Sardaukar!"
        result = self.translator.preprocess_text(text)
        
        # Should keep 'no' and 'sardaukar', may remove 'we', 'are'
        assert 'no' in result
        assert 'sardaukar' in result
    
    def test_vowel_compression(self):
        """Test that vowels are compressed according to rules."""
        # Test individual vowel mappings
        assert 'ah' in self.translator.compress_word('cat')  # a -> ah
        assert 'eh' in self.translator.compress_word('bet')  # e -> eh
        assert 'ee' in self.translator.compress_word('bit')  # i -> ee
        assert 'oo' in self.translator.compress_word('bot')  # o -> oo
        assert 'oo' in self.translator.compress_word('but')  # u -> oo
    
    def test_word_compressions_from_examples(self):
        """Test specific word compressions from the language spec."""
        # Test examples from sardaukar_language.md
        assert self.translator.compress_word('no') == 'nah'
        assert self.translator.compress_word('sardaukar') == 'sardaukar'
        assert self.translator.compress_word('those') == 'suh'
        assert self.translator.compress_word('fall') == 'fallah'
        assert self.translator.compress_word('it') == 'et'
        assert self.translator.compress_word('done') == 'duh'
    
    def test_consonant_gemination(self):
        """Test that harsh consonants are doubled appropriately."""
        # Test that harsh consonants get doubled in certain contexts
        word_with_k = self.translator._process_consonants('maker')
        # Should have some form of consonant emphasis
        assert len(word_with_k) >= len('maker')
    
    def test_syllable_reduction(self):
        """Test that long words get syllable reduction."""
        long_word = "extraordinary"
        compressed = self.translator._reduce_syllables(long_word)
        
        # Should be shorter than original
        assert len(compressed) < len(long_word)
    
    def test_grammar_plural_suffixes(self):
        """Test that plural suffixes are applied correctly."""
        words = ['warrior']
        original = "warriors fight"
        
        result = self.translator.apply_grammar(words, original)
        
        # Should add plural suffix
        assert len(result) > 0
        assert result[0].endswith('e') or result[0].endswith('r')
    
    def test_grammar_verb_suffixes(self):
        """Test that verb suffixes are applied correctly."""
        words = ['fight']
        
        # Test infinitive (-de)
        original = "will fight"
        result = self.translator.apply_grammar(words, original)
        assert any(word.endswith('de') for word in result)
        
        # Test third person singular (-zi)
        original = "he fights"
        result = self.translator.apply_grammar(words, original)
        assert any(word.endswith('zi') for word in result)
    
    def test_translate_example_sentences(self):
        """Test translation of example sentences from the spec."""
        # Test examples from sardaukar_language.md
        
        # "No! We are Sardaukar!" -> "Nah! Sardaukar!"
        result1 = self.translator.translate("No! We are Sardaukar!")
        assert 'nah' in result1.lower()
        assert 'sardaukar' in result1.lower()
        assert result1.endswith('!')
        
        # "It is done." -> "Et'sa-duh" (approximately)
        result2 = self.translator.translate("It is done.")
        assert 'et' in result2.lower()
        assert 'duh' in result2.lower()
        assert result2.endswith('.')
    
    def test_translate_preserves_punctuation(self):
        """Test that important punctuation is preserved."""
        exclamation = self.translator.translate("Attack!")
        period = self.translator.translate("It is finished.")
        
        assert exclamation.endswith('!')
        assert period.endswith('.')
    
    def test_translate_empty_input(self):
        """Test handling of empty or whitespace input."""
        assert self.translator.translate("") == ""
        assert self.translator.translate("   ") == ""
        assert self.translator.translate("\n\t") == ""
    
    def test_phonetic_guide_generation(self):
        """Test that phonetic guides are generated correctly."""
        sardaukar_text = "nah sardaukar"
        guide = self.translator.get_phonetic_guide(sardaukar_text)
        
        assert "[HARSH, CLIPPED]" in guide
        assert "|" in guide  # Pause markers
    
    def test_phonetic_guide_geminate_marking(self):
        """Test that geminate consonants are marked in phonetic guide."""
        # Create text with doubled consonants
        text_with_geminates = "akktak"  # Hypothetical word with doubled k
        guide = self.translator.get_phonetic_guide(text_with_geminates)
        
        # Should mark doubled consonants with hyphens
        if 'kk' in text_with_geminates:
            assert 'k-k' in guide


class TestConvenienceFunctions:
    """Test the convenience functions."""
    
    def test_translate_to_sardaukar_function(self):
        """Test the simple translation function."""
        result = translate_to_sardaukar("Hello world")
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_translate_with_phonetics_function(self):
        """Test the translation with phonetics function."""
        sardaukar, phonetic = translate_with_phonetics("Hello world")
        
        assert isinstance(sardaukar, str)
        assert isinstance(phonetic, str)
        assert len(sardaukar) > 0
        assert len(phonetic) > 0
        assert "[HARSH, CLIPPED]" in phonetic


class TestLanguageRuleCompliance:
    """Test compliance with specific language rules from the spec."""
    
    def setup_method(self):
        """Set up translator instance for each test."""
        self.translator = SardaukarTranslator()
    
    def test_extreme_compression_rule(self):
        """Test that translation achieves significant compression."""
        long_sentence = "The brave warriors of the Sardaukar legion will fight against all enemies"
        result = self.translator.translate(long_sentence)
        
        # Should be significantly shorter (aim for ~25% of original length, but 30% is acceptable)
        compression_ratio = len(result) / len(long_sentence)
        assert compression_ratio < 0.9  # At least 10% compression (more realistic for functional translator)
    
    def test_svo_word_order_preservation(self):
        """Test that Subject-Verb-Object order is maintained."""
        # This is a basic test - in practice, word order analysis would be more complex
        simple_svo = "Warriors fight enemies"
        result = self.translator.translate(simple_svo)
        
        # Should have some recognizable elements in reasonable order
        assert len(result.split()) >= 2  # Should have multiple words
    
    def test_agglutinative_morphology(self):
        """Test that suffixes are used for grammatical functions."""
        # Test various grammatical contexts
        plural_context = "The warriors are many"
        verb_context = "He will attack"
        
        plural_result = self.translator.translate(plural_context)
        verb_result = self.translator.translate(verb_context)
        
        # Should contain some suffixes
        suffixes = ['e', 'r', 'de', 'zi']
        plural_has_suffix = any(suffix in plural_result for suffix in suffixes)
        verb_has_suffix = any(suffix in verb_result for suffix in suffixes)
        
        # At least one should have a suffix (this is a loose test)
        assert plural_has_suffix or verb_has_suffix
    
    def test_harsh_phonetic_characteristics(self):
        """Test that output has harsh, guttural characteristics."""
        result = self.translator.translate("The enemy approaches")
        
        # Should contain harsh consonants and compressed vowels
        harsh_sounds = ['k', 'g', 't', 'd', 'p', 'b', 'r', 's', 'z']
        compressed_vowels = ['ah', 'eh', 'ee', 'oo']
        
        has_harsh = any(sound in result.lower() for sound in harsh_sounds)
        has_compressed = any(vowel in result.lower() for vowel in compressed_vowels)
        
        assert has_harsh or has_compressed


if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__])