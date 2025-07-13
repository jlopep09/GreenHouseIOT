from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import requests
import base64
import json
import os
from typing import Optional
import uvicorn

app = FastAPI(title="Cultivo Analysis API", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")

@app.post("/analyze-crop")
async def analyze_crop(
    prompt: str = Form(...),
    image: UploadFile = File(...),
    temperature: Optional[float] = Form(0.3),
    max_tokens: Optional[int] = Form(1000)
):
    """
    Analiza una imagen de cultivo con datos de sensores
    
    Args:
        prompt: Texto con datos de sensores y pregunta específica
        image: Archivo de imagen del cultivo
        temperature: Creatividad de la respuesta (0.0-1.0)
        max_tokens: Máximo número de tokens en la respuesta
    """
    
    try:
        # Leer y codificar la imagen
        image_content = await image.read()
        image_base64 = base64.b64encode(image_content).decode('utf-8')
        
        # Crear prompt estructurado
        structured_prompt = f"""
Eres un experto en agricultura y análisis de cultivos. 
Analiza la siguiente imagen de cultivo junto con los datos proporcionados.

{prompt}

Proporciona recomendaciones específicas y accionables basadas en:
1. La planta o cultivo que observas en la imagen
2. Los datos de sensores proporcionados
3. Mejores prácticas agrícolas

Estructura tu respuesta de forma clara y práctica.
"""

        # Preparar request para Ollama
        payload = {
            "model": "llava:13b",
            "prompt": structured_prompt,
            "images": [image_base64],
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        # Enviar request al modelo
        response = requests.post(
            f"{OLLAMA_API_URL}/api/generate",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=120
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error del modelo: {response.text}"
            )
        
        result = response.json()
        
        return {
            "status": "success",
            "analysis": result.get("response", ""),
            "metadata": {
                "model": "llava:13b",
                "temperature": temperature,
                "max_tokens": max_tokens,
                "image_size": len(image_content)
            }
        }
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=503,
            detail=f"Error conectando con el modelo: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Endpoint de salud"""
    try:
        response = requests.get(f"{OLLAMA_API_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            return {"status": "healthy", "model_status": "active"}
        else:
            return {"status": "unhealthy", "model_status": "inactive"}
    except:
        return {"status": "unhealthy", "model_status": "unreachable"}

@app.get("/")
async def root():
    return {
        "message": "Cultivo Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/analyze-crop",
            "health": "/health",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)