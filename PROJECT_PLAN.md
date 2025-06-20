# Project Plan: English-to-Sardaukar Translator

This document outlines the plan for building a containerized Python application to translate English to the fictional Sardaukar language, with interfaces for both web and command-line usage.

### 1. System Architecture

The architecture is modular, separating the core translation logic from the interfaces that expose it. This ensures the translator can be used in different contexts without code duplication.

```mermaid
graph TD
    subgraph Development & CI/CD
        T[Unit Tests <br> (`tests/test_translator.py`)] -- Validates --> A
    end

    subgraph Docker Container
        subgraph Application Code
            A[Core Translator Module <br> (`translator.py`)]
            B[FastAPI Web Server <br> (`main.py`)]
            C[Command-Line Interface <br> (`cli.py`)]
        end
    end

    subgraph Interfaces
        D[Web Browser]
        E[Terminal/CLI]
    end

    A -- Is Imported By --> B
    A -- Is Imported By --> C

    D -- HTTP Request --> B
    E -- Executes --> C

    B -- Serves HTML/CSS/JS & API --> D
    C -- Prints to Stdout --> E
```

### 2. Development Roadmap

1.  **Project Scaffolding:** The directory structure is designed to support the modular architecture and testing.
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
2.  **Develop Core Translator (`translator.py`):** Implement the translation rules from `sardaukar_language.md` in a reusable Python module.
3.  **Write Unit Tests (`test_translator.py`):** Create a suite of tests using `pytest` to validate the `translator.py` module. This will cover the preprocessor, sound compression, and grammar engine logic.
4.  **Build Interfaces:**
    *   **Web App (`main.py` & Frontend):** Create the FastAPI server and a simple HTML form that consumes the translation API.
    *   **CLI (`cli.py`):** Develop the command-line script that takes input and prints the translated output.
5.  **Containerize the Application:**
    *   Write the `Dockerfile` to create a portable image of the application.
    *   Write the `docker-compose.yml` for easy local deployment.
6.  **Implement Text-to-Speech:**
    *   **Web:** Use the browser's `SpeechSynthesis` API for an initial implementation.
    *   **CLI:** The `cli.py` output can be piped to a command-line TTS engine (e.g., `espeak-ng`).
7.  **Documentation:** Create a comprehensive `README.md` with setup, build, usage, and testing instructions.