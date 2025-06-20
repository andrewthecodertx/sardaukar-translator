"""
Sardaukar Translator FastAPI Web Application

A web interface for translating English to Sardaukar language,
with built-in text-to-speech capabilities.
"""

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
from typing import Optional

from .translator import translate_to_sardaukar, translate_with_phonetics


# Initialize FastAPI app
app = FastAPI(
    title="Sardaukar Translator",
    description="Translate English to the fictional Sardaukar language from Dune",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


# Pydantic models for API
class TranslationRequest(BaseModel):
    text: str
    include_phonetics: bool = False


class TranslationResponse(BaseModel):
    original: str
    sardaukar: str
    phonetic_guide: Optional[str] = None


# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main web interface."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/translate", response_model=TranslationResponse)
async def translate_api(request: TranslationRequest):
    """
    API endpoint for translating text to Sardaukar.
    
    Args:
        request: Translation request with text and options
        
    Returns:
        Translation response with original text, Sardaukar translation, and optional phonetics
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        if request.include_phonetics:
            sardaukar_text, phonetic_guide = translate_with_phonetics(request.text)
        else:
            sardaukar_text = translate_to_sardaukar(request.text)
            phonetic_guide = None
        
        return TranslationResponse(
            original=request.text,
            sardaukar=sardaukar_text,
            phonetic_guide=phonetic_guide
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")


@app.post("/translate", response_class=HTMLResponse)
async def translate_form(
    request: Request,
    text: str = Form(...),
    include_phonetics: bool = Form(False)
):
    """
    Form-based translation endpoint for the web interface.
    
    Args:
        request: FastAPI request object
        text: English text to translate
        include_phonetics: Whether to include phonetic guide
        
    Returns:
        HTML response with translation results
    """
    if not text.strip():
        return templates.TemplateResponse(
            "index.html", 
            {"request": request, "error": "Please enter some text to translate"}
        )
    
    try:
        if include_phonetics:
            sardaukar_text, phonetic_guide = translate_with_phonetics(text)
        else:
            sardaukar_text = translate_to_sardaukar(text)
            phonetic_guide = None
        
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "original": text,
                "sardaukar": sardaukar_text,
                "phonetic_guide": phonetic_guide,
                "include_phonetics": include_phonetics
            }
        )
    
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": f"Translation error: {str(e)}"}
        )


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "sardaukar-translator"}


@app.get("/api/examples")
async def get_examples():
    """Get example translations for demonstration."""
    examples = [
        {"english": "No! We are Sardaukar!", "sardaukar": "nah sardaukar!"},
        {"english": "It is done.", "sardaukar": "et duh."},
        {"english": "The enemy approaches", "sardaukar": "ehnmee apprahes"},
        {"english": "Victory or death!", "sardaukar": "veek-tor dehth!"},
    ]
    
    return {"examples": examples}


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Custom 404 handler."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "error": "Page not found"},
        status_code=404
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Custom 500 handler."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "error": "Internal server error"},
        status_code=500
    )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )