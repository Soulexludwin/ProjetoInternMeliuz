from pathlib import Path
import os
from dotenv import load_dotenv
import logging
from google import genai
# Se executado a partir de src/config.py, a base é a pasta pai (raiz do projeto)
BASE_DIR = Path(__file__).resolve().parent.parent

# Força o carregamento do .env apontando diretamente para a raiz do projeto
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

# ==========================================
# CONFIGURAÇÃO DE DIRETÓRIOS DO PROJETO
client = genai.Client(api_key= os.getenv("GEMINI_API_KEY"))

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
REPORTS_DIR = BASE_DIR / "reports"
OUTPUT_DIR = BASE_DIR / "output"

# Garante que os diretórios essenciais existam antes do código rodar
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# CONFIGURAÇÕES DA API E MODELO
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = "gemini-3.5-flash-lite" # Alterar caso tenha uma preferencia por outro modelo do gemini

# Parâmetros do LLM

TEMPERATURE = 0.2  
MAX_TOKENS = 2000
REQUEST_TIMEOUT = 30

# ==========================================
# DEBUG E LOGGING
DEBUG = True
LOG_LEVEL = "INFO"

# Configuração refinada do formato de log
try:
    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
except Exception:
    logging.basicConfig(level=logging.INFO)

if DEBUG:
    logging.debug("Modo DEBUG ativado. Caminhos e configurações carregados com sucesso.")