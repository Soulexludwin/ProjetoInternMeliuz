import os
import logging
import csv
from pathlib import Path
from src.config import OUTPUT_DIR
from datetime import datetime

logger = logging.getLogger(__name__)

def salvar_relatorio_txt(nome_arquivo_base: str, conteudo_relatorio: str):
    reports_dir = OUTPUT_DIR / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    # Limpa o nome e adiciona um timestamp detalhado (AnoMêsDia_HoraMinutoSegundo)
    nome_limpo = nome_arquivo_base.replace(".csv", "").replace("dataset_", "").replace("temp_", "")
    timestamp_arquivo = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    txt_path = reports_dir / f"relatorio_{nome_limpo}_{timestamp_arquivo}.txt"
    
    try:
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(conteudo_relatorio)
        logger.info(f"✅ Relatório em texto salvo com sucesso: {txt_path}")
    except Exception as e:
        logger.error(f"Erro ao salvar o relatório em TXT: {e}")
        
def salvar_resultado_teste(nome_teste: str, descricao: str, resultado: str, decisao: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _salvar_no_csv_local(timestamp, nome_teste, descricao, resultado, decisao)
        
def _salvar_no_csv_local(timestamp: str, nome_teste: str, descricao: str, resultado: str, decisao: str):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_file = OUTPUT_DIR / "registro_testes.csv"
    
    arquivo_existe = csv_file.exists()

    try:
        with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter='|')
            
            if not arquivo_existe:
                writer.writerow(["Data/Hora", "Nome do Teste", "Descrição", "Resultado", "Decisão Tomada"])
                
            writer.writerow([timestamp, nome_teste, descricao, resultado, decisao])
            
        logger.info(f" Registro estruturado salvo no CSV local: {csv_file}")
    except Exception as e:
        logger.error(f"Erro ao salvar o CSV local: {e}")
        raise e