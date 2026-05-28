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

**Note:** Docker requires proper permissions. If you get permission errors, either:
- Add your user to the docker group: `sudo usermod -aG docker $USER` (then logout/login)
- Or use `sudo` with docker commands

```bash
# Build and run the application
docker-compose up --build

# Access the web interface
open http://localhost:8000

# Use the CLI inside container
docker-compose exec sardaukar-translator python cli.py "Hello, world!"

# Alternative: Build and run manually
docker build -t sardaukar-translator .
docker run -p 8000:8000 sardaukar-translator
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
| "No! We are Sardaukar!" | "nah sardaukar!" | Compression and article removal |
| "Those who stand against us fall!" | "suh-oost-ageesta fallah" | Word collapse, meaning retention |
| "It is done." | "et duhe." | Compression, auxiliary verb omission |
| "The spice must flow" | "speceh floow" | Essential meaning preservation |
| "Victory or death!" | "veek-tor dehth!" | Harsh consonant emphasis |

## Language Rules

The Sardaukar language is characterized by:

- **Extreme Compression**: ~75% reduction in syllables from English
- **Agglutinative Morphology**: Suffixes for grammar (-e, -r, -de, -zi)
- **Harsh Phonetics**: Guttural consonants, simplified vowels
- **Ritualistic Delivery**: Fast, clipped speech with throat singing elements

## CLI Usage Examples

```bash
# Basic translation
python cli.py "Hello, world!"
# Output: heh-loo woor-dah

# With phonetic guide for TTS
python cli.py "It is done." --phonetic --verbose
# Output:
# English: It is done.
# Sardaukar: et duhe.
# Phonetic: [HARSH, CLIPPED] et | duhe.

# Pipeline integration with TTS
echo "The enemy approaches" | python cli.py --stdin | espeak-ng

# Help and options
python cli.py --help
```

## API Usage

```bash
# Start the web server
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Test the API
curl -X POST "http://localhost:8000/api/translate" \
     -H "Content-Type: application/json" \
     -d '{"text": "Victory or death!", "include_phonetics": true}'

# Access interactive API docs
open http://localhost:8000/api/docs
```

## Troubleshooting

### Docker Permission Issues
If you encounter Docker permission errors:
```bash
# Add user to docker group (requires logout/login)
sudo usermod -aG docker $USER

# Or use sudo with docker commands
sudo docker-compose up --build
```

### Virtual Environment Issues
```bash
# Create fresh virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### TTS Integration
For command-line text-to-speech integration:
```bash
# Install espeak-ng (Ubuntu/Debian)
sudo apt-get install espeak-ng

# Use with Sardaukar translator
python cli.py "The spice must flow" | espeak-ng -s 120 -p 30
```

## Development Status

✅ **Complete** - Full implementation with all features working as specified in [`PROJECT_PLAN.md`](PROJECT_PLAN.md).

## License

MIT, see [LICENSE](LICENSE).

## Contributing

PRs welcome. Please open an issue first for major changes.
