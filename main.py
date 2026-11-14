import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api.rutas import router

app = FastAPI(
    title="Sistema de Gestion Veterinaria",
    description="API para gestion de pacientes veterinarios con comparacion de busqueda lineal y arbol BST.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

# ── Servir archivos estáticos del frontend ──
app.mount("/static", StaticFiles(directory="web"), name="static")


@app.get("/")
def root():
    """Sirve el frontend (index.html) en la raíz."""
    return FileResponse("web/index.html")


# ── Configuración de base de datos con ruta absoluta ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "datos", "veterinaria.db")


@app.on_event("startup")
def startup():
    """Inicializa la base de datos al arrancar la aplicación."""
    from servicios.persistencia import inicializar_db
    inicializar_db(DB_PATH)


# Health check accesible también en la raíz (sin prefijo /api)
@app.get("/health")
def health_check_root():
    """Endpoint de salud accesible en /health (sin prefijo /api)."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
