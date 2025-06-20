#!/usr/bin/env python3
"""
Sardaukar Translator CLI

Command-line interface for translating English to Sardaukar.
Designed to be easily integrated with other command-line tools and TTS engines.

Usage:
    python cli.py "Hello, world!"
    python cli.py "It is done." | espeak-ng
    echo "The enemy approaches" | python cli.py --stdin
"""

import sys
import argparse
from app.translator import translate_to_sardaukar, translate_with_phonetics


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Translate English text to Sardaukar language",
        epilog="Examples:\n"
               "  python cli.py \"Hello, world!\"\n"
               "  python cli.py \"It is done.\" | espeak-ng\n"
               "  echo \"The enemy approaches\" | python cli.py --stdin",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "text",
        nargs="?",
        help="English text to translate (use quotes for multi-word text)"
    )
    
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read input from stdin instead of command line argument"
    )
    
    parser.add_argument(
        "--phonetic",
        action="store_true",
        help="Include phonetic pronunciation guide for TTS"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show both original and translated text"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="Sardaukar Translator CLI 1.0.0"
    )
    
    args = parser.parse_args()
    
    # Get input text
    if args.stdin:
        try:
            input_text = sys.stdin.read().strip()
        except KeyboardInterrupt:
            print("\nInterrupted by user", file=sys.stderr)
            sys.exit(1)
    elif args.text:
        input_text = args.text
    else:
        parser.error("Either provide text as argument or use --stdin flag")
    
    if not input_text:
        print("Error: No input text provided", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Translate the text
        if args.phonetic:
            sardaukar_text, phonetic_guide = translate_with_phonetics(input_text)
        else:
            sardaukar_text = translate_to_sardaukar(input_text)
            phonetic_guide = None
        
        # Output results
        if args.verbose:
            print(f"English: {input_text}")
            print(f"Sardaukar: {sardaukar_text}")
            if phonetic_guide:
                print(f"Phonetic: {phonetic_guide}")
        else:
            print(sardaukar_text)
            if phonetic_guide and not args.verbose:
                print(f"# {phonetic_guide}", file=sys.stderr)
    
    except Exception as e:
        print(f"Error during translation: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()