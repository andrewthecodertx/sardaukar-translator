# Sardaukar Translator

A containerized Python application that translates English text to the fictional Sardaukar language from the Dune universe, optimized for text-to-speech synthesis.

## Features

- **Core Translation Engine**: Implements the linguistic rules of Sardaukar including sound compression, agglutinative suffixes, and harsh phonetics
- **Web Interface**: FastAPI-based web application with interactive translation
- **Command Line Interface**: Terminal-based translator for integration with other tools
- **Text-to-Speech Ready**: Optimized output for TTS engines with proper phonetic formatting
- **Containerized**: Docker support for easy deployment locally or to the web
- **Well Tested**: Comprehensive unit tests for translation accuracy

## Quick Start

### Using Docker (Recommended)

```bash
# Build and run the application
docker-compose up --build

# Access the web interface
open http://localhost:8000

# Use the CLI
docker-compose exec app python cli.py "Hello, world!"
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Start the web server
uvicorn app.main:app --reload

# Use the CLI
python cli.py "It is done."
```

## Project Structure

```
/
├── app/
│   ├── __init__.py
│   ├── translator.py      # Core translation logic
│   ├── main.py            # FastAPI web app
│   ├── static/
│   │   └── style.css
│   └── templates/
│       └── index.html
├── tests/
│   └── test_translator.py # Unit tests for the translator
├── cli.py                 # CLI script
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Translation Examples

| English | Sardaukar | Notes |
|---------|-----------|-------|
| "No! We are Sardaukar!" | "Nah! Sardaukar!" | Compression and article removal |
| "Those who stand against us fall!" | "Suh-oost-ageesta-fallah" | Word collapse, meaning retention |
| "It is done." | "Et'sa-duh" | Compression, auxiliary verb omission |

## Language Rules

The Sardaukar language is characterized by:

- **Extreme Compression**: ~75% reduction in syllables from English
- **Agglutinative Morphology**: Suffixes for grammar (-e, -r, -de, -zi)
- **Harsh Phonetics**: Guttural consonants, simplified vowels
- **Ritualistic Delivery**: Fast, clipped speech with throat singing elements

## Development Status

🚧 **In Development** - This project is currently being built according to the specifications in `PROJECT_PLAN.md`.

## License

MIT License - See LICENSE file for details.