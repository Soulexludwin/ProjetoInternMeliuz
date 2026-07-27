from pathlib import Path
import os
from dotenv import load_dotenv
import logging
from google import genai
import sys

# ==========================================
# CONFIGURAÇÃO DE DIRETÓRIOS E AMBIENTE
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

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
if not GEMINI_API_KEY or GEMINI_API_KEY.strip() == "":
    print("Chave GEMINI_API_KEY (.env) não encontrada.")
    GEMINI_API_KEY = input("Cole sua chave da API do Gemini aqui (NÃO USE ESPAÇO): ").strip()
    
    if GEMINI_API_KEY:
        os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
        try:
            with open(env_path, "w", encoding="utf-8") as f:
                f.write(f"GEMINI_API_KEY={GEMINI_API_KEY}\n")
            print(f"✅ Chave salva com sucesso em: {env_path}")
        except Exception as e:
            print(f"⚠️ Não foi possível salvar o arquivo .env automaticamente: {e}")
    else:
        raise ValueError("❌ Nenhuma chave de API foi informada. O programa será encerrado.")

# Inicializa o cliente do Gemini de forma segura e única
client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-3.5-flash-lite"  # Nome de modelo estável atualizado

# Parâmetros do LLM
# ===========================================
TEMPERATURE = 0.2 
MAX_TOKENS = 2000
REQUEST_TIMEOUT = 30

# ==========================================
# DEBUG E LOGGING
DEBUG = True
LOG_LEVEL = "INFO"

# Configuração refinada do formato de log
# ===========================================
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