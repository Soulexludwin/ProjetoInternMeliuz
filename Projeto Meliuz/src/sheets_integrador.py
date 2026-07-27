import os
import logging
import csv
from pathlib import Path
from src.config import OUTPUT_DIR
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from src.config import GOOGLE_SHEET_ID
import gspread
from google.oauth2.service_account import Credentials
logger = logging.getLogger(__name__)

def salvar_relatorio_txt(nome_arquivo_base: str, conteudo_relatorio: str):
    reports_dir = OUTPUT_DIR / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    #timestamp
    nome_limpo = nome_arquivo_base.replace(".csv", "").replace("dataset_", "").replace("temp_", "")
    timestamp_arquivo = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    txt_path = reports_dir / f"relatorio_{nome_limpo}_{timestamp_arquivo}.txt"
    
    try:
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(conteudo_relatorio)
        logger.info(f"✅ Relatório em texto salvo com sucesso: {txt_path}")
    except Exception as e:
        logger.error(f"Erro ao salvar o relatório em TXT: {e}")

# ==========================================
# NOVA FUNÇÃO DE SALVAMENTO (Atualizada)
# ==========================================
def salvar_resultado_teste(nome_teste: str, descricao: str, resultado: str, decisao: str, sincronizar_sheets: bool = False):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. Salva no CSV local (Obrigatório e sempre funciona)
    try:
        _salvar_no_csv_local(timestamp, nome_teste, descricao, resultado, decisao)
    except Exception as e:
        logger.error(f"Falha ao salvar CSV local: {e}")
        
    # 2. Envia para o Google Sheets (Opcional)
    if sincronizar_sheets:
        try:
            _enviar_para_google_sheets(timestamp, nome_teste, descricao, resultado, decisao)
            logger.info("✅ Dados sincronizados com o Google Sheets com sucesso!")
        except Exception as e:
            logger.warning(f"⚠️ Sincronização com o Google Sheets falhou ou não configurada (Verifique se sua planilha não está privada): {e}")
    else:
        logger.info("ℹ️ Sincronização com o Google Sheets desativada para esta análise.")

# ==========================================
# FUNÇÕES INTERNAS (CSV e Sheets)
# ==========================================
def _salvar_no_csv_local(timestamp: str, nome_teste: str, descricao: str, resultado: str, decisao: str):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_file = OUTPUT_DIR / "registro_testes.csv"
    
    arquivo_existe = csv_file.exists()

    try:
        with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            
            if not arquivo_existe:
                writer.writerow(["Data/Hora", "Nome do Teste", "Descrição", "Resultado", "Decisão Tomada"])
                
            writer.writerow([timestamp, nome_teste, descricao, resultado, decisao])
            
        logger.info(f"✅ Registro estruturado salvo no CSV local: {csv_file}")
    except Exception as e:
        logger.error(f"Erro ao salvar o CSV local: {e}")
        raise e

def _enviar_para_google_sheets(timestamp: str, nome_teste: str, descricao: str, resultado: str, decisao: str):
    from src.config import GOOGLE_SHEET_ID
    
    # Verifica se o ID da planilha existe
    if not GOOGLE_SHEET_ID:
        raise ValueError("O ID da planilha não foi configurado.")

    # Escopos exigidos pela API do Google
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # ATENÇÃO: O arquivo precisa estar na mesma pasta principal do projeto
    credenciais_path = "credentials.json" 
    
    if not Path(credenciais_path).exists():
        raise FileNotFoundError(f"Arquivo de credenciais não encontrado: {credenciais_path}")

    # Autenticação moderna usando google-auth
    creds = Credentials.from_service_account_file(credenciais_path, scopes=scopes)
    cliente_gspread = gspread.authorize(creds)

    # Abre a planilha pelo ID e seleciona a primeira página
    planilha = cliente_gspread.open_by_key(GOOGLE_SHEET_ID)
    aba = planilha.sheet1

    # Insere a nova linha!
    aba.append_row([timestamp, nome_teste, descricao, resultado, decisao])