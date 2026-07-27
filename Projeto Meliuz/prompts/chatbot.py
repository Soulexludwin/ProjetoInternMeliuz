from google import genai
import logging
from src.config import (
    GEMINI_API_KEY,
    MODEL_NAME,
    TEMPERATURE
)
from prompts.prompt import SYSTEM_PROMPT
import os
from dotenv import load_dotenv
logger = logging.getLogger(__name__)
load_dotenv()  # Carrega variáveis de ambiente do arquivo .env
class Chatbot:
    """
    Responsável por enviar prompts ao modelo de IA utilizando o SDK oficial do Google GenAI.
    """

    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY não encontrada no arquivo .env")
        
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_name = MODEL_NAME

    def ask(self, context: str, question: str):
        logger.info("Enviando pergunta para o modelo.")
        
        # Monta a estrutura de prompt combinando o system prompt, contexto e pergunta
        full_prompt = f"""
{SYSTEM_PROMPT}

Contexto:
{context}

Pergunta:
{question}
"""

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
                config={
                    "temperature": TEMPERATURE,
                }
            )
            return response.text
        except Exception as e:
            logger.error(f"Erro ao gerar resposta com o chatbot: {e}")
            raise e