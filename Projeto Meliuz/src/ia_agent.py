from google import genai
import logging
import os

from prompts.prompt import SYSTEM_PROMPT
from src.config import GEMINI_API_KEY, MODEL_NAME, TEMPERATURE

logger = logging.getLogger(__name__)

class GrowthAIAgent:
    def __init__(self):
        # A chave deve ter sido configurada previamente no main.py
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY não encontrada nas variáveis de ambiente.")
        
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_name = MODEL_NAME

    def analyze_test(self, csv_data_summary: str) -> str:
        """
        Envia os dados resumidos do CSV para o LLM analisar.
        """
        logger.info("Enviando dados do teste A/B para o modelo...")
        
        # Monta a estrutura final combinando as instruções e a tabela de dados
        full_prompt = f"{SYSTEM_PROMPT}\n\nAqui estão os dados do teste A/B agregados:\n{csv_data_summary}"

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt,
                config={
                    "temperature": TEMPERATURE,
                }
            )
            return response.text or ""
            
        except Exception as e:
            error_msg = str(e)
            # Tratamento específico para evitar quebras por erro de digitação do modelo
            if "404" in error_msg or "NOT_FOUND" in error_msg:
                logger.error(f"Erro 404: O modelo '{self.model_name}' não foi encontrado. Verifique se o nome do modelo no config.py está correto (ex: 'gemini-1.5-flash').")
            else:
                logger.error(f"Erro ao gerar resposta com a IA: {e}")
            raise e
        
def analyze_ab_test(csv_data_summary: str) -> str:
    agent = GrowthAIAgent()
    return agent.analyze_test(csv_data_summary)